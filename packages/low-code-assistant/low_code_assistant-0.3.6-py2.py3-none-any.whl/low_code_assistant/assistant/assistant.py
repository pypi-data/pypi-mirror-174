import json
import os
import sys
import textwrap
from dataclasses import replace
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, cast

import ipyvuetify as vy
import ipywidgets
import pandas as pd
import plotly
import reacton
import reacton.ipyvuetify as v
import solara as sol
import traitlets
from pandas.core.frame import DataFrame

import low_code_assistant.actions_store as actions_store
import low_code_assistant.util
import low_code_assistant.viz_reducer as vr
from low_code_assistant import __version__, action, app, css, plot_builder, util
from low_code_assistant.assistant import drawer, handle_user_install, mixpanel, notebook
from low_code_assistant.data_panel import DataPanel, DataPanelState
from low_code_assistant.deployer import Deployer
from low_code_assistant.dominocode import TransformationsPanel
from low_code_assistant.hooks import use_reducer_addon
from low_code_assistant.layout import CardGridLayoutBuilder
from low_code_assistant.settings import settings
from low_code_assistant.snippets import snippets, snippets_ui
from low_code_assistant.snippets.snippets import (
    EDIT_SNIPPET_PREFIX,
    Snippet,
    save_snippet,
)
from low_code_assistant.util import DominoHeader, generate_var_name, get_vars, nb_locals

server_software = os.environ.get("SERVER_SOFTWARE", "")
if server_software.lower().startswith("solara"):
    import nbformat

    nb: nbformat.NotebookNode = nbformat.read(settings.domino_notebook_deploy_filename, 4)
    notebook.markdown_cells = {cell["id"]: cell["source"] for cell in nb.cells if cell["cell_type"] == "markdown"}


class AssistantWidget(vy.VuetifyTemplate):
    template_file = (__file__, "assistant.vue")

    menu = traitlets.Any().tag(sync=True, **ipywidgets.widget_serialization)
    cell_id = traitlets.Any().tag(sync=True)
    code = traitlets.Dict(allow_none=True).tag(sync=True)
    code_up = traitlets.Dict(allow_none=True).tag(sync=True)
    notebook_path = traitlets.Unicode(allow_none=True).tag(sync=True)
    save_counter = traitlets.Int(0).tag(sync=True)
    markdown_cells = traitlets.Dict(allow_none=True).tag(sync=True)
    snippet_prefix = traitlets.Unicode(EDIT_SNIPPET_PREFIX).tag(sync=True)
    snippet_saved_snackbar = traitlets.Bool(False).tag(sync=True)
    snippet_saved_count = traitlets.Int(0).tag(sync=True)
    snippet_edit_mode = traitlets.Bool(False).tag(sync=True)
    snippet_add_dialog_open = traitlets.Bool(False).tag(sync=True)
    snippet_add_header = traitlets.Unicode(allow_none=True).tag(sync=True)
    in_user_install_mode = traitlets.Bool(handle_user_install.in_user_install_mode()).tag(sync=True)
    version = traitlets.Unicode(__version__).tag(sync=True)

    def __init__(self, *args, **kwargs):
        self._on_saved: Optional[Callable[[bool], None]] = None
        super().__init__(*args, **kwargs)
        notebook.save_notebook = self.save_notebook

    def save_notebook(self, on_saved: Callable[[bool], None]):
        self._on_saved = on_saved
        self.send({"method": "save_notebook", "args": []})
        self.save_counter += 1

    def vue_notebook_saved(self, result):
        self._on_saved and self._on_saved(result)
        self._on_saved = None

    def vue_save_snippet(self, code):
        save_snippet(code)
        self.snippet_saved_count += 1


class MenuWidget(vy.VuetifyTemplate):
    template_file = (__file__, "menu.vue")

    logo = traitlets.Unicode(util.logo).tag(sync=True)
    items = traitlets.List(default_value=[]).tag(sync=True)
    selected = traitlets.Dict(allow_none=True).tag(sync=True)
    snippet_edit_mode = traitlets.Bool(False).tag(sync=True)
    overlay_open = traitlets.Bool().tag(sync=True)


