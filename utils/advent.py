from pathlib import Path
import ast
import re


class AdventRunner:
    def _scan(self) -> int:
        current_dir = Path.cwd()
        py_files = list(current_dir.glob('*.py'))
        for file in py_files:
            print(file.name)
            self._find_methods(file)

    def _find_methods(self, file: Path):
        print(f"\nScanning: {file.name}")
        try:
            source_code = file.read_text(encoding='utf-8')
            tree = ast.parse(source_code)
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    self._check_method(node)
        except SyntaxError:
            print("Skipped (Syntax Error in file)")
        except Exception as e:
            print(f"Error: {e}")

    def _check_method(self, node: ast.FunctionDef | ast.AsyncFunctionDef):
        task_match = re.match(
                r'^(?:part|task|star)(\d+)$',
                node.name, re.IGNORECASE
        )
        if task_match:
            number = int(task_match.group(1))
            print(f"- Found solver: {node.name}, {number}")


if __name__ == "__main__":
    runner = AdventRunner()
    runner._scan()
