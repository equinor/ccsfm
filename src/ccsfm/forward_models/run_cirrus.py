import subprocess
from typing import Optional

from ert import (
    ForwardModelStepDocumentation,
    ForwardModelStepJSON,
    ForwardModelStepPlugin,
    ForwardModelStepValidationError,
)


class Cirrus(ForwardModelStepPlugin):
    EXECUTABLE = "/prog/pflotran/bin/_runcirrus"

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
        return_value = subprocess.run(
            [self.EXECUTABLE, "--print-available-versions"],
            capture_output=True, check=False,
        )

        if (requested_version := fm_step_json["argList"][version_idx]) not in (
            available_versions := str(return_value.stdout)
        ):
            raise ForwardModelStepValidationError(
                f"Requested version: {requested_version}, is not available. Must be one of {available_versions}"
            )

    @staticmethod
    def documentation() -> Optional[ForwardModelStepDocumentation]:
        return ForwardModelStepDocumentation(
            category="utility.file_system",
            source_package="ccsfm",
            source_function_name="Cirrus",
            description="Add description here",
            examples="""
            | Add examples here
            """,
        )
