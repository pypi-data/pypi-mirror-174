import numpy as np
import os
from glob import glob
from napari.layers import Image, Shapes, Labels
from napari.viewer import Viewer
from napari.types import LayerDataTuple
from magicgui import magic_factory
import tifffile
from skimage.io import imsave, imread

@magic_factory(call_button='Next slide',
               path={'tooltip': 'Path to the folder containing the data.'},
               keyword={'tooltip': 'Keyword to fetch data to annotate'},
               resolution={'tooltip': 'Resolution of pulled image. Higher resolution might lead to lags and slow annotation',
                           'widget_type': 'ComboBox',
                           'choices': [0, 1, 2],
                           'value': 1}
               )
def next_slide(viewer: Viewer,
               path: str='',
               keyword: str='*DAPI.tif',
               resolution: int=1) -> LayerDataTuple:
    """
    Go to next slide for annotating:
        1) Save current annotation if there is one to save
        2) Fetch the next slide to annotate

    Parameters
    ----------
    viewer: napari.Viewer
        viewer object to access layers
    path: str
        path to folder containing the data
    keyword: str
        keyword to select slides
    resolution: int
        resolution to read tiff files

    Returns
    -------
    list of LayerDataTuple to be displayed by napari
    """

    # First we check if there is something to save
    if len(viewer.layers) > 0:
        filename = viewer.layers[0].metadata['source'][:-4] + '_annotations.tif'
        imsave(filename, viewer.layers[1].data, compression='ZLIB', check_contrast=False)
        # Remove previous layers
        del viewer.layers[1]
        del viewer.layers[0]

    # Then we find all images that can be annotated
    microscopy_slides = glob(os.path.join(path, '*'))
    list_to_annotate = []
    for folder in microscopy_slides:
        existing_slides = glob(os.path.join(folder, keyword))
        # Add the slide only if there is no existing annotation
        for s in existing_slides:
            if not os.path.exists(s[:-4] + '_annotations.tif'):
                list_to_annotate.append(s)

    # If there are no slides left to annotate, go to review mode
    if list_to_annotate == []:
        review_annotations(viewer, path, keyword, resolution)

    data = read_slide(list_to_annotate[0], resolution)
    tuple_data = (data,
                  {'name': 'Slide ({} left)'.format(len(list_to_annotate)), 'contrast_limits': [0, 65000],
                   'metadata': {'source': list_to_annotate[0]}},
                  'image')
    tuple_label = (np.zeros_like(data, dtype='uint8'),
                   {'name': 'Annotation mask'},
                   'labels')

    return [tuple_data, tuple_label]

@magic_factory(call_button='Review annotations',
               path={'tooltip': 'Path to the folder containing the data.'},
               keyword={'tooltip': 'Keyword to fetch data to annotate'},
               resolution={'tooltip': 'Resolution of pulled image. Higher resolution might lead to lags and slow annotation',
                           'widget_type': 'ComboBox',
                           'choices': [0, 1, 2],
                           'value': 1}
               )
def review_annotations(viewer: Viewer,
                       path: str='',
                       keyword: str='*DAPI.tif',
                       resolution: int=1) -> LayerDataTuple:
    """
    Go to next slide for reviewing:
        1) List all annotated slides if not done already
        2) Fetch the next slide to review

    Parameters
    ----------
    viewer: napari.Viewer
        viewer object to access layers
    path: str
        path to folder containing the data
    keyword: str
        keyword to select slides
    resolution: int
        resolution to read tiff files

    Returns
    -------
    list of LayerDataTuple to be displayed by napari
    """

    if len(viewer.layers) == 0:
        # Case when you start reviwing from scratch
        # Find all images that are already annotated
        microscopy_slides = glob(os.path.join(path, '*'))
        list_annotated = []
        for folder in microscopy_slides:
            existing_slides = glob(os.path.join(folder, keyword))
            # Add the slide only if there is no existing annotation
            for s in existing_slides:
                if os.path.exists(s[:-4] + '_annotations.tif'):
                    list_annotated.append(s)
    # First we check if there is something to save
    elif len(viewer.layers) > 0:
        if 'source' in viewer.layers[0].metadata:
            # Previous mode was annotating
            # Remove previous layers
            del viewer.layers[1]
            del viewer.layers[0]
            # Find all images that are already annotated
            microscopy_slides = glob(os.path.join(path, '*'))
            list_annotated = []
            for folder in microscopy_slides:
                existing_slides = glob(os.path.join(folder, keyword))
                # Add the slide only if there is no existing annotation
                for s in existing_slides:
                    if os.path.exists(s[:-4] + '_annotations.tif'):
                        list_annotated.append(s)
        elif 'list_annotated' in viewer.layers[0].metadata:
            # Previous mode was review
            list_annotated = viewer.layers[0].metadata['list_annotated']
            list_annotated.pop(0)
            # Remove previous layers
            del viewer.layers[1]
            del viewer.layers[0]

    if len(list_annotated)>0:
        data = read_slide(list_annotated[0], resolution)
        labels = imread(list_annotated[0][:-4] + '_annotations.tif')
        tuple_data = (data,
                      {'name': 'Slide ({} left)'.format(len(list_annotated)), 'contrast_limits': [0, 65000],
                       'metadata': {'list_annotated': list_annotated}},
                      'image')
        tuple_label = (labels,
                       {'name': 'Annotation mask',
                        'scale': [data.shape[0]/labels.shape[0], data.shape[1]/labels.shape[1]]},
                        'labels')

        return [tuple_data, tuple_label]
    else:
        return None


def read_slide(path, resolution):
    """
    Read tiff at a given resolution.

    Parameters
    ----------
    path: str
        path to the stored tiff file
    resolution: int
        resolution to read (0 is highest, then 1, etc.)

    Returns
    -------
    Array containing the tiff data.
    """
    # Read largest resolution in pyramidal tif file or big tif
    with tifffile.TiffFile(path) as tif:
        pyramid = list(reversed(sorted(tif.series, key=lambda p: p.size)))

        size = pyramid[0].size
        pyramid = [p for p in pyramid if size % p.size == 0]

        return pyramid[0].levels[resolution].asarray()