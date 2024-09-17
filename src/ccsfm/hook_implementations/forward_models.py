import ert

from ccsfm.forward_models.run_cirrus import (
    RunCirrus,
)

@ert.plugin(name="ccsfm")
def installable_forward_model_steps():
    return [
        RunCirrus,
    ]
