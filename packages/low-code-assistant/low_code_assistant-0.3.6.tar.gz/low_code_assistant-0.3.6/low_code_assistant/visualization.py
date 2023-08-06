# stand alone version for Visualizations

from typing import Any, Callable

import solara.components.datatable as dt
from solara.alias import reacton
from solara.alias import rv as v
from solara.alias import sol

import low_code_assistant.viz_reducer as vr
from low_code_assistant.hooks import use_variable_watch
from low_code_assistant.util import find_variable_name

from .hooks import provide_viz, use_viz
from .plot_builder import Visualizations


@reacton.component
def DataTable(df, on_drop_column: Callable[[str], Any] = None, on_filter_value: Callable[[str, int], Any] = None):
    def on_local_on_drop_column(column):
        if on_drop_column:
            on_drop_column(column)

    def on_local_filter_value(column, row_index):
        if on_filter_value:
            on_filter_value(column, row_index)

    column_actions = [sol.ColumnAction(icon="mdi-table-column-remove", name="drop column", on_click=on_local_on_drop_column)]
    cell_actions = [sol.CellAction(icon="mdi-filter", name="Filter values like this", on_click=on_local_filter_value)]
    return dt.DataTable(df, column_actions=column_actions, cell_actions=cell_actions, items_per_page=10, scrollable=True)


@reacton.component
def Viz(df):
    provide_viz()
    viz_state, set_viz_state, viz_dispatch = use_viz()

    def once():
        viz_dispatch(vr.ActionDF(df))

    reacton.use_memo(once, [])

    name = reacton.use_memo(lambda: find_variable_name(df))
    df, changed, updater = use_variable_watch(df, name)

    def update_df():
        viz_dispatch(vr.ActionDF(df))

    reacton.use_memo(update_df, [id(df)])

    show_df = True
    breakpoints = False
    with v.Sheet() as main:
        with v.Row(no_gutters=not breakpoints):
            with v.Col(sm=12, lg=5 if breakpoints else 12):
                with v.Card(class_="ma-0"):
                    if changed:
                        v.CardTitle(children=[f"Dataframe: {name} (changed)"])
                    else:
                        v.CardTitle(children=[f"Dataframe: {name}"])

                    with v.CardText(class_="ma-0"):
                        if changed:
                            msg = f"The dataframe with name {name!r} has changed, do you want to reload"
                            sol.Warning(msg)
                            sol.Button("Reload", icon_name="mdi-refresh", on_click=updater)
                        if show_df:
                            if viz_state.df.get() is not None:
                                Visualizations(viz_state)
    return main
