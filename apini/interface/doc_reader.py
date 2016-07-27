class DocReader:
    def __init__(self,url):
        self._url = url

    @staticmethod
    def name(self):
        raise NotImplementedError('This method should be overridden by a subclass')

    @staticmethod
    def matcher(self):
        raise NotImplementedError('This method should be overridden by a subclass')

    @staticmethod
    def priority(self):
        return 1

    def read(self):
        raise NotImplementedError('This method should be overridden by a subclass')