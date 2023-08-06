import inspect
import types
from dataclasses import dataclass
from functools import partial
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import ipyvuetify as vy
import plotly.express as px
import plotly.graph_objs._figure
import plotly.io as pio
import reacton
import reacton.ipyvuetify as v
import solara
import solara as sol

import low_code_assistant.hooks as dhooks
import low_code_assistant.viz_reducer as vr

basic_col_args = (
    "x",
    "y",
    "locations",
    "color",
    "symbol",
    "r",
    "theta",
    "lat",
    "lon",
    "z",
    "a",
    "b",
    "c",
    "size",
)
extra_col_args = (
    "line_group",
    "symbol",
    "pattern_shape",
    "line_dash",
    "names",
    "values",
    "parents",
    "text",
    "hover_name",
    "hover_data",
    "facet_row",
    "facet_col",
    "base",
)

col_list_args = ("hover_data",)

basic_plots = (
    "area",
    "bar",
    "histogram",
    "line",
    "line_3d",
    "scatter",
    "scatter_3d",
    "scatter_geo",
    "choropleth",
)

translations = {
    "area": "Area",
    "bar": "Bar",
    "histogram": "Histogram",
    "line": "Line",
    "line_3d": "Line 3D",
    "scatter": "Scatter",
    "scatter_3d": "Scatter 3D",
    "scatter_geo": "Scatter Map",
    "choropleth": "Choropleth Map",
    "x": "X-axis",
    "y": "Y-axis",
    "z": "Z-axis",
}


def un_dash(value):
    return " ".join([el.capitalize() for el in value.split("_")])


def get_args(name):
    return inspect.getfullargspec(getattr(px, name)).args


def get_col_args(name):
    return [a for a in get_args(name) if a in basic_col_args + extra_col_args]


specs = {
    n: {
        "name": n,
        "col_args": get_col_args(n),
        "args": get_args(n),
    }
    for n in dir(px)
    if isinstance(getattr(px, n), types.FunctionType) and get_args(n)[0] == "data_frame"
}


arg_types: Dict[str, Dict[str, Any]] = {
    "template": {
        "type": list(pio.templates._templates.keys()),
        "default": "plotly",
        "name": "Theme",
    },
    "orientation": {
        "type": ["h", "v"],
        "default": "v",
        "type_mapping": ["Horizontal", "Vertical"],
        "name": "Orientation",
    },
    "histnorm": {
        "type": ["percent", "probability", "density"],
        "name": "Normalization",
    },
    "histfunc": {
        "type": ["count", "sum", "avg", "min", "max"],
        "default": "count",
        "name": "Aggregate Function",
    },
    "log_x": {"type": bool, "default": False, "description": "If True, the x-axis is log-scaled in cartesian coordinates", "name": "Logarithmic X-axis"},
    "log_y": {
        "type": bool,
        "default": False,
        "description": "If True, the x-axis is log-scaled in cartesian coordinates",
        "name": "Logarithmic Y-axis",
    },
    "color_continuous_scale": {
        "type": [x for x in dir(px.colors.sequential) if not x.startswith("_")],
        "default": "Plasma",
        "name": "Color Scale",
    },
}

plot_types = basic_plots


def nop(*_):
    return


plot_type_items = [dict(value=t, text=translations[t]) for t in plot_types]