items = [
    {
        "title": "Load data",
        "icon": "mdi-cloud-upload-outline",
        "action": "load_data",
    },
    {
        "title": "Transformations",
        "icon": "mdi-function-variant",
        "action": "transformations",
    },
    {
        "title": "Visualizations",
        "icon": "mdi-chart-bar-stacked",
        "action": "visualizations",
    },
    {
        "title": "App",
        "icon": "mdi-apps",
        "action": "app",
    },
    {
        "title": "Deploy",
        "icon": "mdi-rocket",
        "action": "deploy",
        "divider": True,
    },
    {
        "title": "Enter text",
        "icon": "mdi-text",
        "action": "markdown",
    },
    {
        "title": "Insert snippet",
        "icon": "mdi-card-text-outline",
        "action": "snippets",
    },
]


@reacton.component
def Menu(selected, on_selected, decoded, snippet_edit_mode, on_snippet_edit_mode):
    menu_action = None
    if decoded and decoded.__class__ in [action.ActionOpen, action.ActionDownloadDataSource, action.ActionDemo]:
        menu_action = "load_data"
    elif decoded and isinstance(decoded, actions_store.ActionsState):
        menu_action = "transformations"
    elif decoded and type(decoded) == vr.PlotState:
        menu_action = "visualizations"
    elif decoded and "type_card_grid_layout" in decoded:
        menu_action = "app"
    elif decoded and "markdown" in decoded:
        menu_action = "markdown"

    overlay_open, set_overlay_open = reacton.use_state(False)

    def close_overlay():
        set_overlay_open(False)

    # note: use_effect is used here over use_memo, so the overlay is closed last
    reacton.use_effect(close_overlay, [selected])

    return MenuWidget.element(
        items=[{"icon": "mdi-pencil", "title": "Edit", "action": menu_action, "edit": True}, *items] if decoded else items,
        selected=selected,
        on_selected=lambda v: v and on_selected(v),
        snippet_edit_mode=snippet_edit_mode,
        on_snippet_edit_mode=on_snippet_edit_mode,
        overlay_open=overlay_open,
        on_overlay_open=set_overlay_open,
    )


class AEncoder(json.JSONEncoder):
    def default(self, obj):
        encoded = action.to_json(obj)
        if not encoded:
            encoded = actions_store.to_json(obj)
        if not encoded:
            encoded = vr.to_json(obj)
        return encoded if encoded else json.JSONEncoder.default(self, obj)


def from_json(dct):
    decoded = action.from_json(dct)
    if not decoded:
        decoded = actions_store.from_json(dct)
    if not decoded:
        decoded = vr.from_json(dct)
    return decoded if decoded else dct


def dumps(value):
    return json.dumps(value, cls=AEncoder)


def loads(str):
    data = json.loads(str, object_hook=from_json)
    # convert previously stored action list to action state
    if type(data) == list and len(data) > 0 and isinstance(data[0], action.Action):
        data = actions_store.ActionsState(preview=True, actions=data)
    return data


@reacton.component
def MarkdownPanel(edit_action, set_code, open, edit, on_close):
    def on_apply():
        mixpanel.api.track_with_defaults(
            "inserted code",
            {
                "section": "Enter markdown",
            },
        )
        set_code(
            {
                "code": markdown_text,
                "meta": {},
                "type_": "markdown",
            }
        )
        on_close()

    markdown_text, set_markdown_text = reacton.use_state("")

    def update_markdown():
        if open and edit and edit_action and "markdown" in edit_action:
            set_markdown_text(edit_action["markdown"])
        else:
            set_markdown_text("")

    reacton.use_memo(update_markdown, [edit_action, edit])

    with drawer.RightDrawer(
        open=open,
        on_open=lambda v: on_close() if not v else None,
        title="Markdown",
        edit=bool(edit),
        on_apply=on_apply,
    ) as main:
        with sol.Div(class_="markdown-drawer", style_="min-width: 800px; max-width: 800px"):
            if open:
                sol.MarkdownEditor(markdown_text, on_value=set_markdown_text)
    return main


