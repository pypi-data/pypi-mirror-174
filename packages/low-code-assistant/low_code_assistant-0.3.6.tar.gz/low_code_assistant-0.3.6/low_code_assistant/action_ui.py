import textwrap
from dataclasses import replace
from typing import Callable, List, Optional, Type, Union

import humanize
import reacton
import reacton.ipyvuetify as v
import solara as sol
from react_ipywidgets.core import Element
from solara.components.sql_code import SqlCode

from low_code_assistant import action
from low_code_assistant.load_dataset import LoadDataset

from .big_query import BigQueryPanel
from .domino_api import get_domino_api


@reacton.component
def OpenPanel(columns, on_action, fill=None):
    def on_file_name(file_name):
        on_action(action.ActionOpen(file_name))

    return LoadDataset(on_file_name=on_file_name)


@reacton.component
def FilterPanel(columns, dtypes, on_action, fill):
    state, set_state = reacton.use_state(fill)

    def make_action():
        on_action(state)

    with sol.Div().meta(ref="FilterPanel") as panel:
        with sol.Div():
            FilterPanelView(columns, dtypes, state, set_state)

        with v.CardActions():
            v.Spacer()
            sol.Button(
                "apply",
                color="primary",
                icon_name="mdi-check",
                disabled=not state.is_valid(),
                on_click=make_action,
            )
    return panel


def escape_special_chars(s):
    return s.replace("\n", "\\n").replace("\t", "\\t").replace("\r", "\\r") if s else s


def unescape_special_chars(s):
    return s.replace("\\n", "\n").replace("\\t", "\t").replace("\\r", "\r") if s else s


@reacton.component
def FilterPanelView(columns, dtypes, action_: action.ActionFilter, on_filter_action):
    with sol.Div().meta(ref="FilterPanel") as main:
        with v.Row():
            with v.Col():
                v.Select(label="Column", v_model=action_.col, items=columns, on_v_model=lambda v: on_filter_action(replace(action_, col=v, dtype=dtypes[v])))
            with v.Col():
                v.Select(
                    label="Operator",
                    v_model=action_.op,
                    items=["<", ">", "<=", ">=", "!=", "=="],
                    on_v_model=lambda v: on_filter_action(replace(action_, op=v)),
                )
            with v.Col():

                def is_float_or_nan(value):
                    if value == "nan":
                        return True
                    try:
                        float(value)
                        return True
                    except ValueError:
                        return False

                v.TextField(
                    label="Value",
                    v_model=escape_special_chars(action_.value),
                    on_v_model=lambda v: on_filter_action(replace(action_, value=unescape_special_chars(v))),
                    error_messages=['Invalid value, consider using "as string"']
                    if action_.value and not action_.is_string and not is_float_or_nan(action_.value)
                    else None,
                )
            with v.Col():
                v.Switch(label="as string", v_model=action_.is_string, on_v_model=lambda v: on_filter_action(replace(action_, is_string=v)))
        with v.Row():
            with v.Col(sm=4):
                v.TextField(label="New dataframe name", v_model=action_.df_var_out, on_v_model=lambda v: on_filter_action(replace(action_, df_var_out=v)))

    return main


@reacton.component
def SelectColumnsPanelView(columns, dtypes, action_: Union[action.ActionSelectColumns, action.ActionDropColumns], on_columns_action):
    with sol.Div().meta(ref="SelectColumnsPanel") as main:
        with v.Row():
            with v.Col():
                v.Select(
                    label="Columns",
                    v_model=action_.columns,
                    items=columns,
                    on_v_model=lambda v: on_columns_action(replace(action_, columns=v)),
                    multiple=True,
                    deletable_chips=True,
                )
        with v.Row():
            with v.Col():
                v.TextField(label="New dataframe name", v_model=action_.df_var_out, on_v_model=lambda v: on_columns_action(replace(action_, df_var_out=v)))
    return main


