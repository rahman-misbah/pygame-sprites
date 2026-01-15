from typing import Union, Any, TypeIs, cast
import pygame

# =============== TYPE ALIASES ===============  #

type RGB = tuple[int, int, int]

type SpriteGridRow = list[pygame.Surface | None]

type SpriteGrid = list[SpriteGridRow]

type Alpha = Union[
    tuple[int, int],
    RGB
]

type NonStringSpriteIndex = Union[
    int,
    tuple[int, int],
    tuple[int, slice],
    tuple[slice, int],
    tuple[slice, slice]
]

type SpriteIndex = Union[
    NonStringSpriteIndex,
    str
]

type SpriteFetch = Union[
    list[SpriteGridRow],
    SpriteGridRow,
    pygame.Surface
]

type ExportableSprite = Union[
    SpriteIndex,
    pygame.Surface
]

type SpriteExtraction = tuple[
    SpriteGrid,
    tuple[int, int],
    int
]

# =============== TYPE CHECKERS ===============  #

def is_int_pair(value: Any) -> TypeIs[tuple[int, int]]:
    if not isinstance(value, tuple):
        return False
    
    safe_tuple = cast(tuple[Any, ...], value)

    if len(safe_tuple) != 2:
        return False
    
    return all(isinstance(i, int) for i in safe_tuple)

def is_slice_pair(value: Any) -> TypeIs[tuple[slice, slice]]:
    if not isinstance(value, tuple):
        return False
    
    slice_tuple = cast(tuple[Any, ...], value)
    
    if len(slice_tuple) != 2:
        return False
    
    return isinstance(slice_tuple[0], slice) and isinstance(slice_tuple[1], slice)

def is_row_slice(value: Any) -> TypeIs[tuple[int, slice]]:
    if not isinstance(value, tuple):
        return False
    
    slice_tuple = cast(tuple[Any, ...], value)
    
    if len(slice_tuple) != 2:
        return False
    
    return isinstance(slice_tuple[0], int) and isinstance(slice_tuple[1], slice)

def is_column_slice(value: Any) -> TypeIs[tuple[slice, int]]:
    if not isinstance(value, tuple):
        return False
    
    slice_tuple = cast(tuple[Any, ...], value)
    
    if len(slice_tuple) != 2:
        return False
    
    return isinstance(slice_tuple[0], slice) and isinstance(slice_tuple[1], int)