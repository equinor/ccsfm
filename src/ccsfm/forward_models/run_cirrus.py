from typing import Optional

from ert import (
    ForwardModelStepDocumentation,
    ForwardModelStepPlugin,
)


class Cirrus(ForwardModelStepPlugin):
    def __init__(self) -> None:
        super().__init__(
            name="CIRRUS",
            command=[
                "/prog/pflotran/bin/_runcirrus",
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

