from ast import ClassDef


class ZincFormatException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class UnitNotFound(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class TimeZoneNotFound(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class RefNotFound(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class EntityNotFound(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)