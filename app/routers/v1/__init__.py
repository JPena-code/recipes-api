__version__ = '1.0.0'

API_VERSION = 'v1.0'

from . import tag
from . import category
from . import recipe
from . import user

__all__ = [
    'tag',
    'category',
    'recipe',
    'user'
]
