from apini.base import DocReader


class HttpReader(DocReader):
    @staticmethod
    def matcher():
        return "http://.*"

    @staticmethod
    def name():
        return "HttpReader"

    def __init__(self,url):
        DocReader.__init__(self,url)

    def read(self):
        pass