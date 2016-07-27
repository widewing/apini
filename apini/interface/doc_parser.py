class DocParser:
    def __init__(self,context,doc_stream,doc_id):
        self._context = context
        self._doc_stream = doc_stream
        self._doc_id = doc_id

    @staticmethod
    def name(self):
        raise NotImplementedError('This method should be overridden by a subclass')

    @staticmethod
    def matcher(self):
        raise NotImplementedError('This method should be overridden by a subclass')

    def parse(self):
        raise NotImplementedError('This method should be overridden by a subclass')

    def _add_record(self,record):
        self._context.add_record(self._doc_id,record)

    def _add_doc(self,url):
        self._context.add_doc(url)