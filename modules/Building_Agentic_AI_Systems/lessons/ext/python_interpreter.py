"""Unsandboxed local Python interpreter for DSPy CodeAct."""

from __future__ import annotations

import contextlib
import io
import keyword
import types
from collections.abc import Callable
from typing import Any

from dspy.primitives import CodeInterpreterError, FinalOutput

__all__ = ["PythonInterpreterLocal", "FinalOutput", "CodeInterpreterError"]


class _SubmitSignal(BaseException):
    def __init__(self, payload: dict[str, Any]) -> None:
        self.payload = payload


def _merge_into_globals(globals_dict: dict[str, Any], item: Any) -> None:
    if isinstance(item, dict):
        globals_dict.update(item)
        return

    if isinstance(item, types.ModuleType):
        globals_dict[item.__name__] = item
        return

    if callable(item):
        name = getattr(item, "__name__", None)
        if not name or not name.isidentifier() or keyword.iskeyword(name):
            raise CodeInterpreterError(
                f"Cannot merge callable without a valid __name__: {item!r}"
            )
        globals_dict[name] = item
        return

    raise CodeInterpreterError(
        f"Unsupported namespace item type: {type(item).__name__}. "
        "Expected a module, callable, or dict."
    )


def _make_submit(output_fields: list[dict] | None) -> Callable[..., None]:
    if not output_fields:

        def submit(output: Any = None, **kwargs: Any) -> None:
            if kwargs:
                raise _SubmitSignal(kwargs)
            raise _SubmitSignal({"output": output})

        return submit

    field_names = [field["name"] for field in output_fields]

    def submit(**kwargs: Any) -> None:
        missing = [name for name in field_names if name not in kwargs]
        if missing:
            raise CodeInterpreterError(
                f"SUBMIT() missing required output field(s): {', '.join(missing)}"
            )
        raise _SubmitSignal({name: kwargs[name] for name in field_names})

    submit.__name__ = "SUBMIT"
    return submit


class PythonInterpreterLocal:
    """Local interpreter for unsandboxed Python execution on the host machine.

    Implements the :class:`~ext.code_interpreter.CodeInterpreter` protocol for
    use with DSPy's :class:`dspy.predict.CodeAct` module. Code runs directly in
    the current Python process via ``exec(compile(...))`` — there is no WASM
    sandbox, Deno subprocess, or JSON-RPC layer.

    Execution state (variables, function definitions) persists across
    :meth:`execute` calls until :meth:`shutdown`.

    Examples:
        ```python
        # Basic execution
        with PythonInterpreterLocal() as interp:
            result = interp("print(1 + 2)")  # Returns "3"

        # With host-side tools
        def my_tool(question: str) -> str:
            return "answer"

        with PythonInterpreterLocal(tools={"my_tool": my_tool}) as interp:
            result = interp("print(my_tool(question='test'))")

        # With the datetime module in the namespace
        import datetime

        with PythonInterpreterLocal(namespace=[datetime]) as interp:
            result = interp('print(datetime.date.today())')

        # With an installed third-party package (import name: dateutil)
        import dateutil

        with PythonInterpreterLocal(namespace=[dateutil]) as interp:
            result = interp(
                'from dateutil.parser import parse; print(parse("June 17, 2026").year)'
            )
        ```
    """

    def __init__(
        self,
        *,
        namespace: list[Any] | None = None,
        tools: dict[str, Callable[..., str]] | None = None,
        output_fields: list[dict] | None = None,
    ) -> None:
        self._namespace_items = list(namespace) if namespace else []
        self._tools = dict(tools) if tools else {}
        self._output_fields = output_fields
        self._globals: dict[str, Any] | None = None
        self._started = False
        self._shutdown = False

    @property
    def tools(self) -> dict[str, Callable[..., str]]:
        return dict(self._tools)

    def start(self) -> None:
        if self._shutdown:
            raise CodeInterpreterError(
                "Interpreter has been shut down. Create a new instance."
            )
        if self._started:
            return

        globals_dict: dict[str, Any] = {"__builtins__": __builtins__}
        globals_dict["SUBMIT"] = _make_submit(self._output_fields)

        for item in self._namespace_items:
            _merge_into_globals(globals_dict, item)

        globals_dict.update(self._tools)

        self._globals = globals_dict
        self._started = True

    def execute(
        self,
        code: str,
        variables: dict[str, Any] | None = None,
    ) -> Any:
        if self._shutdown:
            raise CodeInterpreterError(
                "Interpreter has been shut down. Create a new instance."
            )

        self.start()
        assert self._globals is not None

        if variables:
            for key in variables:
                if not key.isidentifier() or keyword.iskeyword(key):
                    raise CodeInterpreterError(f"Invalid variable name: '{key}'")
            self._globals.update(variables)

        stdout_buffer = io.StringIO()
        try:
            with contextlib.redirect_stdout(stdout_buffer):
                exec(compile(code, "<python_interpreter_local>", "exec"), self._globals)
        except SyntaxError:
            raise
        except _SubmitSignal as signal:
            return FinalOutput(signal.payload)
        except Exception as exc:
            raise CodeInterpreterError(f"{type(exc).__name__}: {exc}") from exc

        captured = stdout_buffer.getvalue()
        if captured:
            return captured.rstrip("\n")
        return None

    def shutdown(self) -> None:
        # self._globals = None
        # self._started = False
        # self._shutdown = True
        pass

    def __enter__(self) -> PythonInterpreterLocal:
        self.start()
        return self

    def __exit__(self, *_: object) -> None:
        self.shutdown()

    def __call__(
        self,
        code: str,
        variables: dict[str, Any] | None = None,
    ) -> Any:
        return self.execute(code, variables)
