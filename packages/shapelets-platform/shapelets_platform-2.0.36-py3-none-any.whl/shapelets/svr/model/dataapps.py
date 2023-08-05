from pydantic import BaseModel
from typing import Optional, Set
from typing_extensions import Literal

DataAppField = Literal['name', 'version', 'description', 'creationDate', 'updateDate', 'spec', 'tags']
DataAppAllFields: Set[DataAppField] = set(['name', 'version', 'description', 'creationDate', 'updateDate', 'spec', 'tags'])


class DataAppProfile(BaseModel):
    name: str
    version: Optional[float]
    description: Optional[str] = None
    creationDate: Optional[int] = None
    updateDate: Optional[int] = None
    spec: Optional[str] = None
    tags: Optional[list] = None
