from apini.base import DocLister


class DummyLister(DocLister):
    @staticmethod
    def matcher():
        return "dummy://list"

    @staticmethod
    def name():
        return "DummyParser"

    def __init__(self, context, doc_id):
        DocLister.__init__(self, context, doc_id)

    def list(self, doc):
        while True:
            line = doc.readline()
            if line == "":
                return
            if line.startswith("dummy://list"):
                self._add_index(line)
            else:
                self._add_doc(line)

