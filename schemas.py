from typing import List, Optional
from pydantic import BaseModel

class TagBase(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class AssetBase(BaseModel):
    id: int
    name: str
    file_path: str
    asset_type: str
    tags: List[TagBase] = []

    class Config:
        from_attributes = True
