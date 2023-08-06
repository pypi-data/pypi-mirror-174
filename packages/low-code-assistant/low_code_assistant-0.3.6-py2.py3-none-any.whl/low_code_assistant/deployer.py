import os
import shutil
import subprocess
import threading
import time
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Optional, Sequence, cast

import humanize
import solara.util
from dateutil import parser  # type: ignore
from solara import Result, use_thread
from solara.alias import reacton
from solara.alias import rv as v
from solara.alias import sol

from low_code_assistant.settings import settings

from .assistant import mixpanel
from .domino_api import get_domino_api

run_sh_content_template = """#!/usr/bin/env bash
SOLARA_APP=low_code_assistant.app_entrypoint SOLARA_THEME_VARIANT={theme_variant} SOLARA_THEME_LOADER={theme_loader} uvicorn solara.server.starlette:app\\
    --loop asyncio\\
    --host=0.0.0.0 --port=8888"""

run_py_content = """import low_code_assistant

app = low_code_assistant.Dominocode()
"""


deploy_sync = solara.util.load_file_as_data_url(Path(__file__).parent / "deploy-sync.png", "image/png")
deploy_start = solara.util.load_file_as_data_url(Path(__file__).parent / "deploy-start.png", "image/png")
deploy_open = solara.util.load_file_as_data_url(Path(__file__).parent / "deploy-open.png", "image/png")


class AppStatus(str, Enum):
    NON_EXISTENT = "Non existent"
    PENDING = "Pending"
    PREPARING = "Preparing"
    RUNNING = "Running"
    STOPPED = "Stopped"
    QUEUED = "Queued"
    FAILED = "Failed"


class AppOperation(str, Enum):
    START = "Start"
    STOP = "Stop"


def app_state(enable_polling):
    current_operation, set_current_operation = reacton.use_state(cast(Optional[AppOperation], None))
    restart_sequence, set_restart_sequence = reacton.use_state(cast(Sequence[AppOperation], ()))
    exec_error, set_exec_error = reacton.use_state(cast(Optional[Exception], None))

    def status_loop(cancel: threading.Event):
        if not enable_polling:
            return
        while not cancel.is_set():
            try:
                status = get_domino_api().get_app_status()
                yield AppStatus.NON_EXISTENT if status is None else status
            except Exception:
                pass
            time.sleep(0.5)

    status_result: Result[AppStatus] = sol.use_thread(status_loop, dependencies=[enable_polling])

    def execute_operation(cancel: threading.Event):
        if current_operation is not None:
            set_exec_error(None)
        if not cancel.is_set():
            if current_operation == AppOperation.START:
                hardware_tire_id = settings.domino_hardware_tier_id or get_domino_api().get_default_hardware_tier_id()
                get_domino_api().app_publish(hardwareTierId=hardware_tire_id)
            elif current_operation == AppOperation.STOP:
                get_domino_api().app_unpublish()

    execute_operation_result: sol.Result = sol.use_thread(execute_operation, intrusive_cancel=True, dependencies=[current_operation])

    def handle_execution_error():
        if execute_operation_result.error:
            set_exec_error(execute_operation_result.error)
            set_current_operation(None)

    reacton.use_memo(handle_execution_error, [execute_operation_result])

    def check_operation_done():
        if (current_operation == AppOperation.START and status_result.value in [AppStatus.RUNNING]) or (
            current_operation == AppOperation.STOP and status_result.value not in [AppStatus.RUNNING, AppStatus.FAILED]
        ):
            set_current_operation(None)

    reacton.use_memo(check_operation_done, [current_operation, status_result.value])

    def update_restart():
        if not current_operation and restart_sequence:
            head, *tail = restart_sequence
            set_current_operation(head)
            set_restart_sequence(tail)

    reacton.use_memo(update_restart, [current_operation, restart_sequence])

    def app_start():
        if status_result is None or current_operation:
            return
        set_current_operation(AppOperation.START)

    def app_stop():
        if status_result is None or current_operation:
            return
        set_current_operation(AppOperation.STOP)

    def app_restart():
        if status_result is None or current_operation:
            return
        set_restart_sequence((AppOperation.STOP, AppOperation.START))

    return status_result, current_operation, app_start, app_stop, app_restart, exec_error


