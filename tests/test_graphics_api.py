from command_context import CommandContext
from document import Document
from graphics_api import build_namespace


def test_namespace_exposes_move_to():
    ns = build_namespace(CommandContext(document=Document()))
    assert callable(ns.get("move_to"))


def test_move_to_delegates_to_document():
    doc = Document()
    ns = build_namespace(CommandContext(document=doc))
    ns["move_to"](10, 20)
    assert doc.cursor == (10, 20)


def test_namespace_includes_builtins():
    ns = build_namespace(CommandContext(document=Document()))
    assert ns.get("print") is print
    assert "len" in ns
