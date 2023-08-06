import os

import reacton
import reacton.ipyvuetify as v
import solara as sol
from solara.components.file_browser import FileBrowser
from solara.components.file_drop import FileDrop

from low_code_assistant.util import DominoHeader, copy_upload


@reacton.component
def LoadDataset(on_file_name):
    dialog_open, set_dialog_open = reacton.use_state(False, key="dialog_open")
    progress, set_progress = reacton.use_state(0, key="progress")

    def toggle_dialog():
        set_dialog_open(not dialog_open)

    def handle_file_name(file):
        if file:
            on_file_name(file)
            set_dialog_open(False)

    def handle_file_upload(file):
        dest_name = copy_upload(file["file_obj"], file["name"])
        on_file_name(dest_name)

    with v.Sheet() as main:
        with sol.Div(style_="display: flex; flex-direction: row"):
            sol.Button(
                "Browse disk",
                color="primary",
                icon_name="mdi-harddisk",
                on_click=toggle_dialog,
            )
        with v.Dialog(
            v_model=dialog_open,
            max_width="500px",
            on_v_model=lambda v: set_dialog_open(v),
        ):
            with v.Card(class_="low_code_assistant-file-dialog"):
                DominoHeader(title="Select Datasat")
                with v.CardText(style_="width: unset, height:400px"):
                    FileBrowser(
                        start_directory=os.getcwd(),
                        on_file_name=handle_file_name,
                    ).key("FileBrowser")
        FileDrop(
            label="Drop dataset here",
            on_total_progress=set_progress,
            on_file=handle_file_upload,
        )
        v.ProgressLinear(value=progress)

    return main
