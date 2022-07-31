from ast import ClassDef


class ZincFormatException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class UnitNotFound(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)