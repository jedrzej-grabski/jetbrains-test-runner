import random
import sys
from typing import Callable
from collections import defaultdict
from sys import stdin, stdout

# While it may seem uneccessary, I decided to use the function registry design pattern
# to allow for scalability


def do_nothing() -> None:
    """Function that does nothing, used when an unspecified command is called"""


COMMAND_REGISTRY: defaultdict[str, Callable[[], None]] = defaultdict(lambda: do_nothing)


def command(name: str) -> Callable:
    """Decorator to define a function as the controllers' command

    Args:
        name (str): Name of the command that can be used by the controller

    Returns:
        Callable: Function thatytwill be executed while calling the command
    """

    def wrapper(func: Callable):
        COMMAND_REGISTRY[name] = func
        return func

    return wrapper


@command("Hi")
def hi() -> None:
    """Function that prints Hi to the stdout"""
    stdout.write("Hi\n")
    stdout.flush()


@command("GetRandom")
def get_random() -> None:
    """Function that prints a pseudo-random intiger to the stdout"""
    rand_int = random.randint(-sys.maxsize, sys.maxsize)
    stdout.write(f"{rand_int}\n")
    stdout.flush()


@command("Shutdown")
def shutdown() -> None:
    """Function that shuts down the program"""
    raise SystemExit("User requested shutdown")


def main() -> None:
    COMMAND_REGISTRY["GetRandom"]()


main()
