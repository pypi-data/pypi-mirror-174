from typing import Dict, List, Optional, Any

from pyrasgo.schemas.offline import OfflineTransform

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

from pydantic import BaseModel, Field


class TransformArgumentCreate(BaseModel):
    name: str
    description: Optional[str]
    type: str
    is_optional: Optional[bool] = Field(alias="isOptional", default=False)

    class Config:
        allow_population_by_field_name = True


class TransformArgument(TransformArgumentCreate):
    pass


class TransformCreate(BaseModel):
    name: str
    type: Optional[str]
    source_code: str = Field(alias="sourceCode")
    description: Optional[str]
    arguments: Optional[List[TransformArgumentCreate]]
    tags: Optional[List[str]]
    context: Optional[Dict[str, Any]]
    dw_type: Optional[Literal["SNOWFLAKE", "BIGQUERY", "UNSET"]] = Field(alias="dwType")
    is_accelerator: Optional[bool] = Field(alias="isAccelerator", default=False)

    class Config:
        allow_population_by_field_name = True


class TransformUpdate(BaseModel):
    """
    Contract for updating a Transform
    """

    type: Optional[str]
    description: Optional[str]
    source_code: Optional[str] = Field(alias="sourceCode")
    arguments: Optional[List[TransformArgumentCreate]]
    tags: Optional[List[str]]
    context: Optional[Dict[str, Any]]
    dw_type: Optional[Literal["SNOWFLAKE", "BIGQUERY", "UNSET"]] = Field(alias="dwType")
    is_accelerator: Optional[bool] = Field(alias="isAccelerator")

    class Config:
        allow_population_by_field_name = True


class Transform(TransformCreate):
    id: Optional[int]
    arguments: Optional[List[TransformArgument]]

    def to_yaml(self) -> str:
        """
        Return a YAML representation of this Transform
        """
        return OfflineTransform(**self.__dict__).yaml()


class TransformExecute(BaseModel):
    transform_args: Dict[str, Any] = Field(alias='transformArgs')
    transform_id: int = Field(alias='transformId')

    class Config:
        allow_population_by_field_name = True