@reacton.component
def LoadPanel(edit_action, set_code, open, edit, on_close):
    data_panel_state, set_data_panel_state = reacton.use_state(DataPanelState())

    def reset_data():
        if not open:
            set_data_panel_state(DataPanelState())

    reacton.use_memo(reset_data, [open])

    def set_action(new_action):
        data_type = None
        data_source_type = None
        if isinstance(new_action, action.ActionOpen):
            if (new_action.filename or "").startswith(settings.domino_datasets_dir):
                data_type = "dataset"
            else:
                data_type = "file"
        elif isinstance(new_action, action.ActionDownloadDataSource):
            data_type = "data source"
            data_source_type = new_action.type_ or ""
        elif isinstance(new_action, action.ActionDemo):
            data_type = "demo"
        mixpanel.api.track_with_defaults(
            "inserted code",
            {
                "section": "load_data",
                "data_type": data_type,
                **({"data_source_type": data_source_type} if data_source_type else {}),
            },
        )
        set_code({"code": new_action.render_code("df") + f"\n{new_action.df_var_out}", "meta": dumps(new_action)})
        on_close()

    def on_file_name(filename: str, df_var: str, reactive: bool):
        set_action(action.ActionOpen(filename=filename, df_var_out=df_var, reactive=reactive))

    def on_apply():
        if data_panel_state.tab == 0:
            set_action(replace(data_panel_state.data_source, df_var_out=data_panel_state.df_out))
        elif data_panel_state.tab == 1 and data_panel_state.dataset_file:
            on_file_name(data_panel_state.dataset_file, data_panel_state.df_out, data_panel_state.reactive)
        elif data_panel_state.tab == 2 and data_panel_state.project_file:
            on_file_name(data_panel_state.project_file, data_panel_state.df_out, data_panel_state.reactive)
        elif data_panel_state.tab == 3 and data_panel_state.upload_file:
            dest_name = util.copy_upload(data_panel_state.upload_file["file_obj"], data_panel_state.upload_file["name"])
            on_file_name(dest_name, data_panel_state.df_out, data_panel_state.reactive)
        elif data_panel_state.tab == 4:
            set_action(action.ActionDemo(df_name=data_panel_state.demo_df_name, df_var_out=data_panel_state.df_out, reactive=data_panel_state.reactive))

    def set_edit():
        if open and edit:
            if isinstance(edit_action, action.ActionOpen):
                filename = cast(action.ActionOpen, edit_action).filename
                if filename is None:
                    set_data_panel_state(replace(data_panel_state, tab=0, df_out=edit_action.df_var_out))
                elif "low_code_assistant_data" in filename:
                    set_data_panel_state(replace(data_panel_state, tab=3, df_out=edit_action.df_var_out))
                elif filename.startswith(settings.domino_datasets_dir):
                    set_data_panel_state(
                        lambda data_panel_state: replace(
                            data_panel_state, tab=1, dataset_dir=Path(filename or "mypy").parent, df_out=edit_action.df_var_out, reactive=edit_action.reactive
                        )
                    )
                else:
                    set_data_panel_state(
                        replace(data_panel_state, tab=2, project_dir=Path(filename).parent, df_out=edit_action.df_var_out, reactive=edit_action.reactive)
                    )
            elif isinstance(edit_action, action.ActionDownloadDataSource):
                set_data_panel_state(replace(data_panel_state, tab=0, data_source=edit_action, df_out=edit_action.df_var_out))
            elif isinstance(edit_action, action.ActionDemo):
                set_data_panel_state(replace(data_panel_state, tab=4, demo_df_name=edit_action.df_name, df_out=edit_action.df_var_out))

    reacton.use_memo(set_edit, [open, edit, edit_action])

    with drawer.RightDrawer(
        open=open,
        on_open=lambda v: on_close() if not v else None,
        title="Load data",
        edit=bool(edit),
        apply_disabled=not data_panel_state.valid(),
        on_apply=on_apply,
        show_var_out=True,
        var_out=data_panel_state.df_out,
        on_var_out=lambda v: set_data_panel_state(lambda data_panel_state: replace(data_panel_state, df_out=v)),
    ) as main:
        if open:
            DataPanel(data_panel_state, set_data_panel_state)

    return main


