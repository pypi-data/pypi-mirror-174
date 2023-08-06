from collections import namedtuple

XAImageModification = namedtuple('ImageModification', ['original_image', 'result'])
"""A named tuple returned by image manipulation operations such as :func:`pixellate` containing the original image and the result after applying modifications.
"""



