import os.path
import numpy as np
from typing import List, Any, Optional, Union, Tuple, Dict
from napari.types import ReaderFunction
from napari.layers import Shapes

def napari_get_reader(path: Union[str, List[str]]) -> Optional[ReaderFunction]:
    """
    No reader implemented yet.

    Parameters
    ----------
    path : str or list of str
        Path to a '.raw' file, or a list of such paths.
    Returns
    -------
    function or None
        If the path is of the correct format, return a function that accepts the
        same path or list of paths, and returns a list of layer data tuples.
        Otherwise returns ``None``.
    """

    return None