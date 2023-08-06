"""Map supported job function names to infer jsonschemas to their tags."""
from enum import Enum


class FunctionNameToTag(str, Enum):
    """Map supported job function names to infer jsonschemas to their tags."""

    train_function = "train_function_schema"
    test_function = "test_function_schema"
    finetune_function = "finetune_function_schema"
