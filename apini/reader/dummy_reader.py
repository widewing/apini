from StringIO import StringIO
from apini.base import DocReader


class DummyReader(DocReader):
    @staticmethod
    def matcher():
        return "dummy://.*"

    @staticmethod
    def name():
        return "DummyReader"

    def __init__(self,url):
        DocReader.__init__(self,url)

    def read(self):
        if self._url.startswith("dummy://list"):
            return StringIO("dummy://doc/testdoc\n"
                            "dummy://doc/testdoc2\n"
                            "dummy://list/1\n"
                            "dummy://list/2")
        return StringIO("This is a test")
