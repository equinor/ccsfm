from typing import Optional

from ert import (
    ForwardModelStepDocumentation,
    ForwardModelStepPlugin,
)

class RunCirrus(ForwardModelStepPlugin):
    def __init__(self):
        super().__init__(
            name="RUN_CIRRUS",
            command=["pwd"],
        )

    @staticmethod
    def documentation() -> Optional[ForwardModelStepDocumentation]:
        return ForwardModelStepDocumentation(
            category="utility.file_system",
            source_package="semeio",
            source_function_name="RunCirrus",
            description="Add description here",
            examples="""
            | Add examples here
            """,
        )