@reacton.component
def GroupByPanelView(columns, dtypes, action_: action.ActionGroupBy, on_group_by_action):
    with sol.Div().meta(ref="GroupByPanel") as main:
        with v.Row():
            with v.Col(sm=4):
                v.Select(
                    label="Columns to group by",
                    v_model=action_.columns,
                    items=columns,
                    on_v_model=lambda v: on_group_by_action(replace(action_, columns=v)),
                    multiple=True,
                    deletable_chips=True,
                )
            with v.Col(sm=8, class_="pa-0"):
                new_aggs = []
                i = 0
                agg_names = ["size", "sum", "mean", "min", "max"]
                # filter out empty entries
                aggs = action_.aggregations and [k for k in action_.aggregations if not all(el is None for el in k)]
                for col, agg in aggs or []:
                    with v.Row():
                        with v.Col():
                            colnew = sol.ui_dropdown("Column to aggregate", col, columns, key=f"col_{i}")
                        with v.Col():
                            aggnew = sol.ui_dropdown("Aggregator", agg, agg_names, key=f"agg_{i}")
                            new_aggs.append((colnew, aggnew))
                            i += -1

                with v.Row():
                    with v.Col():
                        col = sol.ui_dropdown("Column to aggregate", None, columns, key=f"col_{i}")
                    with v.Col():
                        agg_name = sol.ui_dropdown("Aggregator", None, agg_names, key=f"agg_{i}")
                        if col and agg_name:
                            new_aggs.append((col, agg_name))

                on_group_by_action(replace(action_, aggregations=new_aggs))
        with v.Row():
            with v.Col(sm=4):
                v.TextField(label="New dataframe name", v_model=action_.df_var_out, on_v_model=lambda v: on_group_by_action(replace(action_, df_var_out=v)))

    return main


