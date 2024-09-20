import pytest


@pytest.fixture()
def setup_tmpdir(tmpdir):
    with tmpdir.as_cwd():
        yield


def pytest_addoption(parser):
    parser.addoption(
        "--uses-cirrus",
        action="store_true",
        default=False,
        help="Run ERT with Cirrus tests",
    )


def pytest_collection_modifyitems(config, items):
    if config.getoption("--uses-cirrus"):
        # Do not skip tests when --ert-integration is supplied on pytest command line
        return
    skip_uses_cirrus = pytest.mark.skip(
        reason="need --uses-cirrus option to run"
    )
    for item in items:
        if "uses_cirrus" in item.keywords:
            item.add_marker(skip_uses_cirrus)
