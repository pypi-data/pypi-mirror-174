"""Tests for testing CLI errors."""

from pathlib import Path

from commandsheet.cli import CustomArgumentParser
from commandsheet.errors import no_config_file_found
from commandsheet.errors import no_config_file_sections_found
from commandsheet.errors import no_config_file_path_exists
from commandsheet.errors import not_a_valid_config_file
from commandsheet.errors import no_compatible_os

import pytest


def test_no_config_file_found(capsys):
    parser = CustomArgumentParser()
    with pytest.raises(SystemExit):
        no_config_file_found(parser)

    out, err = capsys.readouterr()
    assert err == 'No `commandsheet.ini` file found :(\n'
    assert out == ''


def test_no_config_file_sections_found(capsys):
    parser = CustomArgumentParser()
    with pytest.raises(SystemExit):
        no_config_file_sections_found(parser)

    out, err = capsys.readouterr()
    assert err == 'No sections to display from commandsheet.ini :(\n'
    assert out == ''


def test_no_config_file_path_exists(capsys):
    parser = CustomArgumentParser()
    file = '/invalid/path/to/file.ini'
    with pytest.raises(SystemExit):
        no_config_file_path_exists(parser, file=file)

    out, err = capsys.readouterr()
    assert err == f'Config file `{file}` does not exist\n'
    assert out == ''


def test_not_a_valid_config_file(capsys):
    parser = CustomArgumentParser()
    file = '/path/to/invalid/configfile.invalid'
    with pytest.raises(SystemExit):
        not_a_valid_config_file(parser, file=file)

    out, err = capsys.readouterr()
    name = Path(file).name
    assert err == f'File `{name}` is not of valid config file format\n'
    assert out == ''


def test_no_compatible_os(capsys):
    parser = CustomArgumentParser()
    os = 'Windows'

    with pytest.raises(SystemExit):
        no_compatible_os(parser, os)

    out, err = capsys.readouterr()
    assert err == f'`{os}` is not an OS that is supported :(\n'
    assert out == ''
