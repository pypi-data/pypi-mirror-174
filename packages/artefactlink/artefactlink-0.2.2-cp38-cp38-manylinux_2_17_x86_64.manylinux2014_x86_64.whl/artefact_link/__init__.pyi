import pathlib
from typing import List, Dict, Union, Optional


class LocalArtefactRegistry:
    path: Optional[pathlib.Path]

    def __init__(self, path: Optional[pathlib.Path]) -> None:
        self.path = path


class LocalEndpoint:
    def __init__(self, registry_endpoint: LocalArtefactRegistry, storage_location: Optional[pathlib.Path]) -> None:
        ...


class ShareableAIEndpoint:
    def __init__(self, api_key: str) -> None:
        ...


ArtefactEndpoint = Union[LocalEndpoint, ShareableAIEndpoint]


class PyID:
    """
    Artefact or Artefact Set ID - readable in Python
    """

    def as_string(self) -> str: ...

    def as_hex_string(self) -> str: ...


class PyModelID:
    name: str
    vcs_hash: str
    artefact_schema_id: PyID

    def __init__(self, name: str, vcs_hash: str, artefact_set_id: PyID) -> None: ...


class PyArtefact:
    """
    Data Backing for a Python-Compatible Artefact
    """

    def id(self) -> PyID:
        ...

    def path(self, temp_dir: pathlib.Path) -> pathlib.Path: ...

    """
       Retrieve or create a local path containing the Model Artefact
    """


class ModelData:
    """
    Model Data Representation for Save/Load
    """

    def __init__(
            self,
            name: str,
            vcs_hash: str,
            local_artefacts: List[LocalArtefactPath],
            children: Dict[str, PyModelID],
    ):
        """Create a Model Data Representation
        Args:
            name: Model Name
            vcs_hash: The Version Control System hash for the file
            local_artefacts: Paths for artefacts on the local system
            remote_artefacts: Paths for artefacts on remote systems
            children: Model IDs for Model Children
        """
        ...

    def dumps(
            self, endpoint: ArtefactEndpoint
    ) -> PyModelID: ...

    @property
    def model_id(self) -> PyModelID: ...

    @property
    def child_ids(self) -> dict[str, PyModelID]: ...

    def artefact_by_slot(self, slot: str) -> PyArtefact: ...

    def child_id_by_slot(self, slot: str) -> PyModelID: ...


class LocalArtefactPath:
    """
    Local Artefact - referenced by absolute path
    """

    def __init__(self, slot: str, path: str) -> None: ...



def load_model_data(
        model_name: str,
        vcs_hash: str,
        artefact_schema_id: PyID,
        endpoint: ArtefactEndpoint
) -> ModelData:
    """
    Load Model Data from Model Identifiers

    Requests the Model Data from the remote SQL server, and the Artefact Data from the remote Storage server.

    The model info and artefact data is copied to the local sql server and storage server respectively,
    and then artefacts are provided to the caller. The artefacts are presented with the OnDisk data backing,
    giving the most flexibility in terms of use. It is entirely possible to instead present Remote links to the
    end user, but this means consuming a stream each time the data must be checked, and assuming that the remote
    connection remains valid after the object is returned, which cannot be guaranteed.

    :param model_name: Name of the Model
    :param vcs_hash: Version Control Hash ID
    :param artefact_schema_id: ID representing the saved Artefacts and their layout in the model
    :param endpoint: Connection Options

    """
    ...
