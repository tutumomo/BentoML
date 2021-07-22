# ==============================================================================
#     Copyright (c) 2021 Atalaya Tech. Inc
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
# ==============================================================================

import os
import typing as t

from ._internal.artifacts import ModelArtifact
from ._internal.exceptions import MissingDependencyException
from ._internal.types import MetadataType, PathType


class H2oModel(ModelArtifact):
    """
    Model class for saving/loading :obj:`h2o` models using :meth:`~h2o.saved_model` and :meth:`~h2o.load_model`

    Args:
        model (`h2o.model.model_base.ModelBase`):
            :obj:`ModelBase` for all h2o model instance
        metadata (`Dict[str, Any]`,  `optional`, default to `None`):
            Class metadata

    Raises:
        MissingDependencyException:
            :obj:`h2o` is required by H2oModel

    Example usage under :code:`train.py`::

        TODO:

    One then can define :code:`bento_service.py`::

        TODO:

    Pack bundle under :code:`bento_packer.py`::

        TODO:
    """

    try:
        import h2o

        if t.TYPE_CHECKING:
            import h2o.model
    except ImportError:
        raise MissingDependencyException("h2o is required by H2oModel")

    def __init__(
        self,
        model: "h2o.model.model_base.ModelBase",
        metadata: t.Optional[MetadataType] = None,
    ):
        super(H2oModel, self).__init__(model, metadata=metadata)

    @classmethod
    def load(cls, path: PathType) -> "h2o.model.model_base.ModelBase":
        try:
            import h2o
        except ImportError:
            raise MissingDependencyException("h2o is required by H2oModel")
        h2o.init()
        h2o.no_progress()
        # NOTE: model_path should be the first item in
        #   h2o saved artifact directory
        model_path: str = str(os.path.join(path, os.listdir(path)[0]))
        return h2o.load_model(model_path)

    def save(self, path: PathType) -> None:
        try:
            import h2o
        except ImportError:
            raise MissingDependencyException("h2o is required by H2oModel")
        h2o.save_model(model=self._model, path=str(path), force=True)
