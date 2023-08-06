from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict

from pydantic import BaseModel, Field

from pyrasgo.schemas import dataset_column as dataset_column_schemas
from pyrasgo.schemas import dw_table as dw_table_schemas


class DatasetSourceType(Enum):
    CSV = 'CSV'
    RASGO = 'RASGO'
    TABLE = 'TABLE'
    DATAFRAME = 'DATAFRAME'


class Dataset(BaseModel):
    """
    Contract to return from get by id endpoints
    """

    id: int
    name: str
    resource_key: str = Field(alias='resourceKey')
    description: Optional[str]
    category: Optional[str]
    is_source: Optional[bool] = Field(alias='isSource')

    owner_id: Optional[int] = Field(alias='ownerId')
    organization_id: Optional[int] = Field(alias='organizationId')
    dw_table_id: Optional[int] = Field(alias='dwTableId')
    dw_operation_set_id: Optional[int] = Field(alias='dwOperationSetId')

    columns: Optional[List[dataset_column_schemas.DatasetColumn]]
    dw_table: Optional[dw_table_schemas.DataTableWithColumns] = Field(alias='dataTable')
    fqtn: Optional[str]
    table_type: Optional[str] = Field(alias="tableType")
    consumer_count: int = Field(alias='consumerCount')

    attributes: Optional[Dict[str, str]]

    create_timestamp: Optional[datetime] = Field(alias='createTimestamp')
    create_author: Optional[int] = Field(alias='createdBy')
    update_timestamp: Optional[datetime] = Field(alias='updateTimestamp')
    update_author: Optional[int] = Field(alias='updatedBy')
    source_type: Optional[DatasetSourceType] = Field(alias='sourceType', default=DatasetSourceType.RASGO)

    class Config:
        allow_population_by_field_name = True
        use_enum_values = True


class DatasetBulk(BaseModel):
    """
    Contract to return from get list endpoints
    """

    id: int
    name: str
    resource_key: str = Field(alias='resourceKey')
    description: Optional[str]
    category: Optional[str]
    is_source: Optional[bool] = Field(alias='isSource')

    owner_id: Optional[int] = Field(alias='ownerId')
    organization_id: Optional[int] = Field(alias='organizationId')

    dw_table_id: Optional[int] = Field(alias='dwTableId')
    dw_table: Optional[dw_table_schemas.DataTable] = Field(alias='dataTable')
    fqtn: Optional[str]
    table_type: Optional[str] = Field(alias="tableType")

    dw_operation_set_id: Optional[int] = Field(alias='dwOperationSetId')
    dataset_dependencies: List[int] = Field(alias='datasetDependencies')

    column_count: Optional[int] = Field(alias='columnCount')
    consumer_count: Optional[int] = Field(alias='consumerCount')

    attributes: Optional[Dict[str, str]]

    create_timestamp: Optional[datetime] = Field(alias='createTimestamp')
    create_author: Optional[int] = Field(alias='createdBy')
    update_timestamp: Optional[datetime] = Field(alias='updateTimestamp')
    update_author: Optional[int] = Field(alias='updatedBy')
    source_type: Optional[DatasetSourceType] = Field(alias='sourceType', default=DatasetSourceType.RASGO)

    class Config:
        allow_population_by_field_name = True
        use_enum_values = True


class DatasetCreate(BaseModel):
    """
    Contract to accept in post endpoints
    """

    name: str
    resource_key: Optional[str] = Field(alias='resourceKey')
    description: Optional[str]
    dw_table_id: Optional[int] = Field(alias='dwTableId')
    dw_operation_set_id: Optional[int] = Field(alias='dwOperationSetId')
    attributes: Optional[Dict[str, str]]
    source_type: DatasetSourceType = Field(alias='sourceType', default=DatasetSourceType.RASGO)

    class Config:
        allow_population_by_field_name = True
        use_enum_values = True


class DatasetPublish(BaseModel):
    """
    Contract to accept in publish endpoints
    """

    resource_key: Optional[str] = Field(alis="resourceKey")
    operation_set_resource_key: str = Field(alias="operationSetResourceKey")
    terminal_operation_resource_key: Optional[str] = Field(alias='terminalOperationResourceKey')
    table_name: Optional[str] = Field(alias="tableName")
    table_type: Optional[str] = Field(alias="tableType", default="VIEW")
    source_type: Optional[DatasetSourceType] = Field(alias="sourceType", default=DatasetSourceType.RASGO)
    name: str
    description: Optional[str] = None
    attributes: Optional[Dict[str, str]] = None

    class Config:
        allow_population_by_field_name = True
        use_enum_values = True


class DatasetRePublish(BaseModel):
    """
    Contract to accept in re-publish endpoints
    """

    operation_set_resource_key: str = Field(alias="operationSetResourceKey")
    terminal_operation_resource_key: Optional[str] = Field(alias='terminalOperationResourceKey')
    table_type: Optional[str] = Field(alias="tableType", default="VIEW")
    source_type: Optional[DatasetSourceType] = Field(alias="sourceType", default=DatasetSourceType.RASGO)
    name: Optional[str] = None
    description: Optional[str] = None
    attributes: Optional[Dict[str, str]] = None

    class Config:
        allow_population_by_field_name = True
        use_enum_values = True


class DatasetUpdate(BaseModel):
    """
    Contract to accept in put endpoints
    """

    name: Optional[str]
    description: Optional[str]
    owner_id: Optional[int] = Field(alias='ownerId')
    attributes: Optional[dict]

    class Config:
        allow_population_by_field_name = True
