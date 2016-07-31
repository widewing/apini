import hashlib
import re
import threading
import logging
from Queue import Queue


class Context:
    def __init__(self):
        self._logger = logging.getLogger("Context")
        self._readerClasses = []
        self._parserClasses = []
        self._listerClasses = []
        self._addedDocs = {}
        self._docQueue = Queue()  # (type, url) type 0: doc, type 1: index
        self._docThread = threading.Thread(target=Context._process_doc_queue, args=[self])
        self._docThread.start()
        self._recQueue = Queue()  # (docId, rec)
        self._recThread = threading.Thread(target=Context._process_rec_queue, args=[self])
        self._recThread.start()

    def start(self, url):
        self.add_index(url)

    def register(self, type_name, cls):
        self._get_type_classes(type_name).append(cls)

    def add_record(self, doc_id, record):
        self._recQueue.put((doc_id, record))

    def add_index(self, url):
        if url.strip() == "":
            self._logger.info("Empty URL")
            return
        self._docQueue.put((1, url))

    def add_doc(self, url):
        if url.strip() == "":
            self._logger.info("Empty URL")
            return
        self._docQueue.put((0, url))

    def _process_doc_queue(self):
        while True:
            (doc_type, url) = self._docQueue.get()
            if doc_type == 0:  # doc
                self._process_doc(url)
            elif doc_type == 1:  # index
                self._process_index(url)

    def _process_rec_queue(self):
        while True:
            (doc_id, record) = self._recQueue.get()
            self._process_record(doc_id, record)
    def _process_record(self, doc_id, record):
        self._logger.debug("added record for %s: %s" % (doc_id, record))

    def _process_index(self, url):
        if not self._record_doc(self._get_doc_id(url), url):
            return
        self._logger.info("list for %s" % url)
        reader_cls = self._match_url("reader", url)
        lister_cls = self._match_url("lister", url)
        reader = reader_cls(url)
        lister = lister_cls(self, self._get_doc_id(url))
        lister.list(reader.read())

    def _process_doc(self, url):
        doc_id = self._get_doc_id(url)
        if not self._record_doc(doc_id, url):
            return
        self._logger.info("Added document for URL: %s, ID=%s" % (url, doc_id))
        reader_cls = self._match_url("reader", url)
        parser_cls = self._match_url("parser", url)
        reader = reader_cls(url)
        parser = parser_cls(self, doc_id)
        parser.parse(reader.read())

    def _match_url(self, type_name, url):
        candidates = []
        for cls in self._get_type_classes(type_name):
            matcher = cls.matcher()
            if type(matcher) is str:
                matcher = re.compile(matcher)
            if matcher.match(url):
                candidates.append(cls)
        if len(candidates) == 0:
            raise LookupError("Cannot find %s for URL %s" % (type_name, url))
        candidates.sort(cmp=lambda a, b: cmp(a.priority(), b.priority()), reverse=True)
        return candidates[0]

    def _get_type_classes(self, type_name):
        if type_name not in ["reader", "parser", "lister"]:
            raise AttributeError("Not a recognized type: %s" % type_name)
        return getattr(self, "_%sClasses" % type_name)

    def _get_doc_id(self, url):
        return hashlib.sha1(url).hexdigest()[0:6]

    def _record_doc(self, doc_id, url):
        if doc_id in self._addedDocs:
            return False
        self._addedDocs[doc_id] = url
        return True
