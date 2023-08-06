import sys
from commandsheet.cli import CustomArgumentParser
from commandsheet.cli import argparser
from commandsheet.cli import options
import pytest


class TestCustomArgumentParser:
    def test_print_usage(self, capsys):
        parser = CustomArgumentParser()

        parser.print_usage()
        out, err = capsys.readouterr()
        assert out.startswith('usage: ')
        assert err == ''

        parser.print_usage(file=sys.stderr)
        out, err = capsys.readouterr()
        assert out == ''
        assert err.startswith('usage: ')

    def test_print_help(self, capsys):
        parser = CustomArgumentParser()

        parser.print_help()
        out, err = capsys.readouterr()
        assert out.startswith('usage: ')
        assert err == ''

        parser.print_help(file=sys.stderr)
        out, err = capsys.readouterr()
        assert out == ''
        assert err.startswith('usage: ')

    def test_parse_args(self, capsys):
        prog = 'test'
        command = 'unknown-command'
        parser = CustomArgumentParser(prog=prog)

        with pytest.raises(SystemExit):
            parser.parse_args((command,))
        out, err = capsys.readouterr()
        assert out == ''
        assert err.split('\n')[0] == f'usage: {prog} [-h]'
        assert err.split('\n')[1] == f'{prog}: error: unrecognized arguments: {command}'

        args = parser.parse_args()
        out, err = capsys.readouterr()
        assert out == ''
        assert err == ''

    def test_exit(self, capsys):
        parser = CustomArgumentParser()

        with pytest.raises(SystemExit):
            parser.exit(status=0, message='Exit message', newline=True)
        out, err = capsys.readouterr()
        assert out == ''
        assert err == 'Exit message\n'

        with pytest.raises(SystemExit):
            parser.exit(status=0, message='Exit message', newline=False)
        out, err = capsys.readouterr()
        assert out == ''
        assert err == 'Exit message'

        with pytest.raises(SystemExit):
            parser.exit(status=0)
        out, err = capsys.readouterr()
        assert out == ''
        assert err == ''

    def test_error(self, capsys):
        prog = 'test'
        msg = 'this is an error message'
        parser = CustomArgumentParser(prog=prog)

        with pytest.raises(SystemExit):
            parser.error(message=msg)
        out, err = capsys.readouterr()
        assert out == ''
        assert err.split('\n')[0] == f'usage: {prog} [-h]'
        assert err.split('\n')[1] == f'{prog}: error: {msg}'


def test_options():
    parser = CustomArgumentParser(add_help=False)
    options(parser)
    args = parser.parse_args()

    assert hasattr(args, 'section_numbers')
    assert hasattr(args, 'fillchar')
    assert hasattr(args, 'config_file')


def test_argparser():
    parser = argparser()
    assert isinstance(parser, CustomArgumentParser)
    assert parser.prog == 'commandsheet'
    assert parser.description == 'Display catalog of commands user uses often.'
    assert parser.epilog is None
    assert parser.usage is None
    assert parser.add_help == False
    assert parser.allow_abbrev == False
