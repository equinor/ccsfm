from collections import namedtuple
import pytest
import subprocess

from ert.plugins import ErtPluginManager
from ert.config import ErtConfig
from ert.config.parsing.config_errors import ConfigValidationError

from ccsfm.forward_models.run_cirrus import Cirrus

DEFAULT_CONFIG = """
JOBNAME TEST
NUM_CPU 1
QUEUE_SYSTEM LOCAL
QUEUE_OPTION LOCAL MAX_RUNNING 1


NUM_REALIZATIONS 1
MIN_REALIZATIONS 1

FORWARD_MODEL {}({})
"""


def test_forward_model_installation():
    pm = ErtPluginManager()
    assert Cirrus in pm.forward_model_steps


@pytest.mark.parametrize(
    "call_content,expected_failure",
    [
        pytest.param("<NUM_CPU>=1, <VERSION>=1", "It is not allowed to modify"),
        pytest.param("<VERSION>=1, <INCORRECT>=1", "Missing required arguments"),
    ],
)
def test_parameter_validation(call_content, expected_failure):
    config = DEFAULT_CONFIG.format("CIRRUS", call_content)
    with open("config.ert", "w", encoding="utf-8") as file:
        file.write(config)

    with pytest.raises(ConfigValidationError, match=expected_failure):
        ErtConfig.with_plugins().from_file("config.ert")


@pytest.mark.uses_cirrus
@pytest.mark.usefixtures("setup_tmpdir")
def test_forward_model_validation():
    config = DEFAULT_CONFIG.format("CIRRUS", "<VERSION>=-1")

    with open("config.ert", "w", encoding="utf-8") as file:
        file.write(config)

    processreturn = namedtuple("returntype", ["stdout"])(stdout="")

    with pytest.raises(
        subprocess.CalledProcessError,
        match=r"Command.*ert.*returned non-zero exit status",
    ):
        processreturn = subprocess.run(
            ["ert", "test_run", "config.ert"], check=True, capture_output=True
        )
    assert "Requested version: -1" in str(processreturn.stdout)
