from typing import Optional
from pathlib import Path
import os

from ert import (
    ForwardModelStepDocumentation,
    ForwardModelStepPlugin,
    ForwardModelStepWarning,
    ForwardModelStepJSON,
    ForwardModelStepValidationError,
)

DESCRIPTION = """
Cirrus, previously known as Pflotran-ogs, is developed by the OpenGoSim group.

See their homepage for more information about their product https://opengosim.com

The Forward Model is made to use the resources requested in the ert config. The
NUM_CPU variable is picked up and used to set the number of cores. It is not
possible to use multiple nodes in ert (e.g. the -m parameter for runcirrus),
hence it is not possible to request that through the forward model either.
"""

EXECUTABLE: str = "/prog/cirrus/bin/runcirrus"
VERSIONLOCATION: str = "/prog/cirrus/versions"

class Cirrus(ForwardModelStepPlugin):
    def __init__(self) -> None:
        super().__init__(
            name="CIRRUS",
            command=[
                EXECUTABLE,
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
        PROTECTED_ARGUMENT = ["<NUM_CPU>"]
        REQUIRED_ARGUMENTS = ["<CASE>"]
        OPTIONAL_ARGUMENTS = ["<VERSION>"]

        if protected_arguments_used := [
            arg for arg in self.private_args if arg in PROTECTED_ARGUMENT
        ]:
            raise ForwardModelStepValidationError(
                f"CIRRUS forward model will use {', '.join(protected_arguments_used)} as set in ert config. It is not allowed to modify"
            )

        # If an argument exists in fm_step_json['arglist'] it means it has not been substituted with a defined variable from ert config
        # We check that a required argument must either be in private_args or not present in fm_step_json['arglist']
        if missing_required_arg := [
            arg
            for arg in REQUIRED_ARGUMENTS
            if arg not in self.private_args and arg in fm_step_json["argList"]
        ]:
            raise ForwardModelStepValidationError(
                f"Missing required arguments: {', '.join(missing_required_arg)}"
            )

        if unrecognised_arguments := [
            arg
            for arg in self.private_args
            if arg not in REQUIRED_ARGUMENTS + OPTIONAL_ARGUMENTS
        ]:
            ForwardModelStepWarning.warn(
                f"CIRRUS does not recognise the following arguments {', '.join(unrecognised_arguments)}, they can be completely removed"
            )

        version_idx = fm_step_json["argList"].index("-v") + 1
        requested_version = fm_step_json["argList"][version_idx]
        self.version_path = Path(f"{VERSIONLOCATION}/{requested_version}")

        if not self.version_path.exists():
            available_versions = [
                f for f in os.listdir(VERSIONLOCATION) if not f.startswith(".")
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

            FORWARD_MODEL CIRRUS(<CASE>="casename.in", <VERSION>=x.x)
            """,
        )
