class Context:
    def __init__(self):
        self._reader_classes = []
        self._parser_classes = []

    def start(self,url):
        self.add_doc(url)

    def add_record(self,doc_id,record):
        pass

    def add_doc(self,url):
        reader_cls = self._match_url(url,self._reader_classes)
        parser_cls = self._match_url(url,self._parser_classes)
        reader = reader_cls(url)
        parser = parser_cls(self,self._get_or_new_doc_id(url))
        parser.parse(reader.read())

    def _register_parser(self,parser):
        self._parsers.append(parser)

    def _register_reader(self,reader):
        self._readers.append(reader)

    def _match_url(self,url,list):
        pass

    def _get_or_new_doc_id(self,url):
        pass