import pickle
from datetime import datetime
from typing import Optional, Tuple, cast

import reacton
import reacton.ipyvuetify as v
import solara
from solara.components.code_highlight_css import CodeHighlightCss

import low_code_assistant.action as action
import low_code_assistant.actions_store as actions_store
import low_code_assistant.viz_reducer as vr
from low_code_assistant import action_ui
from low_code_assistant.code import Code

# from low_code_assistant.data_panel import DataPanel
from low_code_assistant.deployer import Deployer
from low_code_assistant.hooks import provide_viz, use_reducer_addon, use_viz
from low_code_assistant.layout_builder import LayoutBuilder
from low_code_assistant.plot_builder import Visualizations
from low_code_assistant.util import DominoHeader, get_nb_locals
from low_code_assistant.visualization import DataTable

# solara.widgets.watch()
# ipyvue.watch()


widget_render_error_msg = """Cannot show the Dominocode app, you should:
<ul>
    <li>Rerun the code cell above (<i>Click in the code cell, and press Shift+Enter <kbd>⇧</kbd>+<kbd>↩</kbd></i>).
    <li>Or start a new app by clicking the blue Dominocode button in the toolbar above 👆.
</ul>
"""

mime_bundle_default = {"text/html": widget_render_error_msg}


def pickle_state(action_state: actions_store.ActionsState, viz_state: vr.VizState, filename: str):
    full_state = {
        "action_state": actions_store.ActionsState(actions=action_state.actions, undo_stack=action_state.undo_stack, redo_stack=action_state.redo_stack),
        "viz_state": vr.VizState(plots=viz_state.plots),
    }

    with open(filename, "bw") as f:
        pickle.dump(full_state, f)


def unpickle_state(filename):
    with open(filename, "rb") as f:
        full_state = pickle.load(f)
        return full_state["action_state"], full_state["viz_state"]