def generate_code(plot_state: vr.PlotState):
    args = {k: v for k, v in plot_state.col_args.items() if k in specs[plot_state.plot_type]["args"]}  # type: ignore

    def transform_arg(k, value):
        if k == "color_continuous_scale":
            return f"px.colors.sequential.{value}"
        if type(value) == str:
            return f'"{value}"'
        return value

    arg_str = ", ".join(
        [f"{k}={transform_arg(k, v)}" for k, v in args.items() if v is not None and not (isinstance(v, list) and len(v) == 0)],
    )

    def remove_margins(var_name):
        return f"{var_name}.update_layout(margin=dict(l=0, r=0, t=40 if {var_name}.layout.title.text else 0, b=0))"

    if plot_state.crossfilter_enabled:
        base_var_name = "_base_" + (plot_state.plot_var_name or "")
        select_config = ""
        if plot_state.plot_type == "scatter":
            select_config = f'{base_var_name}.update_layout(dragmode="lasso")\n'
        elif plot_state.plot_type in ["bar", "histogram"]:
            direction = "v" if "orientation" in plot_state.col_args and plot_state.col_args["orientation"] == "h" else "h"
            select_config = f'{base_var_name}.update_layout(dragmode="select", selectdirection="{direction}")\n'
        return "".join(
            [
                "from low_code_assistant.express import FigurePlotlyCrossFiltered\n",
                "import plotly.express as px\n\n",
                f"{base_var_name} = px.{plot_state.plot_type}({plot_state.df_var_name}, {arg_str})\n",
                select_config,
                remove_margins(base_var_name) + "\n",
                f"{plot_state.plot_var_name} = " if plot_state.plot_var_name else "",
                f"FigurePlotlyCrossFiltered({base_var_name})\n",
                f"\n{plot_state.plot_var_name}" if plot_state.plot_var_name else "",
            ]
        )
    return "".join(
        [
            "import plotly.express as px\n\n",
            f"{plot_state.plot_var_name} = " if plot_state.plot_var_name else "",
            f"px.{plot_state.plot_type}({plot_state.df_var_name}, {arg_str})\n",
            remove_margins(plot_state.plot_var_name),
            f"\n{plot_state.plot_var_name}" if plot_state.plot_var_name else "",
        ]
    )


@reacton.component
def NewPlotPanel(on_add: Callable[[vr.PlotState], Any] = None):
    state, set_state, dispatch = dhooks.use_viz()
    title, set_title = reacton.use_state("")

    def new_plot():
        if on_add:
            on_add(vr.PlotState(name=title or fallback_name, plot_type=plot_type))

    plot_type, set_plot_type = reacton.use_state(plot_types[0])
    # a nice default name
    i = len(state.plots)
    fallback_name = f"{plot_type}-{i}"

    with v.Sheet(style_="min-height: 724px") as main:
        v.TextField(label="Plot name", v_model=title, on_v_model=set_title, placeholder=fallback_name)
        v.Select(label="Plot Type", items=plot_type_items, v_model=plot_type, on_v_model=set_plot_type)
        sol.Button("Create", on_click=new_plot, color="primary")

    return main


@reacton.component
def DimensionSelects(plot_state, on_col_arg: Callable[[str, Any], None], columns, for_cols: Union[List[str], Tuple[str, ...]]):
    with v.Row() as main:
        for col_arg in specs[plot_state.plot_type]["col_args"]:
            if col_arg not in for_cols:
                continue
            with v.Col(sm=2):
                with solara.Div().key(str(col_arg)):
                    v.Select(
                        label=translations.get(col_arg) or un_dash(col_arg),
                        items=columns,
                        clearable=True,
                        multiple=col_arg in col_list_args,
                        v_model=plot_state.col_args.get(col_arg),
                        on_v_model=partial(on_col_arg, col_arg),
                    )
    return main


@reacton.component
def OptionsPanel(plot_state, on_col_arg):
    with v.Row() as main:
        for arg in specs[plot_state.plot_type]["args"]:
            if arg not in arg_types:
                continue
            with v.Col(sm=2):
                with solara.Div():
                    arg_spec = arg_types[arg]
                    if arg_spec.get("type") == bool:
                        v.Switch(
                            label=arg_spec["name"],
                            v_model=plot_state.col_args.get(arg),
                            on_v_model=partial(on_col_arg, arg),
                        )
                    elif type(arg_spec["type"]) in (list, tuple):
                        v.Select(
                            label=arg_spec["name"],
                            items=[dict(value=v, text=t) for v, t in zip(arg_spec["type"], arg_spec["type_mapping"])]
                            if arg_spec.get("type_mapping")
                            else arg_spec["type"],
                            v_model=plot_state.col_args.get(arg),
                            on_v_model=partial(on_col_arg, arg),
                        )
    return main


@dataclass(frozen=True)
class FigState:
    fig: Optional[plotly.graph_objs._figure.Figure] = None
    error: Optional[str] = None
    code: Optional[str] = None


