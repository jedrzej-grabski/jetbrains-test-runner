from argparse import ArgumentParser, Namespace
from contextlib import contextmanager
from statistics import mean, median
from subprocess import Popen, PIPE, TimeoutExpired
import io
from typing import Generator


class Config:
    """Configuration class for holding command constants."""

    HI_COMMAND = "Hi"
    GET_RANDOM_COMMAND = "GetRandom"
    SHUTDOWN_COMMAND = "Shutdown"
    NUM_RANDOM_INTS = 100
    TIMEOUT_MAX = 3.0


class UnexpectedResponseError(Exception):
    """Exception raised when the generator responds with an unexpected value"""

    def __init__(self, message: str, response: str):
        super().__init__(
            f"Message: {message} produced an unexpected response: {response}"
        )


def parse_args() -> Namespace:
    """Parse the command line arguments

    Returns:
        Namespace: Namespace object containing the parsed arguments
    """

    parser = ArgumentParser()
    parser.add_argument(
        "-g",
        "--generator-executable",
        help="Path to the generator executable, or the command required to run it.",
        type=str,
        default="src/generator.py",
    )
    return parser.parse_args()


@contextmanager
def open_generator_process(executable: str) -> Generator[Popen, None, None]:
    """A context manager to return a handle to the generator process.
    It will automatically send a shutdown signal upon exiting the context.

    Args:
        executable (str): Path to the generator executable, or the command required to run it.

    Raises:
        TimeoutError: If the generator process does not shut down in time

    Yields:
        Generator[Popen, None, None]: A handle to the generator process
    """

    try:
        process = Popen(executable, stdin=PIPE, stdout=PIPE, text=True)
    except Exception as e:
        raise RuntimeError(
            f"Could not start the generator process with the provided executable: {e}",
        )

    try:
        yield process
    finally:
        shutdown(process)

        try:
            process.wait(timeout=Config.TIMEOUT_MAX)
        except TimeoutExpired:
            process.kill()
            raise TimeoutError(
                "The generator process did not shut down in time and had to be killed."
            )

        print("Generator process shut down successfully.")


def shutdown(process: Popen) -> None:
    """Sends a shutdown message to the generator process

    Args:
        process (Popen): Handle to the generator process
    """

    send_message(process, Config.SHUTDOWN_COMMAND)


def retrieve_random(process: Popen) -> int:
    """Requests a random number from the generator process

    Args:
        process (Popen): Handle to the generator process

    Raises:
        UnexpectedResponseError: If the generator responds with an unexpected value

    Returns:
        int: The random number generated by the generator process
    """

    command = Config.GET_RANDOM_COMMAND
    send_message(process, command)

    try:
        response = read_message(process)
        number = int(response)
    except ValueError:
        raise UnexpectedResponseError(command, response)

    return number


def greet(process: Popen):
    """Sends a greeting message to the generator process

    Raises:
        UnexpectedResponseError: If the generator responds with an unexpected value

    Args:
        process (Popen): Handle to the generator process
    """
    command = Config.HI_COMMAND
    send_message(process, command)
    try:
        assert read_message(process) == "Hi"
    except AssertionError:
        raise UnexpectedResponseError(command, "Hello")


def send_message(process: Popen, message: str):
    """Sends a message to the generator process

    Raises:
        ValueError: If the process does not have a text-mode stdin
    Args:
        process (Popen): Handle to the generator process
        message (str):
    """

    try:
        assert isinstance(process.stdin, io.TextIOWrapper)
    except AssertionError:
        raise ValueError("The process should have a text-mode stdin.")

    process.stdin.write(f"{message}\n")
    process.stdin.flush()


def read_message(process: Popen) -> str:
    """Reads a message from the generator process

    Raises:
        ValueError: If the process does not have a text-mode stdout

    Args:
        process (Popen): Handle to the generator process

    Returns:
        str: The message read from the generator process
    """

    try:
        assert isinstance(process.stdout, io.TextIOWrapper)
    except AssertionError:
        raise ValueError("The process should have a text-mode stdout.")
    return process.stdout.readline().strip()


if __name__ == "__main__":

    args = parse_args()

    with open_generator_process(args.generator_executable) as generator:
        greet(generator)

        random_ints: list[int] = [
            retrieve_random(generator) for _ in range(Config.NUM_RANDOM_INTS)
        ]

        random_ints.sort()

        print(f"Generated random integers: {random_ints}")
        print(f"Median: {median(random_ints)}")
        print(f"Average: {mean(random_ints)}")
