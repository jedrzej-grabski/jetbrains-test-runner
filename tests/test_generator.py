import pytest
from src.generator import hi, get_random, shutdown, main
import random

import sys


class TestGenerator:
    def test_hi_command(self, capsys):
        """Test the Hi command to ensure it outputs 'Hi'"""
        hi()
        captured = capsys.readouterr()
        assert captured.out == "Hi\n"

    def test_get_random_command(self, capsys, monkeypatch):
        """Test the GetRandom command to ensure it outputs a specified random integer"""

        monkeypatch.setattr(random, "randint", lambda *_: 500)

        get_random()

        captured = capsys.readouterr()
        assert captured.out == "500\n"

    def test_shutdown_command(self):
        """Test the Shutdown command to ensure it raises SystemExit"""
        with pytest.raises(SystemExit):
            shutdown()

    def test_main_loop(self, monkeypatch, capsys):
        """Test the main loop to ensure it processes commands correctly"""

        inputs = iter(["Hi", "GetRandom", "Shutdown"])

        monkeypatch.setattr("sys.stdin.readline", lambda: next(inputs) + "\n")

        monkeypatch.setattr(random, "randint", lambda *args: 500)

        with pytest.raises(SystemExit):
            main()

            captured = capsys.readouterr()
            output_lines = captured.out.strip().splitlines()

            assert output_lines[0] == "Hi"
            assert output_lines[1] == "500"