@reacton.component
def DataSourcePanel(
    columns,
    visible,
    data_source: action.ActionDownloadDataSource = action.ActionDownloadDataSource(),
    on_data_source: Callable[[action.ActionDownloadDataSource], None] = lambda x: None,
):
    def set_name(value):
        on_data_source(replace(data_source, name=value, database=None, schema=None, table=None, project=None))

    def set_type_(value):
        on_data_source(replace(data_source, type_=value, region="default" if value == "BigQueryConfig" else None, use_query=False))

    def set_use_query(value):
        on_data_source(replace(data_source, use_query=value))

    def set_database(value):
        on_data_source(replace(data_source, database=value, schema=None, table=None))

    def set_schema(value):
        on_data_source(replace(data_source, schema=value, table=None))

    def set_table(value):
        on_data_source(replace(data_source, table=value))

    def set_query(value):
        on_data_source(replace(data_source, query=value))

    def set_sample(value):
        if value != data_source.sample:
            on_data_source(replace(data_source, sample=value))

    datasource_list_result: sol.Result = sol.use_thread(lambda _cancel: get_domino_api().get_datasource_list() if visible else None, [visible])

    def get_ds(name):
        if not name:
            return None
        from typing import TYPE_CHECKING

        from low_code_assistant.util import in_dev_mode

        if TYPE_CHECKING:
            from domino.data_sources import DataSourceClient
        else:
            if in_dev_mode():
                from low_code_assistant.domino_lab_mock import DataSourceClient
            else:
                from domino.data_sources import DataSourceClient

        return DataSourceClient().get_datasource(name)

    def get_tables(_cancel):
        if not data_source.name:
            return None, None
        ds = get_ds(data_source.name)
        set_type_(ds.datasource_type)

        if ds.datasource_type in ["S3Config", "GCSConfig", "BigQueryConfig"]:
            return None, ds
        if ds.datasource_type == "SnowflakeConfig":
            if ds.config.get("database"):
                res = ds.query(
                    """select
                    TABLE_CATALOG as "database_name",
                    TABLE_SCHEMA as "schema_name",
                    TABLE_NAME as "name",
                    ROW_COUNT as "rows"
                    from INFORMATION_SCHEMA.TABLES
                    where TABLE_SCHEMA != 'INFORMATION_SCHEMA'"""
                )
            else:
                res = ds.query("show tables")
            return res.to_pandas(), ds
        if ds.datasource_type == "RedshiftConfig":
            res = ds.query(
                textwrap.dedent(
                    """\
                select tab.table_schema as schema_name,
                       tab.table_name as name,
                       tinf.tbl_rows as rows
                from svv_tables tab
                         join svv_table_info tinf
                              on tab.table_schema = tinf.schema
                                  and tab.table_name = tinf.table
                where tab.table_type = 'BASE TABLE'
                  and tab.table_schema not in('pg_catalog','information_schema')
                  and tinf.tbl_rows > 1
                """
                )
            )
            return res.to_pandas(), ds
        raise RuntimeError(f"Unknown datasource: {ds.datasource_type}")

    tables_result: sol.Result = sol.hooks.use_thread(get_tables, [data_source.name])

    tables, ds = tables_result.value or (None, None)

    database_items = []
    schema_items = []
    table_items = []
    names = None
    rows = None

    if tables is not None and ds is not None:
        database_items = tables["database_name"].unique().tolist() if "database_name" in tables else [ds.config.get("database")]
        if data_source.database:
            if ds.datasource_type == "SnowflakeConfig":
                schema_items = tables.loc[tables["database_name"] == data_source.database]["schema_name"].unique().tolist()
            else:
                schema_items = tables["schema_name"].unique().tolist()
            if data_source.schema:
                names = tables.loc[tables["schema_name"] == data_source.schema]["name"].unique().tolist()
                rows = tables.loc[tables["schema_name"] == data_source.schema]["rows"].unique().tolist()
                table_items = [{"value": n, "text": f"{n} ({humanize.intword(r)} rows)"} for n, r in zip(names, rows)]

    def get_schema_spec(_cancel):
        if not (ds and data_source.database and data_source.schema):
            return None
        elif ds.datasource_type == "RedshiftConfig":
            return (
                ds.query(
                    textwrap.dedent(
                        f"""\
                select table_name, column_name
                from information_schema.columns
                where table_schema = '{data_source.schema}'
                and table_catalog = '{data_source.database}'
                order by table_name, ordinal_position
                """
                    )
                )
                .to_pandas()
                .groupby("table_name")["column_name"]
                .apply(list)
                .to_dict()
            )
        elif ds.datasource_type == "SnowflakeConfig":
            return (
                ds.query(f"SHOW COLUMNS IN SCHEMA {data_source.database}.{data_source.schema}")
                .to_pandas()
                .groupby("table_name")["column_name"]
                .apply(list)
                .to_dict()
            )

    spec_result: sol.Result = sol.hooks.use_thread(get_schema_spec, [ds and ds.datasource_type, data_source.database, data_source.schema])

    def get_s3_keys(_cancel) -> Optional[List]:
        if ds and ds.datasource_type in ["S3Config", "GCSConfig"]:
            res = ds.list_objects()
            return res
        else:
            return None

    s3_keys_result: sol.Result[Optional[List]] = sol.hooks.use_thread(get_s3_keys, [ds])

    def pre_select_database():
        if len(database_items) == 1 and database_items[0] != data_source.database:
            set_database(database_items[0])

    reacton.use_memo(pre_select_database, [database_items])

    def pre_selelect_schema():
        if len(schema_items) == 1 and schema_items[0] != data_source.schema:
            set_schema(schema_items[0])

    reacton.use_memo(pre_selelect_schema, [schema_items])

    def check_sample():
        if data_source.use_query:
            set_sample(False)
            return

        if tables is None:
            return

        name_index = not data_source.use_query and names and data_source.table and names.index(data_source.table)
        nr_rows = name_index is not None and rows and rows[name_index]

        set_sample(nr_rows and nr_rows > 3000)

    reacton.use_memo(check_sample, [data_source.table, data_source.use_query])

    def supported(ds_type):
        return ds_type in ["S3Config", "GCSConfig", "RedshiftConfig", "SnowflakeConfig", "BigQueryConfig"]

    def text(e):
        return f'{e["name"]} - {e["dataSourceType"].replace("Config", "")}{" - [not yet supported]" if not supported(e["dataSourceType"]) else ""}'

    with sol.Div() as main:
        with v.Row():
            with v.Col():
                if datasource_list_result.error:
                    sol.Error(str(datasource_list_result.error))
                else:
                    items = datasource_list_result.value and [
                        {
                            "text": text(e),
                            "value": e["name"],
                            "disabled": not supported(e["dataSourceType"]),
                        }
                        for e in datasource_list_result.value
                    ]  # type: ignore
                    v.Select(
                        label="Data Source",
                        # TODO: bug in vuetify wrappers
                        items=items,
                        v_model=data_source.name,
                        on_v_model=set_name,
                    )
        if data_source.name:
            if tables_result.error:
                error_msg = f"{type(tables_result.error).__name__}: {str(tables_result.error)}"
                if isinstance(tables_result.error, KeyError):
                    error_msg = (
                        error_msg
                        + ". This may be due to an environment with an incompatible version of the Domino-API-client (v"
                        + f"{get_domino_api().get_client_version()}) for this Domino version (v{get_domino_api().get_domino_version()})."
                    )
                sol.Warning(error_msg)
            elif not ds:
                v.ProgressLinear(indeterminate=True)
            elif ds.datasource_type in ["S3Config", "GCSConfig"]:
                if s3_keys_result.error:
                    sol.Warning(str(s3_keys_result.error))
                elif s3_keys_result.value is not None:
                    keys = [obj.key for obj in s3_keys_result.value]
                    with v.List():

                        def on_value(index):
                            on_data_source(replace(data_source, database=keys[index] if index is not None else None))

                        with v.ListItemGroup(v_model=keys.index(data_source.database) if data_source.database else None, on_v_model=on_value):
                            for key in keys:
                                with v.ListItem().key(key):
                                    with v.ListItemIcon():
                                        v.Icon(children=["mdi-file-document"])
                                    with v.ListItemContent():
                                        v.ListItemTitle(children=key)
                else:
                    v.ProgressLinear(indeterminate=True)
            elif ds.datasource_type in ["RedshiftConfig", "SnowflakeConfig"]:
                with v.Row():
                    with v.Col():
                        v.Select(label="Database", items=database_items, v_model=data_source.database, on_v_model=set_database)
                    with v.Col():
                        v.Select(label="Schema", items=schema_items, v_model=data_source.schema, on_v_model=set_schema)
                with v.Row():
                    with v.Col():
                        v.Switch(label="Use query", v_model=data_source.use_query, on_v_model=set_use_query)
                with v.Row():
                    if data_source.use_query:
                        with v.Col():
                            SqlCode(query=data_source.query, tables=spec_result.value, on_query=set_query)
                    else:
                        with v.Col():
                            v.Select(label="Table", items=table_items, v_model=data_source.table, on_v_model=set_table)
            elif ds.datasource_type == "BigQueryConfig":
                BigQueryPanel(ds=ds, data_source=data_source, on_data_source=on_data_source, on_sample=set_sample).key("bq" + data_source.name)
            if data_source.sample:
                with sol.Div(class_="ml-4"):
                    sol.Warning("This table has to many rows. A sample of this table will be loaded.")

    return main


