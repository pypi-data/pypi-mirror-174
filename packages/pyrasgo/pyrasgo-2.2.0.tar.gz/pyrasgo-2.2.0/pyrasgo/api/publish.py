"""
API Publish Functions
"""
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from typing_extensions import Literal

import numpy as np
import pandas as pd

from pyrasgo import errors
from pyrasgo.primitives.dataset import Dataset
from pyrasgo.schemas.dataset import DatasetCreate, DatasetPublish, DatasetRePublish, DatasetSourceType
from pyrasgo.schemas.offline import OfflineDataset
from pyrasgo.utils import naming


class Publish:
    """
    API Publish Class
    """

    def __init__(self):
        from pyrasgo.api import Create, Get, Update
        from pyrasgo.api.connection import Connection
        from pyrasgo.config import get_session_api_key

        api_key = get_session_api_key()
        self.api = Connection(api_key=api_key)
        self.get = Get()
        self.create = Create()
        self.update = Update()
        self._dw = None

    @property
    def data_warehouse(self):
        from pyrasgo.storage import DataWarehouse, dw_connection

        if self._dw:
            return self._dw
        self._dw: DataWarehouse = dw_connection(self.api._dw_type())
        return self._dw

    def dataset(
        self,
        dataset: Dataset,
        name: str,
        resource_key: Optional[str] = None,
        description: Optional[str] = None,
        attributes: Optional[dict] = None,
        table_type: Optional[str] = "VIEW",
        table_name: Optional[str] = None,
        if_exists: str = "fail",
        verbose: bool = False,
        timeout: Optional[int] = None,
    ) -> Dataset:
        """
        Saves a transformed Dataset in Rasgo to published
        Args:
            dataset: Dataset to save
            name: Name of dataset
            resource_key: A table-safe key used to identify this dataset
            description: Description of dataset
            attributes: Dictionary with metadata about the Dataset
            table_type: Type of object to create in snowflake. Can be "TABLE" or "VIEW"
            table_name: Data Warehouse Table Name to set for this DS's published operation
            if_exists: Values('fail', 'overwrite') Instructions for how to proceed if an existing Dataset matches this resource_key
                If 'overwrite', Re-Publishes the existing Dataset with this draft
                If 'fail', raises a warning about the key conflict
            verbose: If true will print save progress status
            timeout: Approximate timeout in seconds. Raise an APIError if the dataset isn't available in x seconds
        Returns:
            Dataset
        """
        if verbose:
            print(f"Saving Dataset with name={name!r} description={description!r} resource_key={resource_key}...")

        # Fail if incoming dataset already exists in API
        if dataset._status in ("DRAFT DATASET", "PUBLISHED DATASET"):
            raise errors.RasgoRuleViolation(
                f"This Dataset already exists in Rasgo as resource_key {dataset.resource_key}. "
                "Transform the dataset to save it."
            )

        # Get or create the Operation Set so we can publish it
        elif dataset._status == "API DRAFT":
            dataset._refresh()
            operation_set = dataset._api_operation_set

        elif dataset._status == "OFFLINE DRAFT":
            operation_set = self.create._operation_set(
                operations=dataset._operations,
                dataset_dependency_ids=dataset._dataset_dependencies,
            )

        # Publish vs RePublish routing
        # If this user passes a resource_key check if it exists
        republish = False
        if resource_key:
            try:
                existing_ds = self.get.dataset(resource_key=resource_key)
            except errors.RasgoResourceException:
                existing_ds = None
            if existing_ds:
                if if_exists == "fail":
                    raise errors.DWResourceException(
                        f"A Dataset with resource_key {resource_key} already exists. "
                        "To create a new dataset, re-run with function without the resource_key param or pass in a unique key. "
                        "To overwrite this existing Dataset with your draft, re-run this function with param `if_exists='overwrite'`"
                    )
                elif if_exists == "overwrite":
                    republish = True
                else:
                    raise errors.ParameterValueError("if_exists", ["fail", "overwrite"])

        if republish:
            if verbose:
                print(f"RePublishing Dataset {resource_key}")
            dataset_contract = DatasetRePublish(
                operation_set_resource_key=operation_set.resource_key,
                terminal_operation_resource_key=operation_set.terminal_operation_resource_key,
                name=name,
                description=description,
                attributes=attributes,
                source_type=DatasetSourceType.RASGO,
                table_type=table_type,
            )
            ds = self.update._republish_dataset(
                resource_key=resource_key, dataset_contract=dataset_contract, verbose=verbose, timeout=timeout
            )
        else:
            if verbose:
                print("Publishing new Dataset")
            dataset_obj = DatasetPublish(
                resource_key=resource_key,
                operation_set_resource_key=operation_set.resource_key,
                terminal_operation_resource_key=operation_set.terminal_operation_resource_key,
                table_name=table_name,
                table_type=table_type,
                name=name,
                description=description,
                attributes=attributes,
                source_type=DatasetSourceType.RASGO,
            )
            ds = self.create._dataset_from_draft(dataset_contract=dataset_obj, timeout=timeout)
        if verbose:
            print(f"Dataset {ds.resource_key} saved")
        return Dataset(api_dataset=ds, api_operation_set=operation_set)

    def dataset_from_dict(
        self,
        dataset_dict: dict,
        if_exists: str = "fail",
        verbose: bool = False,
        timeout: int = None,
    ) -> Dataset:
        """
        Publish a new dataset based on a Rasgo-compliant dict

        Args:
            dataset_dict: a Rasgo-compliant json dict (converted from a yaml file)
            if_exists: Values('fail', 'overwrite') Instructions for how to proceed if an existing Dataset matches this resource_key
                If 'overwrite', Re-Publishes the existing Dataset with this draft
                If 'copy', create a new Dataset based on this draft
                If 'fail', raises a warning about the key conflict
            verbose: If true will print save progress status
            timeout: Approximate timeout in seconds. Raise an APIError if the dataset isn't available in x seconds

        To publish a dataset from a yaml file:
            with open(your_file_path, "r") as yaml_file:
                rasgo.publish.dataset_from_dict(yaml.safe_load(yaml_file))
        """
        try:
            dataset_instructions = OfflineDataset(**dataset_dict)
        except Exception as ex:
            raise errors.RasgoSchemaException("dataset_dict violates Rasgo-compliant format") from ex

        # Publish vs RePublish routing
        republish = False
        if dataset_instructions.resource_key:
            try:
                existing_ds = self.get.dataset(resource_key=dataset_instructions.resource_key)
            except errors.RasgoResourceException:
                existing_ds = None
            if existing_ds:
                if if_exists == "fail":
                    raise errors.DWResourceException(
                        f"A Dataset with resource_key {dataset_instructions.resource_key} already exists. "
                        "To create a new dataset, re-run with function without the resource_key param or pass in a unique key. "
                        "To overwrite this existing Dataset with your draft, re-run this function with param `if_exists='overwrite'`"
                    )
                if if_exists == "copy":
                    republish = False
                elif if_exists == "overwrite":
                    republish = True
                else:
                    raise errors.ParameterValueError("if_exists", ["fail", "overwrite", "copy"])

        if republish:
            if verbose:
                print(f"Republishing Dataset {dataset_instructions.resource_key} from this dict")
            return self.update._dataset_from_offline_schema(
                dataset_instructions=dataset_instructions, verbose=verbose, timeout=timeout
            )
        else:
            if verbose:
                print("Creating a new Dataset from this dict")
            return self.create._dataset_from_offline_schema(
                dataset_instructions=dataset_instructions, verbose=verbose, timeout=timeout
            )

    def dbt_project(
        self,
        datasets: List[Dataset],
        project_directory: Union[os.PathLike, str] = None,
        models_directory: Union[os.PathLike, str] = None,
        project_name: str = None,
        model_args: Dict[str, Any] = None,
        verbose: bool = False,
    ) -> str:
        """
        Exports all given datasets to Models in a dbt Project

        Params:
        `datasets`: List[Dataset]:
            list of Rasgo datasets to write to dbt as models
        `project_directory`: Path:
            directory to save project files to
            defaults to current working dir
        `models_directory`: Path:
            directory to save model files to
            defaults to project_directory/models
        `project_name`: str:
            name for this project
            defaults to organization name
        """
        from pyrasgo.primitives import DbtProject
        from pyrasgo.utils.dbt import dataset_to_model, dataset_to_source

        project_directory = Path(project_directory or os.getcwd())
        project_name = project_name or naming.cleanse_dbt_name(self.api._profile["organization"]["name"])
        models_directory = Path(models_directory or (project_directory / "models"))
        project = DbtProject(
            name=project_name,
            project_directory=project_directory,
            models_directory=models_directory,
            models=[dataset_to_model(ds) for ds in datasets if not ds.is_source],
            sources=[dataset_to_source(ds) for ds in datasets if ds.is_source],
            model_args=model_args,
        )
        return project.save_files(verbose=verbose)

    def df(
        self,
        df: pd.DataFrame = None,
        name: Optional[str] = None,
        resource_key: Optional[str] = None,
        description: Optional[str] = None,
        parents: Optional[List[Dataset]] = None,
        verbose: bool = False,
        attributes: Optional[dict] = None,
        fqtn: Optional[str] = None,
        if_exists: Optional[Literal["append", "overwrite", "fail"]] = "fail",
    ) -> Dataset:
        """
        Push a Pandas Dataframe a Data Warehouse table and register it as a Rasgo Dataset

        params:
            df: pandas DataFrame
            name: Optional name for the Dataset (if not provided a random string will be used)
            description: Optional description for this Rasgo Dataset
            parents: Set Parent Dataset dependencies for this df dataset. Input as list of dataset primitive objs.
            verbose: Print status statements to stdout while function executes if true
            attributes: Dictionary with metadata about the Dataset
            fqtn: Optional name for the target table (if not provided a random string will be used)
            if_exists: Values: ['fail', 'append', 'overwrite'] directs the function what to do if a FTQN is passed, and represents an existing Dataset
        return:
            Rasgo Dataset
        """
        # Make sure no incompatible dw dtypes in df uploading
        _raise_error_if_bad_df_dtypes(df)

        # Validate all parent ds Ids exist if passed
        # Calling rasgo.get.dataset(<id>) will raise error if doesn't
        parents = parents if parents else []
        parent_ids = [ds.id for ds in parents]
        for p_ds_id in parent_ids:
            self.get.dataset(p_ds_id)

        if_exists_vals = ["overwrite", "append", "fail"]
        if_exists = if_exists.lower()
        if if_exists not in if_exists_vals:
            raise errors.ParameterValueError("if_exists", if_exists_vals)

        if not resource_key:
            resource_key = naming.random_alias()
        target_database, target_schema, target_table = naming.parse_fqtn(
            fqtn or resource_key, self.api._default_dw_namespace()
        )
        target_fqtn = naming.make_fqtn(database=target_database, schema=target_schema, table=target_table)

        # Check for existing datasets matching FQTN
        ds = None
        try:
            ds = self.get.dataset(fqtn=target_fqtn)
            if ds and verbose:
                print(f"Found Dataset {ds.id} matching FQTN {target_fqtn}. Proceeding in {if_exists} mode.")
        except errors.RasgoResourceException:
            pass

        if ds and if_exists == "overwrite":
            # Users should only be able to overwrite datasets in their own organization
            if ds._api_dataset.organization_id != self.api._profile.get("organizationId"):
                raise errors.RasgoRuleViolation(
                    f"Dataset {ds.id} already exists. This API key does not have permission to replace it."
                )
        elif ds and if_exists == "fail":
            raise errors.ParameterValueError(
                message=f"FQTN {target_fqtn} already exists, and {if_exists} was passed for `if_exists`. "
                "Please confirm the FQTN or choose another value for `if_exists`"
            )

        # Write the df to the target table
        if verbose:
            verb = "Appending" if if_exists == "append" else "Writing"
            print(f"{verb} dataframe to target table {target_fqtn}")
        self.data_warehouse.write_dataframe_to_table(df, table_name=target_fqtn, method=if_exists)

        # Create dataset based on new table FQTN created from df
        if not ds:
            ds = self.table(
                fqtn=target_fqtn,
                name=name or target_fqtn,
                resource_key=resource_key,
                description=description,
                verbose=verbose,
                attributes=attributes,
                parents=parents,
                source_type=DatasetSourceType.DATAFRAME,
            )
        return ds

    def table(
        self,
        fqtn: str,
        name: Optional[str] = None,
        resource_key: Optional[str] = None,
        description: Optional[str] = None,
        parents: Optional[List[Dataset]] = None,
        verbose: bool = False,
        attributes: Optional[dict] = None,
        if_exists: Optional[Literal["return", "update", "fail"]] = "fail",
        timeout: Optional[int] = None,
        source_type: DatasetSourceType = DatasetSourceType.TABLE,
    ) -> Dataset:
        """
        Register an existing table as a Rasgo Dataset

        params:
            fqtn: The fully qualified table name of the table to register
            name: Optional name to apply to this Rasgo Dataset
            description: Optional description for this Rasgo Dataset
            parents: Set Parent Dataset dependencies for this table dataset. Input as list of dataset primitive objs.
            verbose: Print status statements to stdout while function executes if true
            attributes: Dictionary with metadata about the Dataset
            timeout: Approximate timeout for creating the table in seconds. Raise an APIError if the reached
            source_type: Specifies the `source_type` of this Dataset in Rasgo. Defaults to 'TABLE'
        return:
            Rasgo Dataset
        """
        # Validate all parent ds Ids exist if passed
        # Calling rasgo.get.dataset(<id>) will raise error if doesn't
        parents = parents if parents else []
        parent_ids = [ds.id for ds in parents]
        for p_ds_id in parent_ids:
            self.get.dataset(p_ds_id)

        if verbose:
            print(f"Publishing {source_type.value} {fqtn} as Rasgo dataset")

        if fqtn.count(".") != 2:
            raise errors.ParameterValueError(
                message=f"'{fqtn}' is not a valid fully qualified table name. "
                "FQTNs should follow the format DATABASE.SCHEMA.TABLE_NAME.  "
                "Please pass a valid FQTN and try again"
            )

        table_database, table_schema, table_name = naming.parse_fqtn(fqtn)

        try:
            row_count = self.data_warehouse.query_into_dict(
                f"select count(1) as ROW_CT from {table_database}.{table_schema}.{table_name}"
            )
            if row_count[0]["ROW_CT"] == 0:
                raise errors.DWResourceException(
                    f"Source table {table_name} is empty or this role does not have access to it."
                )
        except Exception as err:
            raise errors.DWResourceException(
                f"Source table {table_name} does not exist or this role does not have access to it."
            ) from err

        # Make sure `source_type` param is valid Enum Value
        if not isinstance(source_type, DatasetSourceType):
            raise errors.ParameterValueError("source_type", ["CSV", "RASGO", "TABLE", "DATAFRAME"])

        # Check if a Dataset already exists
        existing_ds = None
        try:
            existing_ds = self.get.dataset(fqtn=fqtn)
        except errors.RasgoResourceException:
            pass
        if existing_ds:
            if if_exists == "return":
                return existing_ds
            elif if_exists == "update":
                dataset = self.update.dataset(
                    dataset=existing_ds,
                    name=name or table_name,
                    description=description,
                    attributes=attributes,
                )
                return Dataset(api_dataset=dataset)
            else:  # if_exists == "fail":
                raise errors.RasgoResourceException(
                    f"{fqtn} is already registered with Rasgo as Dataset {existing_ds.id}"
                )

        # Create operation set with parent dependencies
        # set for this dataset
        operation_set = self.create._operation_set(
            operations=[],
            dataset_dependency_ids=parent_ids,
            async_compute=False,
        )

        # Publish Dataset with operation set created above
        dataset = self.create._dataset_from_table(
            fqtn=fqtn,
            dataset_contract=DatasetCreate(
                name=name or table_name,
                resource_key=resource_key,
                dw_operation_set=operation_set.id,
                source_type=source_type.value,
                description=description,
                attributes=attributes,
            ),
            timeout=timeout,
        )
        # Raise API error if backend error creating dataset
        if not dataset:
            raise errors.APIError("DataSource failed to upload")

        # Return dataset if no error
        return Dataset(api_dataset=dataset)


# ------------------------------------------
#  Private Helper Funcs for Publish Class
# ------------------------------------------


def _raise_error_if_bad_df_dtypes(df: pd.DataFrame) -> None:
    """
    Raise an API error is any dtypes in the pandas dataframe,
    which are being pushed to the data warehouse aren't compatible.

    Raise proper error message if so
    """
    for col_name in df:
        col = df[col_name]
        if col.dtype.type == np.datetime64:
            raise errors.RasgoRuleViolation(
                "Can't publish pandas Df to Rasgo. Df column "
                f"'{col_name}' needs to be converted to proper datetime format.\n\n"
                "If your column is a **DATE** use `pd.to_datetime(df[<col_name>]).dt.date` to convert it\n"
                "If your column is a **TIMESTAMP** use `pd.to_datetime(final_df['col_name']).dt.tz_localize('UTC')`"
            )