@reacton.component
def TransformationsPanel(state, dispatch, on_reset, on_save, breakpoints, assistant_mode=False):
    show_code, set_show_code = reacton.use_state(False)
    show_table, set_show_table = reacton.use_state(True)
    filter_like, set_filter_like = reacton.use_state(cast(Optional[Tuple[str, int]], None))

    def _get_for_index(colection, index):
        if index is None:
            return colection[-1]
        else:
            return colection[index] if 0 <= index < len(colection) else []

    def get_column_names(index):
        return _get_for_index(state.columns_for_action, index)

    def get_dtypes(index):
        return _get_for_index(state.dtypes_for_action, index)

    def reset():
        dispatch((actions_store.e_reset, None))
        on_reset()

    def on_code_view_event(event):
        if not event:
            return
        index = event["index"]
        if isinstance(state.actions[0], action.ActionUseNbLocals):
            index += 1
        name = event["name"]
        if name == "delete":
            dispatch((actions_store.e_delete_index, index))
        if name == "edit":
            dispatch((actions_store.e_edit_index, index))
        if name == "insert":
            dispatch((actions_store.e_insert_index, index))

    add_state, set_add_state = reacton.use_state(cast(action.Action, action.ActionFilter()))
    dialog_state, set_dialog_state = reacton.use_state(cast(action.Action, action.ActionFilter()))

    def on_edit_index():
        if state.index_of_edit_action is not None:
            set_dialog_state(state.actions[state.index_of_edit_action])
        if state.index_of_insert_action is not None:
            set_dialog_state(action.ActionFilter())

    reacton.use_memo(on_edit_index, [state.index_of_edit_action, state.index_of_insert_action])

    with v.Sheet() as main:
        if state.index_of_edit_action is not None:
            index = state.index_of_edit_action
            with v.Dialog(v_model=True, on_v_model=lambda open: dispatch((actions_store.e_edit_index, None)) if not open else None, width="50vw"):
                with v.Card().meta(ref="EditAction"):
                    DominoHeader(title="Edit transformation")
                    with v.CardText():
                        action_ui.EditAction(
                            columns=get_column_names(index - 1),
                            dtypes=get_dtypes(index - 1),
                            on_action=set_dialog_state,
                            action_obj=dialog_state,
                        ).meta(ref="EditAction")
                    with v.CardActions():
                        v.Spacer()
                        solara.Button("edit transformation", color="primary", on_click=lambda: dispatch((actions_store.e_edit_action, dialog_state)))
        if state.index_of_insert_action is not None:
            with v.Dialog(v_model=True, on_v_model=lambda open: dispatch((actions_store.e_insert_index, None)) if not open else None, width="50vw"):
                with v.Card().meta(ref="insert_panel"):
                    DominoHeader(title="Insert transformation")
                    with v.CardText():
                        action_ui.TransformationPanel(
                            columns=get_column_names(state.index_of_insert_action),
                            dtypes=get_dtypes(state.index_of_insert_action),
                            action_=dialog_state,
                            on_action=set_dialog_state,
                            on_action_type=lambda t: set_dialog_state(t()),
                        )
                    with v.CardActions():
                        v.Spacer()
                        solara.Button("insert transformation", color="primary", on_click=lambda: dispatch((actions_store.e_insert_action, dialog_state)))
        if filter_like is not None:
            with v.Dialog(v_model=True, on_v_model=lambda open: set_filter_like(None) if not open else None, width="50vw"):
                with v.Card():
                    DominoHeader(title="Filter like")
                    with v.CardText():
                        column, index = filter_like
                        value = state.df_wrapper.df.iloc[index][column]
                        value = str(value)
                        action_val = action.ActionFilter(col=column, dtype=get_dtypes(None)[column], value=value, op="==")
                        action_ui.FilterPanel(
                            columns=get_column_names(None),
                            dtypes=get_dtypes(None),
                            on_action=lambda action: [set_filter_like(None), dispatch((actions_store.e_insert_action, action))],
                            fill=action_val,
                        ).key(f"filter_like {action_val.__hash__()}")
        with v.Row(no_gutters=not breakpoints):
            with v.Col(sm=12, lg=5 if breakpoints else 12):
                with solara.Div():
                    if show_table and state.df_wrapper.has_df:
                        DataTable(
                            state.df_wrapper.df,
                            on_drop_column=lambda column: dispatch((actions_store.e_insert_action, action.ActionDropColumns(columns=[column]))),
                            on_filter_value=lambda col, row: set_filter_like((col, row)),
                        ).meta(ref="DataTable")

                    with solara.Div():

                        def on_action(action_):
                            dispatch((actions_store.e_insert_action, (idx, action_)))
                            set_add_state(action.ActionFilter())

                        idx = len(state.actions) - 1

                        if not state.error:
                            with solara.Div(style_="max-width: 600px; margin-left: auto; margin-right: auto;").meta(ref="insert_panel"):
                                action_ui.TransformationPanel(
                                    columns=get_column_names(idx),
                                    dtypes=get_dtypes(idx),
                                    action_=add_state,
                                    on_action=set_add_state,
                                    on_action_type=lambda t: set_add_state(t()),
                                )
                                with solara.Div(style_="display: flex"):
                                    v.Spacer()
                                    solara.Button(outlined=True, color="primary", on_click=lambda: on_action(add_state), children=["add transformation"])
                    with v.CardActions(class_="ma-0"):
                        if not assistant_mode:
                            solara.Button(
                                icon_name="mdi-delete",
                                on_click=lambda: reset(),
                                icon=True,
                            )
                            solara.Button(
                                icon=True,
                                icon_name="mdi-content-copy",
                                disabled=True,
                            )
                            solara.Button(
                                icon_name="mdi-content-save",
                                on_click=on_save,
                                icon=True,
                            )
                        solara.Button(
                            icon_name="mdi-undo",
                            on_click=lambda: dispatch((actions_store.e_undo, None)),
                            icon=True,
                            disabled=not state.undo_stack,
                        ).meta(ref="btn_undo")
                        solara.Button(
                            icon_name="mdi-redo",
                            on_click=lambda: dispatch((actions_store.e_redo, None)),
                            icon=True,
                            disabled=len(state.redo_stack) == 0,
                        ).meta(ref="btn_redo")
                        v.Switch(label="Show table", v_model=show_table, on_v_model=set_show_table, class_="mx-4")
                        v.Switch(label="Show code", v_model=show_code, on_v_model=set_show_code, class_="mx-4")

                    if state.error:
                        v.Alert(
                            type="error",
                            text=True,
                            prominent=True,
                            icon="mdi-alert",
                            children=[f"{state.error[1]}"],
                        )
                    if show_code or state.error:
                        CodeHighlightCss()
                        Code(code_chunks=state.code_chunks, on_event=on_code_view_event, error=state.error, assistant_mode=assistant_mode)
    return main


