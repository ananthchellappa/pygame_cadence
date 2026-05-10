import builtins as _builtins


def build_namespace(canvas) -> dict:
    ns: dict = dict(vars(_builtins))

    def move_to(x, y):
        canvas.move_to(x, y)

    ns["move_to"] = move_to
    return ns
