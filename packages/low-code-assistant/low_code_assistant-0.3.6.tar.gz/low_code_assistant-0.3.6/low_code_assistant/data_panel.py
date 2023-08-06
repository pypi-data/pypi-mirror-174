import dataclasses
import sys
from dataclasses import field, replace
from pathlib import Path
from typing import Callable, Dict, Optional, Union

import plotly
import reacton
import reacton.ipyvuetify as v
import solara
from solara.components.file_browser import FileBrowser
from solara.components.file_drop import FileDrop

import low_code_assistant
from low_code_assistant.action import ActionDownloadDataSource
from low_code_assistant.action_ui import DataSourcePanel

from . import settings
from .assistant import mixpanel
from .domino_api import get_domino_api

supported_extensions = [
    "csv",
    "excel",
    "feather",
    "fwf",
    "gbq",
    "hdf",
    "html",
    "json",
    "orc",
    "parquet",
    "pickle",
    "sas",
    "spss",
    "sql",
    "sql_query",
    "sql_table",
    "stata",
    "table",
    "xml",
    "nocode",
]


def is_supported_extension(file):
    if file is None:
        return False
    lower = file.lower()
    return any([lower.endswith(ext) for ext in supported_extensions])


options = [x for x in dir(plotly.data) if not x.startswith("_")] + [x for x in dir(low_code_assistant.data) if not x.startswith("_")]


@dataclasses.dataclass(frozen=True)
class DataPanelState:
    tab: int = 0
    data_source: ActionDownloadDataSource = ActionDownloadDataSource()
    dataset_dir: Path = field(default_factory=lambda: Path(settings.settings.domino_datasets_dir))
    dataset_file: Optional[str] = None
    project_dir: Path = field(default_factory=lambda: Path(settings.settings.domino_working_dir))
    project_file: Optional[str] = None
    upload_file: Optional[Dict] = None
    demo_df_name: str = options[0]
    df_out: str = "df"
    reactive: bool = False

    def valid(self):
        if self.tab == 0:
            if self.data_source and self.data_source.type_ in ["S3Config", "GCSConfig"] and self.data_source.database:
                return True
            elif self.data_source.type_ == "BigQueryConfig":
                return bool(self.data_source and (self.data_source.query if self.data_source.use_query else self.data_source.schema and self.data_source.table))
            else:
                return bool(
                    self.data_source and (self.data_source.query if self.data_source.use_query else self.data_source.database and self.data_source.table)
                )
        if self.tab == 1:
            return bool(self.dataset_file)
        if self.tab == 2:
            return bool(self.project_file)
        if self.tab == 3:
            return bool(self.upload_file)
        if self.tab == 4:
            return True


@reacton.component
def DataPanel(state: DataPanelState, on_state: Callable[[Union[DataPanelState, Callable[[DataPanelState], DataPanelState]]], None]):
    progress, set_progress = reacton.use_state(0, key="progress")

    def on_tab():
        tabs = ["'Data Sources'", "'Datasets'", "'Project Files'", "'Uploads'", "'Demo'"]
        mixpanel.api.track_with_defaults(
            "interaction",
            {
                "section": "load_data",
                "type": "select tab",
                "tab": tabs[state.tab],
            },
        )

    reacton.use_memo(on_tab, [state.tab])

    with solara.Div(style_="max-width: 700px; max-width: 700px") as main:
        with v.Tabs(v_model=state.tab, on_v_model=lambda tab: on_state(replace(state, tab=tab))):
            v.Tab(children=["Data Sources"])
            if state.dataset_dir.exists():
                v.Tab(children=["Datasets"])
            v.Tab(children=["Project Files"])
            v.Tab(children=["Upload"])
            v.Tab(children=["Demo data"])
            with v.TabItem():
                version = get_domino_api().get_domino_version()
                if not (version.startswith("5") or version.startswith("0")):
                    solara.Div(children=["Data Sources are not available in Domino 4.x and earlier."], class_="ma-4")
                elif sys.version_info.minor == 6:
                    solara.Div(children=["Data Sources are not available in Python 3.6."], class_="ma-4")
                else:
                    DataSourcePanel(
                        columns=None,
                        visible=state.tab == 0,
                        data_source=state.data_source,
                        on_data_source=lambda ds: on_state(lambda state: replace(state, data_source=ds)),
                    )
            if state.dataset_dir.exists():
                with v.TabItem():
                    with solara.Div(style_="height: calc(100vh - 166px); padding-bottom: 0px; overflow: hidden; display: flex; flex-direction: column;"):
                        solara.Div(class_="my-4", children=[f"Select a file with one of the following extensions: {', '.join(supported_extensions)}"])
                        with solara.Div(style_="display: flex; flex-direction: column; flex-grow: 1; overflow: hidden;"):
                            with solara.Div(style_="flex-grow: 1; overflow: hidden;"):
                                FileBrowser(
                                    directory=state.dataset_dir,
                                    on_directory_change=lambda x: on_state(replace(state, dataset_dir=x, dataset_file=None)),
                                    on_file_name=lambda fn: on_state(replace(state, dataset_file=fn)),
                                ).key("DatasetsFileBrowser").meta(ref="datasets")
                            v.Switch(label="reactive", v_model=state.reactive, on_v_model=lambda x: on_state(replace(state, reactive=x)))
            with v.TabItem():
                with solara.Div(
                    style_="height: calc(100vh - 166px); overflow: auto; padding-bottom: 0px; overflow: hidden; display: flex; flex-direction: column;"
                ):
                    solara.Div(class_="my-4", children=[f"Select a file with one of the following extensions: {', '.join(supported_extensions)}"])
                    with solara.Div(style_="display: flex; flex-direction: column; flex-grow: 1; overflow: hidden;"):
                        FileBrowser(
                            directory=state.project_dir,
                            on_directory_change=lambda x: on_state(replace(state, project_dir=x, project_file=None)),
                            on_file_name=lambda fn: on_state(replace(state, project_file=fn)),
                        ).key("ProjectFileBrowser").meta(ref="project")
                        v.Switch(label="reactive", v_model=state.reactive, on_v_model=lambda x: on_state(replace(state, reactive=x)))
            with v.TabItem():
                solara.Div(class_="my-4", children=[f"Drag a file with one of the following extensions: {', '.join(supported_extensions)}"])
                FileDrop(
                    label="Drop dataset here",
                    on_total_progress=set_progress,
                    on_file=lambda file: on_state(replace(state, upload_file=file)),
                )
                v.ProgressLinear(value=progress)
                v.Switch(label="reactive", v_model=state.reactive, on_v_model=lambda x: on_state(replace(state, reactive=x)))
            with v.TabItem():
                with v.List():
                    with v.ListItemGroup(
                        v_model=state.demo_df_name,
                        on_v_model=lambda item: on_state(lambda state: replace(state, demo_df_name=item)),
                        color="primary",
                        mandatory=True,
                    ):
                        for item in options:
                            with v.ListItem(value=item).key(item):
                                with v.ListItemContent():
                                    v.ListItemTitle(children=[item])
                v.Switch(label="reactive", v_model=state.reactive, on_v_model=lambda x: on_state(replace(state, reactive=x)))

    return main
