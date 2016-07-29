
class Matchable:
    def __init__(self):
        pass

    @staticmethod
    def name():
        raise NotImplementedError('This method should be overridden by a subclass')

    @staticmethod
    def matcher():
        raise NotImplementedError('This method should be overridden by a subclass')

    @staticmethod
    def priority():
        return 1


class DocReader(Matchable):
    def __init__(self,url):
        Matchable.__init__(self)
        self._url = url

    def read(self):
        raise NotImplementedError('This method should be overridden by a subclass')


class DocParser(Matchable):
    def __init__(self,context,doc_id):
        Matchable.__init__(self)
        self._context = context
        self._docId = doc_id

    def parse(self,stream):
        raise NotImplementedError('This method should be overridden by a subclass')

    def _add_record(self,record):
        self._context.add_record(self._docId,record)


class DocLister(Matchable):
    def __init__(self,context,doc_id):
        Matchable.__init__(self)
        self._context = context
        self._docId = doc_id

    def list(self,stream):
        raise NotImplementedError('This method should be overridden by a subclass')

    def _add_doc(self,url):
        self._context.add_doc(url)

    def _add_index(self,url):
        self._context.add_index(url)