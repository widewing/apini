from apini.base import DocParser


class DummyParser(DocParser):
    @staticmethod
    def matcher():
        return "dummy://doc/.*"

    @staticmethod
    def name():
        return "DummyParser"

    def __init__(self, context, doc_id):
        DocParser.__init__(self, context, doc_id)

    def parse(self, doc):
        while True:
            line = doc.readline()
            if line == "":
                return
            self._add_record(line.strip())