@reacton.component
def PlotBuilder(
    plot_state: vr.PlotState, df, columns, index, on_plot_type=nop, on_col_arg=nop, min_height="724px", on_crossfilter=nop, var_name=None, on_var_name=None
):
    state, set_state = reacton.use_state(FigState())
    exp_panel, set_exp_panel = reacton.use_state(0)

    def make_fig():
        if not plot_state.col_args or not plot_state.plot_type or not df:
            set_state(FigState())
            return
        try:
            args = {k: v for k, v in plot_state.col_args.items() if k in specs[plot_state.plot_type]["args"]}
            fig = getattr(px, plot_state.plot_type)(df.get(), **args)
            code = generate_code(plot_state)
            set_state(FigState(fig=fig, code=code))
        except Exception as e:
            set_state(FigState(error=str(e)))

    reacton.use_effect(make_fig, [plot_state, df, index])

    with v.Sheet(style_=min_height and f"min-height: {min_height}") as main:
        if on_var_name:
            v.TextField(label="Variable name", v_model=var_name, on_v_model=on_var_name).meta(ref="var")
        v.Select(
            label="Plot Type",
            items=plot_type_items,
            v_model=plot_state.plot_type,
            on_v_model=on_plot_type,
        )
        with v.Col(sm=2):
            with solara.Div():
                v.Switch(label="Enable crossfilter", v_model=plot_state.crossfilter_enabled, on_v_model=on_crossfilter)

        if plot_state.plot_type:
            with v.Sheet():
                with v.ExpansionPanels(v_model=exp_panel, on_v_model=set_exp_panel):
                    with v.ExpansionPanel():
                        v.ExpansionPanelHeader(children=["Dimensions"])
                        with v.ExpansionPanelContent():
                            DimensionSelects(plot_state, on_col_arg, columns, basic_col_args)
                    with v.ExpansionPanel():
                        v.ExpansionPanelHeader(children=["Extra Dimensions"])
                        with v.ExpansionPanelContent():
                            DimensionSelects(plot_state, on_col_arg, columns, extra_col_args)
                    with v.ExpansionPanel():
                        v.ExpansionPanelHeader(children=["Options"])
                        with v.ExpansionPanelContent():
                            OptionsPanel(plot_state, on_col_arg)

            if state.error:
                solara.Div(children=["plot error", state.error])
            elif state.fig:
                solara.FigurePlotly(state.fig, dependencies=state)
                from solara.components.code_highlight_css import CodeHighlightCss

                CodeHighlightCss()
                from low_code_assistant.code import Code

                Code(
                    code_chunks=[state.code],
                    on_event=lambda a: None,
                    error=None,
                )

    return main


@reacton.component
def Visualizations(state: vr.VizState):
    state, set_state, dispatch = dhooks.use_viz()

    tab, set_tab = reacton.use_state(0)

    def add(plot: vr.PlotState):
        dispatch(vr.ActionAddPlot(plot))
        set_tab(len(state.plots or []) + 1)

    with v.Tabs(v_model=tab, on_v_model=set_tab) as main:
        for index, plot in enumerate(state.plots or []):

            def on_close(index=index):
                if index <= tab:
                    # we are removing the selected one, or one to our left
                    # so move one tab to the left
                    set_tab(max(0, tab - 1))
                dispatch(vr.ActionRemovePlot(index))

            # TODO: use this
            button_close = sol.IconButton("mdi-window-close", on_click=on_close, click_event="click.prevent.stop")
            # with v.Btn(icon=True) as button_close:
            #     v.Icon(children=["mdi-window-close"])

            # use_event(button_close, "click.stop", lambda *_: on_close())

            vy.Tab.element(
                children=[
                    plot.name,
                    button_close,
                ],
            ).key(plot.id + "tab")
        v.Tab(children=["new"])

        with v.TabsItems(v_model=tab):
            for index, plot in enumerate(state.plots or []):

                with v.TabItem(value=index).key(plot.id + "tab-item"):
                    PlotBuilder(
                        plot,
                        state.df,
                        state.columns,
                        index,
                        on_plot_type=lambda val, index=index: dispatch(vr.ActionSetPlotType(index, val)),
                        on_col_arg=lambda arg, val, index=index: dispatch(vr.ActionSetColArg(index=index, arg=arg, value=val)),
                    )

            with v.TabItem(value=len(state.plots or [])).key("__new__item"):
                NewPlotPanel(on_add=add)

    return main
