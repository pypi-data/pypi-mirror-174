from dataclasses import dataclass, replace
from typing import List, Optional

import humanize
import reacton
import reacton.ipyvuetify as v
import solara as sol
from solara.components.sql_code import SqlCode

from low_code_assistant import action


@dataclass(frozen=True)
class SchemasResult:
    default_region: Optional[str]
    schemas: List[str]


regions = [
    "default",
    "us",
    "eu",
    "us-central1",
    "us-west4",
    "us-west2",
    "northamerica-northeast1",
    "us-east4",
    "us-west1",
    "us-west3",
    "southamerica-east1",
    "southamerica-west1",
    "us-east1",
    "northamerica-northeast2",
    "europe-west1",
    "europe-north1",
    "europe-west3",
    "europe-west2",
    "europe-southwest1",
    "europe-west8",
    "europe-west4",
    "europe-west9",
    "europe-central2",
    "europe-west6",
    "asia-south2",
    "asia-east2",
    "asia-southeast2",
    "australia-southeast2",
    "asia-south1",
    "asia-northeast2",
    "asia-northeast3",
    "asia-southeast1",
    "australia-southeast1",
    "asia-east1",
    "asia-northeast1",
]

columns = ["table_schema", "table_name", "column_name"]


@reacton.component
def BigQueryPanel(ds, data_source: action.ActionDownloadDataSource, on_data_source, on_sample):
    project_temp, set_project_temp = sol.use_state_or_update(ds.config.get("project") or data_source.project)

    def set_project(v):
        on_data_source(replace(data_source, project=v, schema=None, table=None))

    def project():
        return ds.config.get("project") or data_source.project

    def set_region(v):
        on_data_source(replace(data_source, region=v, schema=None, table=None))

    def set_schema(v):
        on_data_source(replace(data_source, schema=v, table=None))

    def set_table(v):
        on_data_source(replace(data_source, table=v))

    def set_query(v):
        on_data_source(replace(data_source, query=v))

    def set_use_query(v):
        on_data_source(replace(data_source, use_query=v))

    def get_schemas(_cancel):
        if not project():
            return None
        if data_source.region == "default":
            schemas_and_location_df = ds.query(f"SELECT location, schema_name FROM `{project()}`.INFORMATION_SCHEMA.SCHEMATA").to_pandas()
            default_region = schemas_and_location_df["location"].tolist()[0]
            schemas = schemas_and_location_df["schema_name"].tolist()
            return SchemasResult(default_region, schemas)

        schema_df = ds.query(f"SELECT schema_name FROM `{project()}.region-{data_source.region}`.INFORMATION_SCHEMA.SCHEMATA").to_pandas()
        schemas = schema_df["schema_name"].tolist()
        return SchemasResult(None, schemas)

    schemas_result: sol.Result = sol.hooks.use_thread(get_schemas, [data_source.region, project()])

    def select_single_schema():
        if schemas_result.value and len(schemas_result.value.schemas) == 1:
            value = schemas_result.value.schemas[0]
            if value != data_source.schema:
                set_schema(value)

    reacton.use_memo(select_single_schema, [schemas_result.value and schemas_result.value.schemas])

    def get_tables(_cancel):
        if not data_source.schema or not schemas_result.value:
            return

        q = f"SELECT table_id, row_count, type FROM `{project()}.{data_source.schema}`.__TABLES__"
        table_df = ds.query(q).to_pandas()

        return [
            {
                "text": f'{item["table_id"]} ({humanize.intword(item["row_count"] if item["type"] == 1 else "-")}) rows',
                "value": item["table_id"],
                "rows": item["row_count"],
            }
            for item in table_df.to_dict("records")
        ]

    tables_result: sol.Result = sol.hooks.use_thread(get_tables, [data_source.region, project(), data_source.schema, schemas_result.value])

    def get_column_spec(_cancel):
        if not data_source.schema or not schemas_result.value:
            return
        return (
            ds.query(
                f"SELECT table_name, column_name FROM `{project()}.{data_source.schema}`.INFORMATION_SCHEMA.COLUMNS order by table_name, ordinal_position;"
            )
            .to_pandas()
            .groupby("table_name")["column_name"]
            .apply(list)
            .to_dict()
        )

    column_spec_result: sol.Result = sol.hooks.use_thread(get_column_spec, [data_source.schema, schemas_result.value])

    def check_sample():
        if data_source.use_query:
            on_sample(False)
            return

        if tables_result.value is None:
            return

        large_table = [item for item in tables_result.value if item["value"] == data_source.table and item["rows"] > 3000]
        on_sample(bool(large_table))

    reacton.use_memo(check_sample, [data_source.table, data_source.use_query])

    with v.Sheet() as main:
        with v.Row():
            with v.Col(style_="display: flex; align-items: center"):
                v.TextField(label="Project", v_model=project_temp, on_v_model=set_project_temp, disabled=bool(ds.config.get("project")))
                if not ds.config.get("project") and project() != project_temp:
                    sol.Button(
                        "apply", on_click=lambda: set_project(project_temp), icon_name="mdi-check", color="primary", small=True, class_="ml-2", outlined=True
                    )
            with v.Col():
                v.Select(label="region", items=regions, v_model=data_source.region, on_v_model=set_region)
            with v.Col():
                if schemas_result.value and schemas_result.value.schemas:
                    v.Select(label="Dataset", items=schemas_result.value.schemas, v_model=data_source.schema, on_v_model=set_schema).key("schema")
        if tables_result.value:
            with v.Row():
                with v.Col():
                    v.Switch(label="Use query", v_model=data_source.use_query, on_v_model=set_use_query)
            with v.Row():
                with v.Col():
                    if data_source.use_query:
                        if column_spec_result.value:
                            SqlCode(query=data_source.query, tables=column_spec_result.value, on_query=set_query)
                    else:
                        v.Select(label="Table", items=tables_result.value, v_model=data_source.table, on_v_model=set_table).key("table")

        if sol.ResultState.RUNNING in [schemas_result.state, tables_result.state, column_spec_result.state]:
            v.ProgressLinear(indeterminate=True).key("progress")
        if sol.ResultState.ERROR in [schemas_result.state, tables_result.state, column_spec_result.state]:
            sol.Warning(str(schemas_result.error or tables_result.error or column_spec_result.error))

    return main


# @reacton.component
# def Higher():
#     from domino.data_sources import DataSourceClient
#     name, set_name = reacton.use_state(None)
#     data_source, set_data_source = reacton.use_state(action.ActionDownloadDataSource())
#
#     def on_name():
#         if name:
#             ds = DataSourceClient().get_datasource(name)
#             set_data_source(action.ActionDownloadDataSource(data_source, name=name, type_=ds.datasource_type, region="default"))
#             return ds
#
#     ds = reacton.use_memo(on_name, [name])
#
#     with v.Sheet() as main:
#         v.Select(labels="source", v_model=name, on_v_model=set_name, items=["BigQuery-mario", "BigQuery-no_project"], clearable=True)
#
#         if ds:
#             BiqQueryPanel(ds, data_source, set_data_source).key("bq" + name)
#
#     return main
#
#
# Higher()
