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
import os
from typing import Optional

from .models import FinishedExperiment

LOG = logging.getLogger(__name__)


def save(directory, experiment=None, simulation=None):
    # type: (str, Optional[FinishedExperiment], Optional[FinishedExperiment]) -> None

    if experiment is None and simulation is None:
        return

    file_id = experiment.external_id if experiment is not None else simulation.external_id
    file_id = file_id.replace('-', '_')

    LOG.info("Saving to %s/%s.py", directory, file_id)

    with open(os.path.join(directory, "import_" + file_id + ".py"), 'w') as file:
        content = {}

        if experiment is not None:
            content['experiment'] = experiment.to_dict()

        if simulation is not None:
            content['simulation'] = simulation.to_dict()

        # When printed out naively a lot of indentation is missing
        # it is nicer to have this.
        import pprint
        import io
        output = io.StringIO()
        pprint.pprint(content, stream=output)

        # As we have numpy arrays in the data, we need to import the function _code:`asarray` with the name `array`
        # It is a bit of a hack but makes it smooth afterwards.
        file.writelines(['from numpy import asarray as array\n', 'result = '])
        file.write(output.getvalue())


def load(directory: str, external_id: str):
    import importlib

    module = importlib.import_module(f'import_{external_id}', directory)
    result_var = getattr(module, 'result')
    del module

    return FinishedExperiment.from_dict(result_var.get('simulation', None)), FinishedExperiment.from_dict(result_var.get('experiment', None))
