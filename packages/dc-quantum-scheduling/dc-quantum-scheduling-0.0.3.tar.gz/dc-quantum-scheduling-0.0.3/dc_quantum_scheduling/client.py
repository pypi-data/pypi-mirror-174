#    Copyright 2018-2022 Carsten Blank
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
import logging
from typing import Optional, List

import qiskit
import requests
from qiskit.providers.ibmq import IBMQBackend
from retry import retry

from .qiskit.qiskit_provider import provider
from .models import PreparedExperiment, RunningExperiment, FinishedExperiment

LOG = logging.getLogger(__name__)

_url = 'http://localhost:8080'


def set_url(url: str):
    global _url
    _url = url


def is_done(key) -> bool:
    status = get_status(key)
    if status is None:
        raise UserWarning(f"Experiment with key {key} is does not exist!")
    return status == 'finished'


def get_status(key) -> Optional[str]:
    status_response: requests.Response = requests.get(f'{_url}/qiskit/experiment/{key}/status')
    if status_response.status_code == 200:
        return status_response.json().get('status')
    else:
        return None


def get_error(key) -> Optional[str]:
    status_response: requests.Response = requests.get(f'{_url}/qiskit/experiment/{key}/error')
    if status_response.status_code == 200:
        return status_response.json().get('error')
    else:
        return None


def clear_error(key) -> Optional[str]:
    status_response: requests.Response = requests.patch(f'{_url}/qiskit/experiment/{key}/error')
    if status_response.status_code == 200:
        return status_response.json().get('status')
    else:
        return None


@retry((requests.exceptions.ConnectionError, ConnectionError), backoff=2, max_delay=8, tries=4)
def save_prepared_experiment(experiment: PreparedExperiment) -> str:
    result_response: requests.Response = requests.post(
        f'{_url}/qiskit/experiment',
        json=experiment.to_dict()
    )
    if result_response.status_code == 200:
        return result_response.json().get('id')
    else:
        raise ConnectionError(f"Problem while saving experiment. Details: {result_response.text}")


def get_experiment(key, raise_error=True) -> [PreparedExperiment or RunningExperiment or FinishedExperiment]:
    status = get_status(key)

    if status == 'deleted' and raise_error:
        msg = f"Experiment with key {key} is scheduled for deletion!"
        if raise_error:
            raise UserWarning(msg)
        else:
            LOG.error(msg)
    if status == 'error':
        msg = f"Experiment with key {key} had an error. Details {get_error(key)}"
        if raise_error:
            raise UserWarning(msg)
        else:
            LOG.error(msg)

    status_response: requests.Response = requests.get(f'{_url}/qiskit/experiment/{key}')
    if status_response.status_code == 200:
        experiment_dictionary = status_response.json()
        if status in ['prepared', 'error', 'deleted']:
            return PreparedExperiment.from_dict(experiment_dictionary)
        elif status == 'running':
            return RunningExperiment.from_dict(experiment_dictionary)
        elif status == 'finished':
            return FinishedExperiment.from_dict(experiment_dictionary)
        else:
            raise ValueError(f"Status {status} found, which is not in the expected ones: prepared, running, finished.")
    else:
        return None


def delete_experiment(key: str) -> None:
    response = requests.delete(f"{_url}/qiskit/experiment/{key}")
    if response.status_code != 200:
        raise ConnectionError(f"Problem while deleting experiment. Details: {response.text}")


def run_experiment(key: str, backend: [str or IBMQBackend], ibmq_config: Optional[dict] = None) -> None:
    backend_name = backend.name() if isinstance(backend, IBMQBackend) else backend

    if ibmq_config is None:
        active_provider = provider()
        active_account = qiskit.IBMQ.active_account()
        ibmq_config = {
            "hub": active_provider.credentials.hub,
            "group": active_provider.credentials.group,
            "project": active_provider.credentials.project,
            "url": active_account['url'],
            "token": active_provider.credentials.token
        }

    response: requests.Response = requests.post(
        f'{_url}/qiskit/experiment/{key}/run/{backend_name}',
        json=ibmq_config
    )

    if response.status_code != 200:
        raise UserWarning(f"Error during run command for experiment {key}. Details: {response.text}")


def get_experiments(*tags) -> List[str]:
    tags_list = "&".join([f'tags={t}' for t in tags])
    response: requests.Response = requests.get(f'{_url}/qiskit/experiments?{tags_list}')
    if response.status_code == 200:
        return response.json()
    else:
        raise ConnectionError(f"Error while fetching matching experiments by tags: {tags}. Detials: {response.text}.")


def execute_experiment(main_experiment: PreparedExperiment, execution_backend: IBMQBackend,
                       ibmq_config: Optional[dict] = None,
                       mitigation_experiment: Optional[PreparedExperiment] = None):

    key_exp = save_prepared_experiment(main_experiment)
    LOG.info(f'======> Experiment key={key_exp}')

    key_mitigation = None
    if mitigation_experiment:
        key_mitigation = save_prepared_experiment(mitigation_experiment)
        LOG.info(f'======> Mitigation key={key_mitigation}')

    try:
        if mitigation_experiment:
            run_experiment(key_mitigation, backend=execution_backend, ibmq_config=ibmq_config)
        run_experiment(key_exp, backend=execution_backend, ibmq_config=ibmq_config)
    except UserWarning as ex:
        LOG.error(ex)
        try:
            if mitigation_experiment:
                delete_experiment(key_mitigation)
            delete_experiment(key_exp)
        except ConnectionError:
            pass
        raise ex

    return key_exp, key_mitigation