@reacton.component
def TransformationPanel(action_state, set_code, dfs, open, edit, on_close):
    state, set_state = sol.use_state_or_update(action_state if open and edit and action_state else actions_store.ActionsState(preview=True))
    dispatch = use_reducer_addon(actions_store.actions_reducer, set_state)
    df_var_name, set_df_var_name = reacton.use_state(cast(Optional[str], (state.actions and state.actions[0] and state.actions[0].var_name) or None))

    actions_store.use_execute_df(state, set_state, nb_locals)

    def set_transformations():
        code_str = action.render_code(action.render_code_chunks(state.actions))
        set_code({"code": code_str, "meta": dumps(state)})
        mixpanel.api.track_with_defaults("inserted code", {"section": "transformations"})
        close()

    def close():
        set_df_var_name(None)
        set_state(actions_store.ActionsState(preview=True))
        on_close()

    def on_df_var_change():
        if df_var_name and not state.actions:
            set_state(lambda state: replace(state, actions=[action.ActionUseNbLocals(var_name=df_var_name, df_var_out=df_var_name or "mypy")]))
            mixpanel.api.track_with_defaults(
                "interaction",
                {
                    "section": "transformations",
                    "type": "selected dataframe",
                },
            )

    reacton.use_memo(on_df_var_change, [df_var_name])

    with drawer.RightDrawer(
        open=open, on_open=lambda v: close() if not v else None, title="Transformations", edit=bool(edit), on_apply=set_transformations
    ) as main:
        should_select_var = not df_var_name and not (state.actions and edit)
        with sol.Div(class_="lca-transform-header", style_="margin-left: -24px; margin-right: -24px; margin-top: -4px; padding: 8px 80px;"):
            v.Select(v_model=df_var_name, label="DataFrame", on_v_model=set_df_var_name, items=dfs or [])
        with sol.Div(style_="margin-left: -24px; margin-right: -24px"):
            v.Divider()
        if not should_select_var:
            TransformationsPanel(state, dispatch, on_reset=lambda: None, on_save=lambda: None, breakpoints=False, assistant_mode=True).meta(
                ref="TransformationsPanel"
            )
    return main