@reacton.component
def TransformationPanel(columns, dtypes, action_: action.Action, on_action, on_action_type: Callable[[Type[action.Action]], None]):
    action_mapping = {
        action.ActionFilter: "Filter rows",
        action.ActionDropColumns: "Drop columns",
        action.ActionSelectColumns: "Select columns",
        action.ActionGroupBy: "Groupby and aggregate",
    }
    action_mapping_reverse = {val: k for k, val in action_mapping.items()}

    op = action_mapping[type(action_)]

    def get_panel():
        if isinstance(action_, action.ActionFilter):
            return FilterPanelView(columns, dtypes, action_, on_action).key("filter_rows")
        if isinstance(action_, action.ActionDropColumns):
            return SelectColumnsPanelView(columns, dtypes, action_, on_action).key("drop columns")
        if isinstance(action_, action.ActionSelectColumns):
            return SelectColumnsPanelView(columns, dtypes, action_, on_action).key("select columns")
        if isinstance(action_, action.ActionGroupBy):
            return GroupByPanelView(columns, dtypes, action_, on_action).key("group by")

    with v.Sheet() as main:
        v.Select(
            label="Transformation",
            v_model=op,
            items=list(action_mapping.values()),
            on_v_model=lambda v: on_action_type(action_mapping_reverse[v]),  # type: ignore
        )
        if op is not None:
            get_panel()

    return main


_ui_for_action = {
    action.ActionOpen: OpenPanel,
    action.ActionDownloadDataSource: DataSourcePanel,
    action.ActionFilter: FilterPanelView,
    action.ActionSelectColumns: SelectColumnsPanelView,
    action.ActionDropColumns: SelectColumnsPanelView,
    action.ActionGroupBy: GroupByPanelView,
}


@reacton.component
def EditAction(columns, dtypes, on_action, action_obj) -> Element:
    return _ui_for_action[action_obj.__class__](
        columns,
        dtypes,
        action_obj,
        on_action,
    )  # type: ignore
