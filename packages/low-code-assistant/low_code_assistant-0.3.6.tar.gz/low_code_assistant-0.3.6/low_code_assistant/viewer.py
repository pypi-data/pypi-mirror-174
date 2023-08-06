from typing import Any, Optional, cast

import plotly.express as px
import reacton
import reacton.ipyvuetify as v
import solara

import low_code_assistant.viz_reducer as vr
from low_code_assistant import actions_store
from low_code_assistant.hooks import use_reducer_addon
from low_code_assistant.low_code_assistant import unpickle_state
from low_code_assistant.plot_builder import specs


def use_fig(plot_state: vr.PlotState, df):
    state, set_state = reacton.use_state(cast(Optional[Any], None))

    def make_fig():
        if df.get() is None or not plot_state.col_args or not plot_state.plot_type:
            set_state(None)
            return
        try:
            args = {k: v for k, v in plot_state.col_args.items() if k in specs[plot_state.plot_type]["col_args"]}
            fig = getattr(px, plot_state.plot_type)(df.get(), title=plot_state.name, **args)
            set_state(fig)
        except Exception as e:
            set_state(str(e))

    reacton.use_effect(make_fig, [plot_state, df])

    return state


@reacton.component
def PlotView(plot_state: vr.PlotState, df):
    fig = use_fig(plot_state, df)

    with v.Sheet() as main:
        if df.get() is not None:
            if fig:
                if isinstance(fig, str):
                    solara.Div(children=["plot error: ", fig])
                else:
                    solara.FigurePlotly(fig)

    return main


@reacton.component
def Viewer(filename: str):
    state, set_state = reacton.use_state(actions_store.ActionsState())
    viz_state, set_viz_state = reacton.use_state(vr.VizState())
    viz_dispatch = use_reducer_addon(vr.viz_reducer, set_viz_state)

    actions_store.use_execute_df(state, set_state)

    reacton.use_effect(
        lambda: viz_dispatch(vr.ActionDF(state.df_wrapper.df)),
        [state.df_wrapper],
    )

    def load_state():
        state_action, state_viz = unpickle_state(filename)
        set_state(state_action)
        set_viz_state(state_viz)

    reacton.use_effect(load_state, [filename])

    with v.Sheet() as main:
        with v.Snackbar(v_model=state.df_exec_status == actions_store.ThreadState.RUNNING, timeout=0):
            solara.Text("Executing ")
            v.ProgressLinear(indeterminate=True, class_="ml-8")
        for plot_state in viz_state.plots or []:
            PlotView(plot_state, viz_state.df)

    return main
