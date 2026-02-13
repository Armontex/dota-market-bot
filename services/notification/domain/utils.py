from .exc import DomainValidationError


def non_empty_str(v: str) -> bool:
    return bool(v and v.strip())


def validate_optional_string(field_name: str, value: str | None) -> None:
    if value is not None:
        if not non_empty_str(value):
            raise DomainValidationError(field_name, "cannot be empty string")
