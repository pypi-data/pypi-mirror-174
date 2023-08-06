from textwrap import dedent

from commandsheet.config import Section
from commandsheet.output import header
from commandsheet.output import display_commandsheet
from commandsheet.output import format_section_heading
from commandsheet.output import format_section_content

import pytest


def test_header(capsys):
    """
    ████████████████████████████████████████████████████████████████████████████
    █─▄▄▄─█─▄▄─█▄─▀█▀─▄█▄─▀█▀─▄██▀▄─██▄─▀█▄─▄█▄─▄▄▀█─▄▄▄▄█─█─█▄─▄▄─█▄─▄▄─█─▄─▄─█
    █─███▀█─██─██─█▄█─███─█▄█─███─▀─███─█▄▀─███─██─█▄▄▄▄─█─▄─██─▄█▀██─▄█▀███─███
    ▀▄▄▄▄▄▀▄▄▄▄▀▄▄▄▀▄▄▄▀▄▄▄▀▄▄▄▀▄▄▀▄▄▀▄▄▄▀▀▄▄▀▄▄▄▄▀▀▄▄▄▄▄▀▄▀▄▀▄▄▄▄▄▀▄▄▄▄▄▀▀▄▄▄▀▀
    """
    header()
    out, err = capsys.readouterr()
    assert out == dedent(test_header.__doc__) + '\n'
    assert err == ''


def test_format_section_heading():
    text = 'heading'
    index = 1
    assert format_section_heading(text, index=index) == '1. heading'
    assert format_section_heading(text, index=None) == 'heading'


def test_format_section_content_with_short_description():
    cmd = 'ls --long'
    dsc = 'List in a long format'
    fillchar = '.'
    indent = len(cmd) + 5
    max_width = 85

    result = format_section_content(
        cmd,
        dsc,
        indent=indent,
        fillchar=fillchar,
        max_width=max_width
    )

    expected = 'ls --long..... List in a long format'
    assert result == expected


def test_format_section_content_with_long_description():
    cmd = 'ls --long'
    dsc = 'List in a long format. You can also use the -l option.'
    fillchar = '.'
    indent = len(cmd) + 5

    # We don't need to actually write a longer description
    # to test against a 'longer' description (we could if
    # we'd like to, but that is unnecessary). Instead, we
    # can simply reduce the value of the ``max_width``
    # parameter.
    max_width = 40

    result = format_section_content(
        cmd,
        dsc,
        indent=indent,
        fillchar=fillchar,
        max_width=max_width
    )

    expected = (
        'ls --long..... List in a long format. You can also use\n'
        '               the -l option.'
    )
    assert result == expected


def test_display_commandsheet(capsys):
    content = (('cmd', 'desc'),)
    alpha = Section(name='alpha', contents=content)
    bravo = Section(name='bravo', contents=content)

    # This basically represents the commandsheet as if
    # it would be read from a file and parsed. This way,
    # we don't have to actually have a config-file that
    # we have to read, but we can simulate one, instead.
    sections = [alpha, bravo]

    # We're not using the ``section_numbers`` parameter here
    display_commandsheet(
        sections,
        fillchar='.',
        section_numbers=False,
        max_width=40,
        indent=8
    )

    expected = (
        '╭─ alpha ───────╮\n'
        '│ cmd..... desc │\n'
        '╰───────────────╯\n'
        '╭─ bravo ───────╮\n'
        '│ cmd..... desc │\n'
        '╰───────────────╯\n'
    )

    out, err = capsys.readouterr()
    assert out == expected
    assert err == ''

    # We are using the ``section_numbers`` parameter here
    display_commandsheet(
        sections,
        fillchar='.',
        section_numbers=True,
        max_width=40,
        indent=8
    )

    expected = (
        '╭─ 1. alpha ────╮\n'
        '│ cmd..... desc │\n'
        '╰───────────────╯\n'
        '╭─ 2. bravo ────╮\n'
        '│ cmd..... desc │\n'
        '╰───────────────╯\n'
    )

    out, err = capsys.readouterr()
    assert out == expected
    assert err == ''