@reacton.component
def VisualizationPanel(plot_state: vr.PlotState, set_code, dfs, open, edit, on_close):
    plot_state_local, set_plot_state_local = reacton.use_state(cast(Optional[vr.PlotState], None))
    df_ref = reacton.use_ref(cast(pd.DataFrame, None))

    plot_var_name = plot_state_local and plot_state_local.plot_var_name

    def set_plot_var_name(value):
        set_plot_state_local(lambda state: replace(state, plot_var_name=value))

    df_var_name = plot_state_local and plot_state_local.df_var_name

    def set_df_var_name(value):
        mixpanel.api.track_with_defaults(
            "interaction",
            {
                "section": "visualizations",
                "type": "selected dataframe",
            },
        )
        set_plot_state_local(lambda state: replace(state, df_var_name=value))

    def on_plot_type(plot_type):
        mixpanel.api.track_with_defaults(
            "interaction",
            {
                "section": "visualizations",
                "type": "selected plot type",
                "plot_type": plot_type,
            },
        )
        set_plot_state_local(replace(plot_state_local, plot_type=plot_type))

    def on_col_arg(col_arg, value):
        mixpanel.api.track_with_defaults(
            "interaction",
            {
                "section": "visualizations",
                "type": "set attribute",
                "attribute": col_arg,
            },
        )
        set_plot_state_local(vr.set_in(plot_state_local, ["col_args", col_arg], value))

    def on_crossfilter(value):
        mixpanel.api.track_with_defaults(
            "interaction",
            {
                "section": "visualizations",
                "type": "set crossfilter",
            },
        )
        set_plot_state_local(replace(plot_state_local, crossfilter_enabled=value))

    def set_visualization():
        assert plot_state_local
        code_str = plot_builder.generate_code(plot_state_local)
        set_code({"code": code_str, "meta": dumps(plot_state_local)})
        mixpanel.api.track_with_defaults("inserted code", {"section": "visualizations"})
        close()

    def close():
        on_close()

    def init_plot_state():
        if not open:
            return
        if plot_state and edit:
            set_plot_state_local(plot_state)
        else:
            set_plot_state_local(vr.PlotState(plot_var_name=generate_var_name("var")))

    reacton.use_memo(init_plot_state, [plot_state, open])

    def handle_var_name():
        df_ref.current = vr.EqWrapper(low_code_assistant.util.nb_locals[df_var_name]) if df_var_name else None

    reacton.use_memo(handle_var_name, [df_var_name])

    with drawer.RightDrawer(
        open=open,
        on_open=lambda v: close() if not v else None,
        title="Visualization",
        edit=bool(edit),
        on_apply=set_visualization,
        apply_disabled=not df_var_name,
        show_var_out=True,
        var_out=plot_var_name or "",
        on_var_out=set_plot_var_name,
        width="1024px",
    ) as main:
        v.Select(v_model=df_var_name, label="DataFrame", on_v_model=set_df_var_name, items=dfs or [])
        if plot_state_local and df_var_name:
            plot_builder.PlotBuilder(
                plot_state_local,
                df_ref.current,
                df_ref.current and df_ref.current.get().columns.tolist(),
                0,
                on_plot_type=on_plot_type,
                on_col_arg=on_col_arg,
                min_height=None,
                on_crossfilter=on_crossfilter,
            )
    return main


class Symbol:
    def __init__(self, name: str):
        self._name = name

    def __repr__(self):
        return self._name


@reacton.component
def AppPanel(edit_data, set_code, open, edit, on_close, markdown_cells: Optional[Dict] = None):
    layout, on_layout = sol.use_state_or_update(open and edit and edit_data and edit_data["type_card_grid_layout"] or [])

    plot_vars = get_vars(lambda v: isinstance(v, plotly.graph_objs._figure.Figure) or isinstance(v, reacton.core.Element))
    dfs = get_vars(lambda v: isinstance(v, (DataFrame, app.ReactiveDf)))

    def make_code():
        def filter_keys(d: Dict):
            return {k: v for k, v in d.items() if k in ["w", "h", "x", "y"]}

        def layout_item(item: Dict):
            obj: Any = Symbol(item["i"])
            if markdown_cells and item["i"] in markdown_cells:
                obj = item["i"]
            return {"item": obj, **filter_keys(item)}

        layout_with_items = [layout_item(item) for item in layout]

        layout_lines = (",\n" + (" " * 24)).join(str(k) for k in layout_with_items)

        code = textwrap.dedent(
            f"""\
                from low_code_assistant.layout import CardGridLayout
                from low_code_assistant.layout import Preview

                def App():
                    return CardGridLayout([
                        {layout_lines}
                    ])

                Page = App()

                Preview(App)
                """
        )
        set_code({"code": code, "meta": json.dumps({"type_card_grid_layout": layout})})
        mixpanel.api.track_with_defaults("inserted code", {"section": "app"})
        on_close()

    def on_toggle(on):
        mixpanel.api.track_with_defaults(
            "interaction",
            {
                "section": "app",
                "type": "toggle variable",
                "state": bool(on),
            },
        )

    with drawer.RightDrawer(open=open, on_open=lambda v: on_close() if not v else None, title="App", edit=bool(edit), on_apply=make_code, width="100%") as main:
        CardGridLayoutBuilder(obj_vars=plot_vars + (dfs or []), layout=layout, on_layout=on_layout, markdown_cells=markdown_cells, on_toggle=on_toggle)

    return main


