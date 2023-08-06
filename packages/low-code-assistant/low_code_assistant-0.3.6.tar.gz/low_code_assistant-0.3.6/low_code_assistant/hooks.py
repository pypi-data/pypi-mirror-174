from typing import Any, Callable, List, Optional, Tuple, TypeVar, Union, cast

import reacton
from IPython import get_ipython

import low_code_assistant.viz_reducer as vr

T = TypeVar("T")
U = TypeVar("U")
VizContextType = Tuple[vr.VizState, Callable[[vr.VizState], Any], Callable]
viz_context = reacton.create_context(cast(Optional[VizContextType], None))


def use_variable_watch(value, name: str):
    changed, set_changed = reacton.use_state(False)
    updater_default: List[Optional[Callable[[], None]]] = [None]
    updater, set_updater = reacton.use_state(updater_default)
    value, set_value = reacton.use_state(value, eq=lambda a, b: a is b)

    # first, ensure the user_ns is observable
    #     user_ns = get_ipython().user_ns
    #     if not isinstance(user_ns, observable_dict):
    #         get_ipython().user_ns = observable_dict(user_ns)
    #         user_ns = get_ipython().user_ns

    #     def observer(type, data):
    #         if type == '__setitem__':
    #             name_which_was_set, value_which_was_set = data
    #             def value_updater():
    #                 set_value(value_which_was_set)
    #                 set_changed(False)
    #                 set_updater(None)
    #             if name == name_which_was_set:
    #                 set_changed(True)
    #                 set_updater([value_updater])

    def watch_for_change():
        #         print("watch for change")
        current_value = get_ipython().user_ns[name]

        def value_updater():
            #             print("setting to", current_value)
            set_value(current_value)
            set_changed(False)
            set_updater([None])

        #             print("done!")
        if current_value is not value:
            set_changed(True)
            set_updater([value_updater])

    def watch():
        if not changed:
            ip = get_ipython()

            def cleanup():
                ip.events.unregister("post_execute", watch_for_change)

            ip.events.register("post_execute", watch_for_change)
            return cleanup

    reacton.use_effect(watch)
    return value, changed, updater[0]


def use_reducer_addon(reduce: Callable[[T, U], T], set_state: Callable[[Union[T, Callable[[T], T]]], None]) -> Callable[[U], None]:
    def dispatch(action: U):
        def state_updater(state: T):
            return reduce(state, action)

        set_state(state_updater)

    return dispatch


def provide_viz(default=vr.VizState()):
    viz_state, set_viz_state = reacton.use_state(default)
    viz_dispatch = use_reducer_addon(vr.viz_reducer, set_viz_state)
    viz_context.provide((viz_state, set_viz_state, viz_dispatch))


def use_viz():
    viz = reacton.use_context(viz_context)
    assert viz is not None
    return cast(VizContextType, viz)
