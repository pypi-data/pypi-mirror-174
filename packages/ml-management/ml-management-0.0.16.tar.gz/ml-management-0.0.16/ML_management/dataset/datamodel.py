"""Define class with supported data flavours."""
from enum import Enum


class DatasetFlavour(str, Enum):
    """List of supported data flavours."""

    MNIST = "mnist"
    NERC_TDM = "nerc_tdm"
    CONLL_TDM = "conll_tdm"
    TOPIC_MARKER = "topic_marker"
    AG_NEWS = "ag_news"
