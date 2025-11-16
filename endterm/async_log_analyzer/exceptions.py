class AsyncLogAnalyzerError(Exception):
    """Base exception for the package."""


class InvalidLogFormatError(AsyncLogAnalyzerError):
    """Raised when a log line cannot be parsed according to expected format."""


class FileReadError(AsyncLogAnalyzerError):
    """Raised when a file cannot be read or opened."""