import dotenv
from rich.style import Style
from rich.text import Text
from textual import on
from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import ModalScreen
from textual.widgets import Input, Button, Label

from app.management.platform_support import platform_verify_support
from app.validation.path_validator import PathValidator


class FirstConfig(ModalScreen[bool]):
    def __init__(self, remember: bool = True, *args, **kwargs) -> None:
        self.remember = remember
        self.env_path = platform_verify_support()
        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        yield Grid(
            Grid(
                Label(
                    Text(
                        'Provea la direccion de la carpeta donde se deben guardar los archivos',
                        Style(
                            color='cyan',
                        ),
                    ),
                    id='folder_label'
                ),
                classes='center'
            ),
            Input(
                placeholder='Carpeta hacia donde descargar',
                validators=[
                    PathValidator()
                ],
                valid_empty=False,
                id='input',
            ),
            Label('', id='error_label'),
            Grid(
                Button('Aceptar', variant='success', id='accept'),
                classes='center',
            ),
            id='container',
        )

    @on(Input.Changed, '#input')
    def show_invalid_reasons(self, event: Input.Changed) -> None:
        # Updating the UI to show the reasons why validation failed
        if not event.validation_result.is_valid:
            self.query_one('#error_label').update(event.validation_result.failure_descriptions[0])
        else:
            self.query_one('#error_label').update('')

    @on(Input.Submitted, '#input')
    @on(Button.Pressed, '#accept')
    def save_changes(self):
        value = self.query_one(Input).value
        if Input.is_valid:
            if value:
                dotenv.set_key(self.env_path, 'save_path', value)
                self.dismiss()
            else:
                self.query_one('#error_label').update('La ruta no puede estar en blanco')
