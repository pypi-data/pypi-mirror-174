from commandsheet.compatibility import compatible_os


def test_compatible_os_with_compatible_os():
    oses = ('Linux', 'Darwin',)
    for os in oses:
        assert compatible_os(os)


def test_compatible_os_with_incompatible_os():
    oses = ('Windows', 'Other invalid OS',)
    for os in oses:
        assert not compatible_os(os)