@reacton.component
def AppStarter(back, next):
    app_status_current, current_operation, app_start, app_stop, app_restart, exec_error = app_state(True)

    app_info = reacton.use_memo(get_domino_api().get_app_info, [app_status_current.value])

    # app_id_result = use_app_id()
    app_id_result: sol.Result = sol.use_thread(get_domino_api().get_app_id, [bool(app_status_current.value == AppStatus.RUNNING)])
    url = f"/modelproducts/{app_id_result.value}"

    def with_tracking(fn, event):
        def wrapper():
            fn()
            mixpanel.api.track_with_defaults(
                "interaction",
                {
                    "section": "deploy",
                    "type": "server state change",
                    "server": event,
                },
            )

        return wrapper

    with v.Card() as main:
        if app_status_current.error:
            sol.Error(f"Error reading current status: {app_status_current.error}")
            sol.Button("Retry", on_click=app_status_current.retry)
        else:
            if app_info:
                try:
                    last_deploy = humanize.naturaltime(datetime.now(timezone.utc) - parser.parse(app_info[0]["created"]))
                except Exception as e:
                    last_deploy = f"error: {type(e).__name__} - {str(e)}"
                sol.Div(children=f"Last deployed: {last_deploy}").key("app_info")

            if current_operation or app_status_current.value in [None, AppStatus.PENDING, AppStatus.PREPARING, AppStatus.QUEUED]:
                v.ProgressLinear(indeterminate=True)
            if exec_error:
                sol.Error(f"Error: {exec_error}")
            if app_status_current.value is None:
                sol.Info("Requesting server status")
            else:
                sol.Info(f"Server status: {app_status_current.value}")

        sol.Button("Back to Sync filesystem", on_click=back, class_="ma-1", icon_name="mdi-keyboard-backspace")

        def deploy():
            if app_status_current.value in [None, AppStatus.STOPPED, AppStatus.FAILED, AppStatus.NON_EXISTENT]:
                app_start()
            elif app_status_current.value in [AppStatus.RUNNING]:
                app_restart()

        sol.Button(
            "Deploy app",
            on_click=with_tracking(deploy, "deploy"),
            color="primary",
            disabled=bool(current_operation) or app_status_current.value in [AppStatus.PENDING, AppStatus.PREPARING, AppStatus.QUEUED],
            class_="ma-1",
            icon_name="mdi-rocket",
        )

        sol.Button(
            "View app",
            class_="ma-1",
            icon_name="mdi-application",
            disabled=bool(current_operation) or app_status_current.value not in [AppStatus.RUNNING],
            href=url,
            target="_blank",
            on_click=lambda: mixpanel.api.track_with_defaults(
                "interaction",
                {
                    "section": "deploy",
                    "type": "view app",
                },
            ),
        )
    return main


@reacton.component
def ScriptWriter(next):
    root = Path(settings.domino_working_dir)
    path = root / "app.sh"
    theme_variant, set_theme_variant = reacton.use_state("light", key="theme-variant")
    run_sh_content = run_sh_content_template.format(
        theme_variant=theme_variant,
        theme_loader="plain",
    ).encode("utf8")
    current_run_sh_content = sol.use_file_content(path)
    write_error, set_write_error = reacton.use_state(cast(Optional[Exception], None))
    write_script_counter, set_write_script_counter = reacton.use_state(0, key="write-script-counter")

    def write_scripts_thread():
        if write_script_counter > 0:
            try:
                with open(path, "wb") as f:
                    f.write(run_sh_content)
                set_write_error(None)
            except Exception as e:
                set_write_error(e)

    use_thread(write_scripts_thread, dependencies=[write_script_counter])
    script_ok = current_run_sh_content.exists and (current_run_sh_content.value == run_sh_content)

    def write_scripts():
        mixpanel.api.track_with_defaults(
            "interaction",
            {
                "section": "deploy",
                "type": "write script",
            },
        )
        set_write_script_counter(write_script_counter + 1)

    with v.Card() as main:
        with sol.Padding(2):
            with sol.Details("Settings"):
                with sol.GridFixed(2):
                    sol.Markdown("**Theme variant**")
                    with sol.ToggleButtonsSingle(value=theme_variant, on_value=set_theme_variant):
                        sol.Button(icon_name="mdi-white-balance-sunny", value="light")
                        sol.Button(icon_name="mdi-weather-night", value="dark")
                        sol.Button(icon_name="mdi-theme-light-dark", value="auto")
            with sol.Details("run.sh"):
                sol.Preformatted(run_sh_content.decode("utf8"))
            if write_error:
                sol.Error(f"Error writing script files: {write_error}")
            elif not current_run_sh_content.exists:
                sol.Warning(f"Script {path} file does not exist yet")
            elif current_run_sh_content.error:
                sol.Error(f"Error reading existing script: {current_run_sh_content.error}")
            else:
                if script_ok:
                    sol.Success(f"Script {path} is up to date")
                else:
                    sol.Warning(f"Script {path} requires an update")
            sol.Button("Write script", on_click=write_scripts, disabled=script_ok, class_="ma-1", icon_name="mdi-content-save")
            sol.Button("Continue", color="primary", on_click=next, disabled=not script_ok, class_="ma-1", icon_name="mdi-check")
    return main


