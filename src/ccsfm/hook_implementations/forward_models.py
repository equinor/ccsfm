import ert

from ccsfm.forward_models.run_cirrus import (
    Cirrus,
)


@ert.plugin(name="ccsfm")
def installable_forward_model_steps():
    return [
        Cirrus,
    ]
