import hashlib
import re


class Context:
    def __init__(self):
        self._reader_classes = []
        self._parser_classes = []
        self._lister_classes = []

        self._added_docs = {}

    def start(self,url):
        self.add_index(url)

    def add_record(self,doc_id,record):
        print "added record for %s: %s"%(doc_id,record)

    def add_index(self,url):
        if not self._record_doc(self._get_doc_id(url),url):
            return
        print "list for %s"%url
        reader_cls = self._match_url("reader",url)
        lister_cls = self._match_url("lister",url)
        reader = reader_cls(url)
        lister = lister_cls(self,self._get_doc_id(url))
        lister.list(reader.read())

    def add_doc(self,url):
        if not self._record_doc(self._get_doc_id(url),url):
            return
        reader_cls = self._match_url("reader",url)
        parser_cls = self._match_url("parser",url)
        reader = reader_cls(url)
        parser = parser_cls(self,self._get_doc_id(url))
        parser.parse(reader.read())

    def register(self,type_name,cls):
        self._get_type_classes(type_name).append(cls)

    def _match_url(self,type_name,url):
        candidates = []
        for cls in self._get_type_classes(type_name):
            matcher = cls.matcher()
            if type(matcher) is str:
                matcher = re.compile(matcher)
            if matcher.match(url):
                candidates.append(cls)
        if len(candidates) == 0:
            raise LookupError("Cannot find %s for URL %s"%(type_name,url))
        candidates.sort(cmp=lambda a,b:cmp(a.priority(),b.priority()),reverse=True)
        return candidates[0]

    def _get_type_classes(self,type_name):
        if type_name not in ["reader","parser","lister"]:
            raise AttributeError("Not a recognized type: %s"%type_name)
        return getattr(self,"_%s_classes"%type_name)

    def _get_doc_id(self,url):
        return hashlib.sha1(url).hexdigest()[0:6]

    def _record_doc(self,doc_id,url):
        if doc_id in self._added_docs:
            return False
        self._added_docs[doc_id] = url
        return True