@reacton.component
def DeployPanel(open: bool, on_close: Callable[[], None], notebook_path: str):
    def on_v_model(open):
        if not open:
            on_close()

    with v.Dialog(v_model=open, on_v_model=on_v_model) as main:
        with v.Card(style_="height: 90vh", class_="overflow-y-auto"):
            DominoHeader(title="Deploy")
            with v.CardText(class_="pt-2"):
                with v.Sheet():
                    if sys.version_info.minor == 6:
                        sol.Div(children=["Not supported for Python 3.6"])
                    else:
                        Deployer(opened=open, notebook_path=notebook_path)
                with v.CardActions():
                    sol.Button("Close", icon_name="mdi-close", on_click=on_close)
    return main


@reacton.component
def SnippetPanel(set_code, open, on_close, save_count, edit_mode, on_edit_mode, writable_paths):
    root = {"label": "home", "id": 0, "leaf": False}
    path, set_path = reacton.use_state([root])
    refresh_count, set_refresh_count = reacton.use_state(0)

    nr_of_snippets, get_items, get_content = reacton.use_memo(snippets.make_fns, [save_count, refresh_count])

    def on_apply():
        mixpanel.api.track_with_defaults(
            "inserted code",
            {
                "section": "Insert snippet",
            },
        )
        set_code(
            {
                "code": snippet_code,
                "meta": None,
            }
        )
        on_close()

    snippet_code, set_snippet_code = reacton.use_state("")

    def on_edit(content: Snippet):
        set_code(
            {
                "code": f"{EDIT_SNIPPET_PREFIX} {content.base_path / content.path / content.name}\n" + content.code,
            }
        )
        on_close()

    def on_delete(content: Snippet):
        os.remove(content.base_path / content.path / content.name)

    def on_add_snippet(base_path, path, name):
        set_code(
            {
                "code": f"{EDIT_SNIPPET_PREFIX} {Path(base_path) / 'snippets' / Path(*[p['id'] for p in path[1:] if not p['leaf']] + [name + '.py'])}\n",
            }
        )
        on_close()

    with drawer.RightDrawer(
        open=open,
        on_open=lambda v: on_close() if not v else None,
        title="Snippets",
        edit=False,
        on_apply=on_apply,
        apply_disabled=not snippet_code,
        show_default_buttons=bool(nr_of_snippets),
    ) as main:
        with sol.Div(style_="min-width: 1200px; max-width: 1200px; height: 100%;"):
            if open:
                if nr_of_snippets:
                    snippets_ui.SnippetsPanel(
                        get_items,
                        get_content,
                        path,
                        set_path,
                        edit_mode,
                        on_edit_mode,
                        writable_paths,
                        on_edit,
                        on_delete,
                        on_add_snippet,
                        on_snippet=lambda snippet: set_snippet_code(snippet.code if snippet else ""),
                        on_refresh_count=set_refresh_count,
                    ).key("snippets" + str(save_count) + "-" + str(refresh_count))
                else:
                    with sol.Div(class_="text-center"):
                        v.Html(
                            tag="h3",
                            class_="ma-4",
                            children=["No snippets found. Snippets can be added by adding a shared project or shared dataset that has a snippets directory."],
                        )

    return main


