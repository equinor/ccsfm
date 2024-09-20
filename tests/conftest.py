import pytest


@pytest.fixture()
def setup_tmpdir(tmpdir):
    with tmpdir.as_cwd():
        yield


def pytest_addoption(parser):
    parser.addoption(
        "--ert-integration",
        action="store_true",
        default=False,
        help="Run ERT integration tests",
    )


def pytest_collection_modifyitems(config, items):
    if config.getoption("--ert-integration"):
        # Do not skip tests when --ert-integration is supplied on pytest command line
        return
    skip_ert_integration = pytest.mark.skip(
        reason="need --ert-integration option to run"
    )
    for item in items:
        if "ert-integration" in item.keywords:
            item.add_marker(skip_ert_integration)
