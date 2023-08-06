import abc

from . import Plugin

from importlib.resources import Package


class JsType(Plugin):
    @property
    @abc.abstractmethod
    def name(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def version(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def main(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def package(self) -> Package:
        pass
