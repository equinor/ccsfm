from typing import Optional
import os

from ert import (
    ForwardModelStepDocumentation,
    ForwardModelStepPlugin,
    ForwardModelStepJSON,
    ForwardModelStepValidationError,
)

DESCRIPTION = """
Cirrus, previously known as Pflotran-ogs, is developed by the OpenGoSim group.

"""


class Cirrus(ForwardModelStepPlugin):
    EXECUTABLE = "/prog/pflotran/bin/_runcirrus"
    VERSIONLOCATION = "/prog/pflotran/versions/"

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

        available_versions = [
            f for f in os.listdir(self.VERSIONLOCATION) if not f.startswith(".")
        ]

        if (requested_version := fm_step_json["argList"][version_idx]) not in (
            available_versions
        ):
            raise ForwardModelStepValidationError(
                f"Requested version: {requested_version}, is not available. Must be one of {available_versions}"
            )

    @staticmethod
    def documentation() -> Optional[ForwardModelStepDocumentation]:
        return ForwardModelStepDocumentation(
            category="simulators.reservoir",
            source_package="ccsfm",
            source_function_name="Cirrus",
            description="Cirrus,",
            examples="""
            | Add examples here
            """,
        )
