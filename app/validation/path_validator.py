import os

from textual.validation import Validator, ValidationResult


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
