import logging,sys
from context import Context
from reader.dummy_reader import DummyReader
from parser.dummy_parser import DummyParser
from lister.dummy_lister import DummyLister

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(threadName)s %(levelname)s %(name)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    stream=sys.stdout)

context = Context()
context.register("reader", DummyReader)
context.register("parser", DummyParser)
context.register("lister", DummyLister)
context.start("dummy://list")
print context._addedDocs
