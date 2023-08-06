from functools import partial
from typing import Callable, Dict, List, cast

import plotly
import reacton
import reacton.ipyvuetify as v
import solara as sol
from pandas.core.frame import DataFrame

from low_code_assistant import app, css, util

from .assistant import notebook


def to_widget(x):
    if isinstance(x, plotly.graph_objs._figure.Figure):
        return sol.FigurePlotly(x)
    else:
        # todo: add special cases as needed
        return x


@reacton.component
def VerticalLayout(children):
    with sol.Div() as main:
        for child in children:
            with sol.Div():
                to_widget(child)
    return main


@reacton.component
def Preview(app: Callable[[], reacton.core.Element]):
    open, set_open = reacton.use_state(False)
    with v.Sheet() as main:
        with v.Dialog(v_model=open, on_v_model=lambda v: set_open(v)):
            v.Sheet(class_="overflow-y-auto overflow-x-auto", style_="height: calc(100vh - 96px); width: calc(100vw - 48px)", children=[app()])
        sol.Button("Preview", color="primary", icon_name="mdi-magnify", on_click=lambda: set_open(True))

    return main


def _make_grid_panel_builder(layout_item, markdown_cells):

    children = []
    if layout_item.get("i"):
        i = layout_item.get("i")
        if util.nb_locals.get(i) is not None:
            obj = util.nb_locals[i]
            if isinstance(obj, plotly.graph_objs._figure.Figure):
                children = [sol.FigurePlotly(obj)]
            elif isinstance(obj, DataFrame):
                children = [DataTableCrossFiltered(obj)]
            elif isinstance(obj, app.ReactiveDf):
                children = [app.DropDataframe(obj.var_name, obj.label)]
            else:
                children = [obj]
        elif markdown_cells and i in markdown_cells:
            children = [sol.Markdown(markdown_cells[i])]

    with v.Card(style_="height: 100%;") as panel:
        v.CardText(style_="height: 100%; max-height: 100%; overflow: auto;", children=children)

    return panel


def _make_grid_panel_viewer(obj):
    def wrap(obj):
        if isinstance(obj, plotly.graph_objs._figure.Figure):
            return sol.FigurePlotly(obj)
        if isinstance(obj, DataFrame):
            return DataTableCrossFiltered(obj)
        elif isinstance(obj, app.ReactiveDf):
            return app.DropDataframe(obj.var_name, obj.label)
        if isinstance(obj, str):
            if notebook.markdown_cells and obj in notebook.markdown_cells:
                return sol.Markdown(notebook.markdown_cells[obj])

            return sol.Text(f"Markdown: {obj} not found")
        return obj

    with v.Card(style_="height: 100%;") as panel:
        v.CardText(style_="height: 100%; max-height: 100%; overflow: auto;", children=[wrap(obj)])

    return panel


@reacton.component
def CardGridLayoutBuilder(obj_vars, layout, on_layout, markdown_cells, on_toggle):
    sol.provide_cross_filter()
    objects_on = [k["i"] for k in layout]

    def toggle_layout(on, id):
        on_toggle(on)

        def update(layout):
            layout_contains_id = any([k for k in layout if k["i"] == id])

            if on:
                top_y = max([k["y"] + k["h"] for k in layout]) if layout else 0
                return layout + [dict(i=id, w=6, h=5, x=0, y=top_y)] if not layout_contains_id else layout
            else:
                return [k for k in layout if k["i"] != id] if layout_contains_id else layout

        on_layout(lambda state: update(state))

    items = {layout_item["i"]: _make_grid_panel_builder(layout_item, markdown_cells) for layout_item in layout}

    with v.Sheet(class_="domino-plotly-auto-height domino-card-grid") as main:
        css.Css()
        with v.Row():
            for obj_var in obj_vars + list(markdown_cells.keys() if markdown_cells else []):
                label = obj_var
                if markdown_cells and obj_var in markdown_cells:
                    label = markdown_cells[obj_var].replace("\n", " ")
                    length = len(label)
                    label = label[:28] + ("..." if length > 28 else "")
                with v.Col(sm=1):
                    v.Switch(label=label, v_model=obj_var in objects_on, on_v_model=partial(toggle_layout, id=obj_var))
        sol.GridLayout(items=items, grid_layout=layout, resizable=True, draggable=True, on_grid_layout=on_layout)

    return main


@reacton.component
def CardGridLayout(layout, resizable=False, draggable=False):
    sol.provide_cross_filter()

    layout_without_item, set_layout_without_item = reacton.use_state(cast(List[Dict], []))

    layout_no_item = [
        {
            **util.remove_keys(item, ["item"]),
            "i": index,
        }
        for index, item in enumerate(layout)
    ]

    reacton.use_memo(lambda: set_layout_without_item(layout_no_item), [layout_no_item])

    items = [_make_grid_panel_viewer(layout_item["item"]) for layout_item in layout]

    with sol.Div(class_="domino-plotly-auto-height domino-card-grid") as main:
        css.Css()
        sol.GridLayout(items=items, grid_layout=layout_without_item, resizable=resizable, draggable=draggable, on_grid_layout=set_layout_without_item)

    return main


@reacton.component
def DataTableCrossFiltered(df):
    dff = df
    filter, set_filter = sol.use_cross_filter(id(df), "datatable")
    if filter is not None:
        dff = df[filter]
    return sol.DataTable(dff, items_per_page=10, scrollable=True)
