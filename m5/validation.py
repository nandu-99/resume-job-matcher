"""Request bounds shared by the interface and direct inference callers."""

import unicodedata


MAX_INPUT_CHARACTERS = 50_000


class InputValidationError(ValueError):
    """Input that the user can correct without changing the model."""


def validate_inputs(resume_text: str, job_text: str) -> None:
    # These checks enforce request bounds; they do not assess resume quality or relevance.
    for name, text in (("Resume", resume_text), ("Job description", job_text)):
        if not isinstance(text, str):
            raise TypeError(f"{name} must be a string.")
        if len(text) > MAX_INPUT_CHARACTERS:
            raise InputValidationError(
                f"{name} is too long. Use at most {MAX_INPUT_CHARACTERS:,} characters."
            )
        if not text.strip():
            raise InputValidationError(f"{name} must contain text.")
        if any(unicodedata.category(character) == "Cc" and character not in "\n\r\t"
               for character in text):
            raise InputValidationError(f"Remove unsupported control characters from the {name.lower()}.")
        if not any(character.isalnum() for character in text):
            raise InputValidationError(f"{name} must include letters or numbers.")
