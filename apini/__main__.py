from context import Context
from reader.dummy_reader import DummyReader
from parser.dummy_parser import DummyParser
from lister.dummy_lister import DummyLister

context = Context()
context.register("reader",DummyReader)
context.register("parser",DummyParser)
context.register("lister",DummyLister)
context.start("dummy://list")
print context._added_docs