@reacton.component
def Assistant():
    code, set_code = reacton.use_state(cast(Optional[Dict], None))
    code_up, set_code_up = reacton.use_state(cast(Optional[Dict], None))
    selected, set_selected = reacton.use_state(cast(Optional[Dict], None))

    notebook_path, set_notebook_path = reacton.use_state(cast(Optional[str], None))

    edit_data, set_edit_data = reacton.use_state(cast(Optional[Dict["str", Any]], None))
    markdown_cells, set_markdown_cells = reacton.use_state(cast(Optional[Dict], None))

    snippet_saved_count, set_snippet_saved_count = reacton.use_state(0)
    snippet_edit_mode, set_snippet_edit_mode = reacton.use_state(False)
    writable_paths, set_writable_paths = reacton.use_state(cast(Optional[List[str]], None))

    snippet_add_header, set_snippet_add_header = reacton.use_state(cast(Optional[str], None))
    add_dialog_open, set_add_dialog_open = reacton.use_state(False)

    def handle_code_up():
        if code_up and code_up.get("type_") == "markdown":
            set_edit_data({"markdown": code_up["code"]})
        elif code_up and code_up.get("meta"):
            set_edit_data(loads(code_up.get("meta")))
        else:
            set_edit_data(None)

    reacton.use_memo(handle_code_up, [code_up])

    dfs = get_vars(lambda v: isinstance(v, DataFrame))

    def update_markdown():
        notebook.markdown_cells = markdown_cells

    reacton.use_memo(update_markdown, [markdown_cells])

    def on_selected():
        if selected and selected.get("action"):
            mixpanel.api.track_with_defaults(
                "open",
                {
                    "section": selected.get("action"),
                    "edit": bool(selected.get("edit")),
                },
            )

    reacton.use_memo(on_selected, [selected])

    reacton.use_memo(lambda: set_writable_paths(snippets.get_writable_paths()), [])

    with v.Sheet() as main:
        css.Css()

        if mixpanel.mixpanel_widget:
            sol.Div(children=[mixpanel.mixpanel_widget])
        AssistantWidget.element(
            menu=Menu(
                selected=selected, on_selected=set_selected, decoded=edit_data, snippet_edit_mode=snippet_edit_mode, on_snippet_edit_mode=set_snippet_edit_mode
            ),
            code=code,
            on_code=set_code,
            on_notebook_path=set_notebook_path,
            on_code_up=set_code_up,
            markdown_cells=markdown_cells,
            on_markdown_cells=set_markdown_cells,
            on_snippet_saved_count=set_snippet_saved_count,
            snippet_edit_mode=snippet_edit_mode,
            snippet_add_header=snippet_add_header,
            snippet_add_dialog_open=add_dialog_open,
            on_snippet_add_dialog_open=set_add_dialog_open,
        )
        MarkdownPanel(
            edit_data,
            set_code,
            open=(selected and selected.get("action")) == "markdown",
            edit=selected and selected.get("edit"),
            on_close=lambda: set_selected(None),
        )

        LoadPanel(
            edit_data,
            set_code,
            open=(selected and selected.get("action")) == "load_data",
            edit=selected and selected.get("edit"),
            on_close=lambda: set_selected(None),
        )

        TransformationPanel(
            edit_data,
            set_code,
            dfs,
            open=(selected and selected.get("action")) == "transformations",
            edit=selected and selected.get("edit"),
            on_close=lambda: set_selected(None),
        ).key(f'trans-edit-{selected and selected.get("edit")}')

        VisualizationPanel(
            cast(vr.PlotState, edit_data),
            set_code,
            dfs,
            open=(selected and selected.get("action")) == "visualizations",
            edit=(selected and selected.get("edit")),
            on_close=lambda: set_selected(None),
        ).key(f'viz-edit-{selected and selected.get("edit")}')

        AppPanel(
            edit_data,
            set_code,
            open=(selected and selected.get("action")) == "app",
            edit=selected and selected.get("edit"),
            on_close=lambda: set_selected(None),
            markdown_cells=markdown_cells,
        )

        SnippetPanel(
            set_code,
            open=(selected and selected.get("action")) == "snippets",
            on_close=lambda: set_selected(None),
            save_count=snippet_saved_count,
            edit_mode=snippet_edit_mode,
            on_edit_mode=set_snippet_edit_mode,
            writable_paths=writable_paths,
        )

        def on_add_snippet(base_path, path, name):
            set_snippet_add_header(
                f"{EDIT_SNIPPET_PREFIX} {Path(base_path) / 'snippets' / Path(*[p['id'] for p in path[1:] if not p['leaf']] + [name + '.py'])}\n"
            )
            set_add_dialog_open(False)

        if writable_paths:
            snippets_ui.AddDialog(writable_paths, add_dialog_open, set_add_dialog_open, on_add_snippet)

        def close():
            set_selected(None)

        DeployPanel(open=(selected and selected.get("action")) == "deploy", on_close=close, notebook_path=notebook_path or "")

    return main
