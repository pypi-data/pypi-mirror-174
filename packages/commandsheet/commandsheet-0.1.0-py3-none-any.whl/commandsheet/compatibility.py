"""Code to validate if OS is compatible."""

COMPATIBLE_OS = (
    'linux',
    'darwin',
)


def compatible_os(name):
    if name.strip().lower() not in COMPATIBLE_OS:
        return False
    return True
