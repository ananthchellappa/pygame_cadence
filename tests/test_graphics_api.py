import pytest

from command_context import CommandContext, FontTarget
from document import Document
from graphics_api import MAX_FONT_SIZE, MIN_FONT_SIZE, build_namespace


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


def _ctx_with_font_target():
    ctx = CommandContext(document=Document())
    size = {"value": 10}
    ctx.font_targets["Command"] = FontTarget(
        get=lambda: size["value"],
        set=lambda n: size.__setitem__("value", n),
    )
    return ctx, size


def test_hi_app_set_font_dispatches_to_registered_setter():
    ctx, size = _ctx_with_font_target()
    ns = build_namespace(ctx)
    ns["hi_app_set_font"]("Command", 14)
    assert size["value"] == 14


def test_hi_app_get_font_returns_current_size():
    ctx, size = _ctx_with_font_target()
    size["value"] = 11
    ns = build_namespace(ctx)
    assert ns["hi_app_get_font"]("Command") == 11


def test_hi_app_set_font_is_case_insensitive():
    ctx, size = _ctx_with_font_target()
    ns = build_namespace(ctx)
    ns["hi_app_set_font"]("COMMAND", 12)
    assert size["value"] == 12
    ns["hi_app_set_font"]("command", 16)
    assert size["value"] == 16


def test_hi_app_get_font_is_case_insensitive():
    ctx, size = _ctx_with_font_target()
    size["value"] = 13
    ns = build_namespace(ctx)
    assert ns["hi_app_get_font"]("command") == 13
    assert ns["hi_app_get_font"]("COMMAND") == 13


def test_get_set_round_trip():
    ctx, _ = _ctx_with_font_target()
    ns = build_namespace(ctx)
    current = ns["hi_app_get_font"]("Command")
    ns["hi_app_set_font"]("Command", current + 2)
    assert ns["hi_app_get_font"]("Command") == current + 2


def test_hi_app_set_font_unknown_target_lists_valid_targets():
    ctx, _ = _ctx_with_font_target()
    ns = build_namespace(ctx)
    with pytest.raises(ValueError, match="Command"):
        ns["hi_app_set_font"]("Schematic", 12)


def test_hi_app_get_font_unknown_target_lists_valid_targets():
    ctx, _ = _ctx_with_font_target()
    ns = build_namespace(ctx)
    with pytest.raises(ValueError, match="Command"):
        ns["hi_app_get_font"]("Schematic")


def test_hi_app_set_font_rejects_non_string_target():
    ctx, _ = _ctx_with_font_target()
    ns = build_namespace(ctx)
    with pytest.raises(ValueError):
        ns["hi_app_set_font"](123, 12)


@pytest.mark.parametrize("bad_size", [MIN_FONT_SIZE - 1, MAX_FONT_SIZE + 1, 0, -1, 1000])
def test_hi_app_set_font_rejects_out_of_range_size(bad_size):
    ctx, _ = _ctx_with_font_target()
    ns = build_namespace(ctx)
    with pytest.raises(ValueError, match=str(MIN_FONT_SIZE)):
        ns["hi_app_set_font"]("Command", bad_size)


@pytest.mark.parametrize("bad_size", [10.5, "12", None, True, False])
def test_hi_app_set_font_rejects_non_integer_size(bad_size):
    ctx, _ = _ctx_with_font_target()
    ns = build_namespace(ctx)
    with pytest.raises(ValueError):
        ns["hi_app_set_font"]("Command", bad_size)


def test_hi_app_set_font_accepts_boundary_sizes():
    ctx, size = _ctx_with_font_target()
    ns = build_namespace(ctx)
    ns["hi_app_set_font"]("Command", MIN_FONT_SIZE)
    assert size["value"] == MIN_FONT_SIZE
    ns["hi_app_set_font"]("Command", MAX_FONT_SIZE)
    assert size["value"] == MAX_FONT_SIZE
