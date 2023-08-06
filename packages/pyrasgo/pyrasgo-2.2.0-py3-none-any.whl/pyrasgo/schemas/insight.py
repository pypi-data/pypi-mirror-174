from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class Insight(BaseModel):
    id: Optional[int]
    resource_key: Optional[str] = Field(alias='resourceKey')
    name: Optional[str]
    operation_set_resource_key: Optional[str] = Field(alias='operationSetResourceKey')
    transform_id: Optional[int] = Field(alias='transformId')
    transform_arguments: Optional[Dict[str, Any]] = Field(alias='transformArguments')
    operation_sql: Optional[str] = Field(alias='operationSQL')

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
