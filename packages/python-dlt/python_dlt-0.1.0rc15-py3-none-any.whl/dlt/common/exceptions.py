from typing import Any, AnyStr


class DltException(Exception):
    pass


class SignalReceivedException(DltException):
    def __init__(self, signal_code: int) -> None:
        self.signal_code = signal_code
        super().__init__(f"Signal {signal_code} received")


class PoolException(DltException):
    """
    Thrown by worker pool to pass information when thrown during processing an item
    """
    def __init__(self, pool_name: str = None, item: str = None, internal_exception: Exception = None) -> None:
        # we need it to make it pickle compatible
        if pool_name:
            self.pool_name = pool_name
            self.item = item
            self.internal_exception = internal_exception
            super().__init__(f"Pool {pool_name} raised on item {item} with {str(internal_exception)}")


class UnsupportedProcessStartMethodException(DltException):
    def __init__(self, method: str) -> None:
        self.method = method
        super().__init__(f"Process pool supports only fork start method, {method} not supported. Switch the pool type to threading")


class CannotInstallDependency(DltException):
    def __init__(self, dependency: str, interpreter: str, output: AnyStr) -> None:
        self.dependency = dependency
        self.interpreter = interpreter
        if isinstance(output, bytes):
            str_output = output.decode("utf-8")
        else:
            str_output = output
        super().__init__(f"Cannot install dependency {dependency} with {interpreter} and pip:\n{str_output}\n")


class VenvNotFound(DltException):
    def __init__(self, interpreter: str) -> None:
        self.interpreter = interpreter
        super().__init__(f"Venv with interpreter {interpreter} not found in path")


class TerminalException(Exception):
    """
    Marks an exception that cannot be recovered from, should be mixed in into concrete exception class
    """
    pass


class TransientException(Exception):
    """
    Marks an exception in operation that can be retried, should be mixed in into concrete exception class
    """
    pass


class TerminalValueError(ValueError, TerminalException):
    """
    ValueError that is unrecoverable
    """
    pass


class TimeRangeExhaustedException(DltException):
    """
    Raised when backfilling complete and no more time ranges can be generated
    """
    def __init__(self, start_ts: float, end_ts: float) -> None:
        self.start_ts = start_ts
        self.end_ts = end_ts
        super().__init__(f"Timerange ({start_ts} to {end_ts}> exhausted")


class DictValidationException(DltException):
    def __init__(self, msg: str, path: str, field: str = None, value: Any = None):
        self.path = path
        self.field = field
        self.value = value
        super().__init__(msg)
