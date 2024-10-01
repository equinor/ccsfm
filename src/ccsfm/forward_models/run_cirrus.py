from typing import Optional
from pathlib import Path
import os

from ert import (
    ForwardModelStepDocumentation,
    ForwardModelStepPlugin,
    ForwardModelStepJSON,
    ForwardModelStepValidationError,
)

DESCRIPTION = """
Cirrus, previously known as Pflotran-ogs, is developed by the OpenGoSim group.

See their homepage for more information about their product https://opengosim.com
"""


class Cirrus(ForwardModelStepPlugin):
    EXECUTABLE = "/prog/pflotran/bin/_runcirrus"
    VERSIONLOCATION = "/prog/pflotran/versions"

    def __init__(self) -> None:
        super().__init__(
            name="CIRRUS",
            command=[
                self.EXECUTABLE,
                "-q",
                "local",
                "-n",
                "<NUM_CPU>",
                "-v",
                "<VERSION>",
                "<CASE>",
            ],
            default_mapping={"<NUM_CPU>": 1, "<VERSION>": "latest"},
        )

    def validate_pre_experiment(self, fm_step_json: ForwardModelStepJSON) -> None:
        version_idx = fm_step_json["argList"].index("-v") + 1

        requested_version = fm_step_json["argList"][version_idx]
        self.version_path = Path(f"{ self.VERSIONLOCATION}/{requested_version}")

        if not self.version_path.exists():

            available_versions = [
                f for f in os.listdir(self.VERSIONLOCATION) if not f.startswith(".")
            ]

            raise ForwardModelStepValidationError(
                f"Requested Cirrus version: {requested_version}, is not available. Must be one of {available_versions}"
            )

    def validate_pre_realization_run(
        self, fm_step_json: ForwardModelStepJSON
    ) -> ForwardModelStepJSON:

        # Version has already been validated, we only need to ensure it is used
        version_idx = fm_step_json["argList"].index("-v") + 1
        fm_step_json["argList"][version_idx] = self.version_path.resolve().name

        return fm_step_json

    @staticmethod
    def documentation() -> Optional[ForwardModelStepDocumentation]:
        return ForwardModelStepDocumentation(
            category="simulators.reservoir",
            source_package="ccsfm",
            source_function_name="Cirrus",
            description=DESCRIPTION,
            examples="""
            FORWARD_MODEL CIRRUS(<CASE>="casename.in")

            FORWARD_MODEL CIRRUS(<CASE>="casename.in", <VERSION>=x.x, <NUM_CPU>=4)
            """,
        )
