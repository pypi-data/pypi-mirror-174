import json
import pathlib

from deephaven.plugin import Registration
from deephaven.plugin.content import ContentPlugin

from importlib.resources import files, as_file
from contextlib import contextmanager
from typing import Generator

from .__info__ import (
    __distribution_path__,
)


class PlotlyJs(ContentPlugin):
    @contextmanager
    def distribution_path(self) -> Generator[pathlib.Path, None, None]:
        with as_file(files(__package__)) as package:
            yield package / __distribution_path__

    @property
    def type(self) -> str:
        return "js"

    @property
    def metadata(self):
        with self.distribution_path() as distribution_path:
            with open(distribution_path / "package.json") as package_json:
                return json.load(package_json)


class PlotlyJsRegistration(Registration):
    @classmethod
    def register_into(cls, callback: Registration.Callback) -> None:
        callback.register(PlotlyJs)
