import dataclasses
import uuid
from dataclasses import asdict, dataclass, field, replace
from typing import Any, Callable, Dict, List, Optional, Union


class EqWrapper:
    def __init__(self, obj):
        self.obj = obj

    def get(self):
        return self.obj


@dataclass(frozen=True)
class PlotState:
    name: str = "Untitled"
    plot_type: Optional[str] = None
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    col_args: Dict = field(default_factory=lambda: {})
    df_var_name: Optional[str] = None
    plot_var_name: Optional[str] = None
    crossfilter_enabled: bool = False


@dataclass(frozen=True)
class VizState:
    df: EqWrapper = field(default_factory=lambda: EqWrapper(None))
    columns: Optional[List[str]] = None
    plots: Optional[List[PlotState]] = None
    error: Optional[str] = None
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    layout: List[Dict] = field(default_factory=lambda: [])


def viz_reducer(state: VizState, event: "Action") -> VizState:
    return event.handle(state)


@dataclass(frozen=True)
class Action:
    def handle(self, state: VizState) -> VizState:
        pass


@dataclass(frozen=True)
class ActionDF(Action):
    df: Any

    def handle(self, state):
        columns = self.df.columns.tolist() if self.df is not None else None
        plots = state.plots
        if self.df is not None and state.plots is None and len(columns) > 2:
            plots = [PlotState(name="plot-1", plot_type="scatter", col_args={"x": columns[0], "y": columns[2], "color": columns[1]})]
        return replace(state, df=EqWrapper(self.df), columns=columns, plots=plots)


def update_in(data: Any, path: List[Union[int, str]], fn: Callable[[Any], Any]) -> Any:
    if not path:
        return fn(data)
    else:
        if isinstance(data, list) and isinstance(path[0], int):
            idx = path[0]
            if idx is None or idx >= len(data):  # append
                new_item = update_in(None, path[1:], fn)
                return data + [new_item]
            if idx < 0:  # prepend
                new_item = update_in(None, path[1:], fn)
                return [new_item] + data

            new_item = update_in(data[idx], path[1:], fn)
            return data[:idx] + [new_item] + data[idx + 1 :]
        elif dataclasses.is_dataclass(data) and isinstance(path[0], str):
            attr = path[0]
            new_item = update_in(getattr(data, attr), path[1:], fn)
            return replace(data, **{attr: new_item})
        elif isinstance(data, dict):
            key = path[0]
            new_item = update_in(data.get(key), path[1:], fn)
            return {**data, key: new_item}
        raise Exception("can't update.")


def set_in(data: Any, path: List[Union[int, str]], value: Any) -> Any:
    return update_in(data, path, lambda _: value)


def append(data, item):
    return data + [item]


def remove(data, index):
    return data[:index] + data[index + 1 :]


@dataclass(frozen=True)
class ActionSetColArg(Action):
    index: int
    arg: str
    value: Any

    def handle(self, state):
        return set_in(state, ["plots", self.index, "col_args", self.arg], self.value)


@dataclass(frozen=True)
class ActionSetPlotType(Action):
    index: int
    plot_type: str

    def handle(self, state):
        return set_in(state, ["plots", self.index, "plot_type"], self.plot_type)


@dataclass(frozen=True)
class ActionAddPlot(Action):
    plot_state: PlotState

    def handle(self, state):
        return replace(state, plots=state.plots + [self.plot_state])


@dataclass(frozen=True)
class ActionRemovePlot(Action):
    index: int

    def handle(self, state):
        return update_in(state, ["plots"], lambda plots: remove(plots, self.index))


@dataclass(frozen=True)
class ActionReset(Action):
    def handle(self, state):
        return VizState()


def to_json(obj):
    if isinstance(obj, PlotState):
        return {"type_plot_state": asdict(obj)}


def from_json(dct):
    if "type_plot_state" in dct:
        res = PlotState(**dct["type_plot_state"])
        return res
