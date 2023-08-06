from typing import Any, Callable, Dict, Generator


class StrCommand(str):
    @classmethod
    def __get_validators__(cls) -> Generator[Callable[[str], "StrCommand"], None, None]:
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema: Dict[str, Any]) -> None:
        pass

    @classmethod
    def validate(cls, v: str) -> "StrCommand":
        if isinstance(v, bool):
            return StrCommand(str(v).lower())

        if not isinstance(v, str):
            raise ValueError("must be a string")

        if len(v) == 0:
            raise ValueError("ensure this value has at least 1 characters")

        if not (v.startswith("! ") or v[0].isalnum()):
            raise ValueError("command must start with an alphanumerical character or bang")

        if v.startswith("! "):
            if len(v) < len("! x"):
                raise ValueError("invalid command")

            first_bang_command_char = v[2]
            if not first_bang_command_char.isalnum():
                raise ValueError("invalid command")

        return StrCommand(v)
