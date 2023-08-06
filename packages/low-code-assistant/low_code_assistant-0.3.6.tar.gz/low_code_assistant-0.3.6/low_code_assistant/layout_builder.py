import dataclasses
from functools import partial

import reacton
import reacton.ipyvuetify as v
import solara as sol

import low_code_assistant.viz_reducer as vr


@reacton.component
def ColorCard(title, color):
    with v.Card(style_=f"background-color: {color}; width: 100%; height: 100%") as main:
        v.CardTitle(children=[title])

    return main


@reacton.component
def LayoutBuilder(viz_state: vr.VizState, set_viz_state):
    layout_ids = [k["i"] for k in viz_state.layout]

    def update_layout(layout):
        set_viz_state(lambda state: dataclasses.replace(state, layout=layout))

    def toggle_layout(on, id):
        def update(layout):
            layout_contains_id = any([k for k in layout if k["i"] == id])

            if on:
                top_y = max([k["y"] + k["h"] for k in layout]) if layout else 0
                return layout + [dict(i=id, w=6, h=5, x=0, y=top_y)] if not layout_contains_id else layout
            else:
                return [k for k in layout if k["i"] != id] if layout_contains_id else layout

        set_viz_state(lambda state: dataclasses.replace(state, layout=update(state.layout)))

    colors = "green red orange brown yellow pink".split()

    if viz_state and viz_state.plots:
        id_name_map = {plot.id: plot.name for plot in viz_state.plots}

        def make_panel(i, layout_item):
            return ColorCard(title=id_name_map[layout_item["i"]], color=colors[i])
            # with v.Card(color=colors[i]) as panel:
            #     v.CardTitle(children=[f"{id_name_map[l['i']]}"])
            #     with v.CardText():
            #         import plotly.express as px
            #         fig = px.line(x=[1, 2, 3], y=[1, 2, 3])
            #         fig.update_layout({'autosize': True})
            #         print(fig)
            #         sol.FigurePlotly(fig)
            # return panel

        items = {layout_item["i"]: make_panel(i, layout_item) for i, layout_item in enumerate(viz_state.layout)}

        with v.Sheet() as main:
            with v.Row():
                for plot in viz_state.plots:
                    with v.Col(sm=1):
                        v.Switch(label=plot.name, v_model=plot.id in layout_ids, on_v_model=partial(toggle_layout, id=plot.id))
            sol.GridLayout(items=items, grid_layout=viz_state.layout, resizable=True, draggable=True, on_grid_layout=update_layout)

        return main
    return sol.Div()
