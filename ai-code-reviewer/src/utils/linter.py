import io
from pyflakes.api import check
from pyflakes.reporter import Reporter
from typing import Dict, Any, List


def run_ruff_linter(code_string: str) -> Dict[str, Any]:
    """
    Statically analyzes code for errors, unused imports, and undefined variables
    using pyflakes directly in-memory without invoking CLI subprocesses.
    """
    warning_stream = io.StringIO()
    error_stream = io.StringIO()
    reporter = Reporter(warning_stream, error_stream)

    # Run static check in-memory
    check(code_string, filename="target.py", reporter=reporter)

    output = warning_stream.getvalue().strip()
    issues: List[str] = [line for line in output.splitlines() if line] if output else []

    return {"passed": len(issues) == 0, "issue_count": len(issues), "issues": issues}