def check_code(notebook_saved):
    def run():
        if notebook_saved:
            proc = subprocess.run(
                ["python", "-m", "low_code_assistant.app_entrypoint"], cwd=settings.domino_working_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            if proc.returncode != 0:
                raise Exception(proc.stderr.decode("utf-8").split("\n")[-2])

    return sol.use_thread(run, dependencies=[notebook_saved])


@reacton.component
def Deployer(opened=False, notebook_path: str = ""):

    update, set_update = reacton.use_state(0, key="update")  # to force manual update
    step, set_step = reacton.use_state(1, key="step")
    notebook_saved, set_notebook_saved = reacton.use_state(False)
    error, set_error = reacton.use_state(cast(Optional[Exception], None))

    def save_and_copy_notebook():
        try:
            if not opened:
                set_notebook_saved(False)
                return
            if notebook_saved:
                root = Path(settings.domino_working_dir)
                notebook_local_path = Path(os.getcwd()) / Path(notebook_path).name
                shutil.copy2(notebook_local_path, root / settings.domino_notebook_deploy_filename)
                return
            from low_code_assistant.assistant import notebook

            assert notebook.save_notebook

            def on_save(is_saved):
                if is_saved:
                    set_notebook_saved(True)
                else:
                    set_error(Exception("could not save notebook"))

            notebook.save_notebook(on_save)
        except Exception as e:
            set_error(e)

    reacton.use_effect(save_and_copy_notebook, dependencies=[opened, step, notebook_saved])
    check_code_result = check_code(notebook_saved)

    def on_step_change():
        steps = ["Create app", "Sync filesystem'", "Start app", "View app"]
        mixpanel.api.track_with_defaults(
            "interaction",
            {
                "section": "deploy",
                "type": "step",
                "step": steps[step - 1],
            },
        )

    reacton.use_memo(on_step_change, [step])

    if error:
        return sol.Error(f"Error: {error}")

    with v.Sheet(class_="px-2") as main:

        if check_code_result.state == sol.ResultState.FINISHED:
            with v.Stepper(v_model=step, on_v_model=set_step).key("ok"):
                with v.StepperHeader():
                    with v.StepperStep(children=["Create app"], step=1, complete=step > 1):
                        pass
                    with v.StepperStep(children=["Sync filesystem"], step=2, complete=step > 2):
                        pass
                    with v.StepperStep(children=["Start app"], step=3, complete=step > 3):
                        pass
                with v.StepperItems():
                    with v.StepperContent(step=1):
                        if step == 1:
                            ScriptWriter(next=lambda: set_step(2))
                    with v.StepperContent(step=2):
                        with v.Card():
                            sol.Info("Goto the top left, and click the `Sync all Changes` button as shown in the screenshot below")
                            v.Img(src=deploy_sync, style_="height: 455px", contain=True)
                            sol.Button("Back to `Create app`", on_click=lambda: set_step(1), class_="ma-1", icon_name="mdi-keyboard-backspace")
                            sol.Button("Continue", color="primary", on_click=lambda: set_step(3), class_="ma-1", icon_name="mdi-check")
                    with v.StepperContent(step=3):
                        if step == 3:
                            AppStarter(back=lambda: set_step(2), next=lambda: set_step(4))
        elif check_code_result.state == sol.ResultState.RUNNING:
            with sol.Div().key("checking"):
                sol.Div(children=["Validating app..."])
                v.ProgressLinear(indeterminate=True)
        elif check_code_result.state == sol.ResultState.ERROR:
            sol.Error(f"Error: {check_code_result.error}").key("code error")
    return main


# app = Deployer()
