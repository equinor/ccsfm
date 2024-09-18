from collections import namedtuple
import pytest
import subprocess

DEFAULT_CONFIG = """
JOBNAME TEST

QUEUE_SYSTEM LOCAL
QUEUE_OPTION LOCAL MAX_RUNNING 1


NUM_REALIZATIONS 1
MIN_REALIZATIONS 1

FORWARD_MODEL {}({})
"""


@pytest.mark.usefixtures("setup_tmpdir")
def test_forward_model_installation():
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
