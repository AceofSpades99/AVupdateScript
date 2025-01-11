import os.path

import dotenv
from rich.text import Text
from textual import on
from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import Screen
from textual.validation import ValidationResult, Validator
from textual.widgets import Input, Button, Label

from app.management.env_manager import platform_verify_support


# A custom validator
class PathValidator(Validator):
    def validate(self, path: str) -> ValidationResult:
        if os.path.exists(path):
            if os.path.isdir(path):
                if os.access(path, os.W_OK):
                    return self.success()
                else:
                    return self.failure('No puedo crear archivos ahi')
            else:
                return self.failure('La ruta no es un directorio')
        else:
            if len(path.strip()) == 0:
                return self.failure('La ruta no puede estar en blanco')
            else:
                return self.failure('La ruta no existe')


class SettingsScreen(Screen):
    def __init__(self, remember: bool = True, *args, **kwargs) -> None:
        self.remember = remember
        self.env_path = platform_verify_support()
        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        folder = dotenv.get_key(self.env_path, 'save_path')
        if folder:
            yield Label(Text.assemble(('Carpeta de guardado actual: ', 'bold cyan'), folder), id='folder_label')
        yield Grid(
            Input(
                placeholder='Carpeta hacia donde descargar',
                validators=[
                    PathValidator()
                ],
                id='input'
            ),
            Label('', id='error_label'),
            Grid(
                Grid(
                    Button('Aceptar', variant='success', id='accept'),
                    id='grid_accept'
                ),
                Grid(
                    Button('Cancelar', variant='error', id='cancel'),
                    id='grid_cancel'
                ),
                id='buttons'
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
        if Input.is_valid:
            dotenv.set_key(self.env_path, 'save_path', self.query_one(Input).value)
            self.app.switch_mode('dashboard')

    @on(Button.Pressed, '#cancel')
    def ignore_changes(self):
        self.app.switch_mode('dashboard')