@reacton.component
def DominocodeMain(nb_locals, breakpoints):
    state, set_state = reacton.use_state(actions_store.ActionsState())
    dispatch = use_reducer_addon(actions_store.actions_reducer, set_state)
    tab, set_tab = reacton.use_state(0)
    provide_viz()
    viz_state, set_viz_state, viz_dispatch = use_viz()

    actions_store.use_execute_df(state, set_state, nb_locals)
    publish_dialog, set_publish_dialog = reacton.use_state(False)

    reacton.use_effect(
        lambda: viz_dispatch(vr.ActionDF(state.df_wrapper.df)),
        [state.df_wrapper],
    )

    def on_save():
        now = datetime.now()
        dt_string = now.strftime("%Y%m%d%H%M%S")
        pickle_state(state, viz_state, f"{dt_string}.domino.nocode"),

    with v.Sheet(class_="px-2") as main:
        with v.Snackbar(v_model=state.df_exec_status == actions_store.ThreadState.RUNNING, timeout=0):
            solara.Text("Executing ")
            v.ProgressLinear(indeterminate=True, class_="ml-8")
        if not state.actions:
            with v.Card(class_="my-2"):
                DominoHeader(title="Load data")
                with v.CardText(class_="pt-2"):
                    pass
                    # todo: refactor to new datamodel of DataPanel if no-code mode needed again
                    # def on_file_name(filename: str, df_var: str):
                    #     if filename.endswith(".nocode"):
                    #         state_action, state_viz = unpickle_state(filename)
                    #         set_viz_state(state_viz)
                    #         set_state(state_action)
                    #     else:
                    #         dispatch((actions_store.e_insert_action, action.ActionOpen(filename=filename, df_var_out=df_var)))

                    # DataPanel(on_file_name=on_file_name, on_action=lambda action: dispatch((actions_store.e_insert_action, action)))
        else:
            with v.Tabs(background_color="#2d71c7", dark=True, v_model=tab, on_v_model=set_tab):
                v.Tab(children=["Visualization"])
                v.Tab(children=["Table and Transformations"])
                v.Tab(children=["Publish"])
                with v.TabItem():
                    if state.df_wrapper.has_df and viz_state.plots is not None:
                        Visualizations(state=viz_state)
                with v.TabItem():
                    TransformationsPanel(state, dispatch, lambda: viz_dispatch(vr.ActionReset()), on_save, breakpoints)
                with v.TabItem():
                    LayoutBuilder(viz_state, set_viz_state)
                    solara.Button("publish", color="primary", on_click=lambda: set_publish_dialog(True))
                    with v.Dialog(v_model=publish_dialog, on_v_model=set_publish_dialog):
                        Deployer()

    return main


nb_locals = get_nb_locals()


@reacton.component(mime_bundle=mime_bundle_default)
def Dominocode(breakpoints=False):
    return DominocodeMain(nb_locals, breakpoints)
