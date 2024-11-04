import pytest
from subprocess import TimeoutExpired
import io
from src.controller import (
    UnexpectedResponseError,
    greet,
    retrieve_random,
    send_message,
    read_message,
)


@pytest.fixture
def mock_correct_process():
    class CorrectProcess:
        """Mock class for a properly working process."""

        def __init__(self):
            self.stdin = io.TextIOWrapper(io.BytesIO(), write_through=True)
            self.stdout = io.TextIOWrapper(io.BytesIO(), write_through=True)

        def set_output(self, output: str) -> None:
            """Helper function to set stdout content."""
            self.stdout = io.TextIOWrapper(
                io.BytesIO(output.encode()), write_through=True
            )

    return CorrectProcess()


@pytest.fixture
def mock_incorrect_process():
    """Mock class for a process that does not have stdin and stdout and should not work."""

    class IncorrectProcess:
        def __init__(self) -> None:
            self.stdin = None
            self.stdout = None

    return IncorrectProcess()


class TestSendMessage:

    def test_send_message_from_incorrect_process(self, mock_incorrect_process):
        with pytest.raises(ValueError):
            send_message(mock_incorrect_process, "Hi")

    def test_send_message_from_correct_process(self, mock_correct_process):
        send_message(mock_correct_process, "Hi")


class TestReadMessage:

    def test_read_message_from_correct_process(self, mock_correct_process):
        read_message(mock_correct_process)

    def test_read_message_from_incorrect_process(self, mock_incorrect_process):
        with pytest.raises(ValueError):
            read_message(mock_incorrect_process)


class TestGreet:

    def test_greet_expected(self, mock_correct_process):
        mock_correct_process.set_output("Hi")
        greet(mock_correct_process)

    def test_greet_unexpected(self, mock_correct_process):
        mock_correct_process.set_output("Unexpected")
        with pytest.raises(UnexpectedResponseError):
            greet(mock_correct_process)


class TestRetrieveRandom:

    def test_retrieve_random_expected(self, mock_correct_process):
        mock_correct_process.set_output("33")
        result = retrieve_random(mock_correct_process)
        assert result == 33

    def test_retrieve_random_unexpected(self, mock_correct_process):
        mock_correct_process.set_output("NotInt")
        with pytest.raises(UnexpectedResponseError):
            retrieve_random(mock_correct_process)
