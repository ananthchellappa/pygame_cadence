import builtins as _builtins

from command_context import CommandContext


def build_namespace(context: CommandContext) -> dict:
    ns: dict = dict(vars(_builtins))

    def move_to(x, y):
        context.document.move_to(x, y)

    ns["move_to"] = move_to
    return ns
