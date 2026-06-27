from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "geo_agent"


class PublicFunctionVisitor(ast.NodeVisitor):
    def __init__(self, path: Path) -> None:
        self.path = path
        self.failures: list[str] = []

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        if node.name.startswith("_"):
            self.generic_visit(node)
            return
        missing = [arg.arg for arg in node.args.args if arg.arg != "self" and arg.annotation is None]
        missing.extend(arg.arg for arg in node.args.kwonlyargs if arg.annotation is None)
        if missing:
            rel = self.path.relative_to(ROOT)
            self.failures.append(f"{rel}:{node.lineno}: missing annotations on {node.name}: {', '.join(missing)}")
        if node.returns is None:
            rel = self.path.relative_to(ROOT)
            self.failures.append(f"{rel}:{node.lineno}: missing return annotation on {node.name}")
        self.generic_visit(node)


def main() -> None:
    failures: list[str] = []
    for path in sorted(SRC.rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        visitor = PublicFunctionVisitor(path)
        visitor.visit(tree)
        failures.extend(visitor.failures)
    if failures:
        raise SystemExit("\n".join(failures))


if __name__ == "__main__":
    main()
