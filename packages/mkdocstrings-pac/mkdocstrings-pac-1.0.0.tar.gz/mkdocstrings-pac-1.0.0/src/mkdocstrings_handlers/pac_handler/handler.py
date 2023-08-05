"""This module implements a handler for PAC's LUA functions."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Optional, List

from mkdocstrings.handlers.base import BaseHandler
from mkdocstrings.loggers import get_logger
from dataclasses import dataclass

logger = get_logger(__name__)


@dataclass
class DocFunction:
    """Class for keeping track of an item in inventory."""
    name: str = ""
    docs: str = ""
    parameters: str = ""
    copy_parameters: str = ""
    returns: str = ""


class PACHandler(BaseHandler):
    """
        The PAC's LUA handler class.
    """

    def collect(self, identifier: str, config: dict) -> str:
        return identifier

    def get_name(self, name: str) -> str:
        result = name.replace('lua_state->set_function("', '')
        result = result.replace('"', '')
        result = result.replace(',', '')
        return result.strip()

    def get_parameters(self, parameters: str) -> str:
        result = parameters.replace('[](', '').replace(')', '')
        result = result.replace("const ", "")
        result = result.replace("std::string ", "String ")
        result = result.replace("&", "")
        result = result.replace("int ", "Number ")
        result = result.replace("float ", "Number ")
        result = result.replace("sol::function ", "Function ")

        return result.strip()

    def get_copy_parameters(self, parameters: str) -> str:
        result = self.get_parameters(parameters)
        result = result.replace("String ", "")
        result = result.replace("Number ", "")
        result = result.replace("Function ", "")
        result = result.replace("bool ", "")
        return result.strip()

    def get_docs(self, code: List[str], index: int) -> str:
        result = ""
        index -= 1

        while "///" in code[index]:
            result += code[index].replace("///", "").strip()
            index -= 1

        if result == "":
            return "Cool Documentation"

        return result.strip()

    def get_returns(self, code: List[str], index: int) -> str:
        result = ""
        index -= 1

        while "///" in code[index]:
            if "return" in code[index]:
                result += code[index].replace("///", "").strip()
            index -= 1

        if result == "":
            return "void"

        return result.strip()

    def render(self, data: str, config: dict) -> str:

        template = self.env.get_template("function_template.html")

        code_file = Path("../src/" + data).absolute()
        result = []
        with code_file.open() as f:
            code = f.readlines()

            for i, line in enumerate(code):
                if "set_function" in line:
                    pass
                    doc_obj = DocFunction()
                    doc_obj.name = self.get_name(code[i])
                    doc_obj.docs = self.get_docs(code, i)
                    doc_obj.parameters = self.get_parameters(code[i + 1])
                    doc_obj.copy_parameters = self.get_copy_parameters(code[i + 1])
                    doc_obj.returns = self.get_returns(code, i)
                    result.append(doc_obj)

        return template.render(
            **{"doc_objs": result},
        )


def get_handler(
    theme: str,
    custom_templates: Optional[str] = None,
    config_file_path: str | None = None,
    **config: Any,
) -> PACHandler:
    """Simply return an instance of `PACHandler`.

    Arguments:
        theme: The theme to use when rendering contents.

    Returns:
        An instance of `PACHandler`.
    """
    return PACHandler(
        handler="pac_handler",
        theme=theme,
    )
