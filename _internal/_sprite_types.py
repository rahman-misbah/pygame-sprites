from typing import Union, Any, TypeIs, cast
import pygame

# =============== TYPE ALIASES ===============  #

type RGB = tuple[int, int, int]

type SpriteGridRow = list[pygame.Surface | None]

type SpriteGrid = list[SpriteGridRow]

type Coordinate = tuple[int, int]

type Size = tuple[int, int]

type RowSlice = tuple[int, slice]

type ColumnSlice = tuple[slice, int]

type Region = tuple[slice, slice]

type Alpha = Union[
    Coordinate,
    RGB
]

type NonStringSpriteIndex = Union[
    int,        # Row Index
    Coordinate,
    RowSlice,
    ColumnSlice,
    Region
]

type SpriteIndex = Union[
    str,        # Named Group
    NonStringSpriteIndex
]

type SpriteFetch = Union[
    SpriteGrid,
    SpriteGridRow,
    pygame.Surface
]

type ExportableSprite = Union[
    SpriteIndex,
    pygame.Surface
]

type SpriteExtraction = tuple[
    int,        # Sprite Count
    Size,
    SpriteGrid
]

# =============== TYPE CHECKERS ===============  #

def is_coordinate(value: Any) -> TypeIs[Coordinate]:
    if not isinstance(value, tuple):
        return False
    
    safe_tuple = cast(tuple[Any, ...], value)

    if len(safe_tuple) != 2:
        return False
    
    return all(isinstance(i, int) for i in safe_tuple)

def is_region(value: Any) -> TypeIs[Region]:
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

def is_sprite_grid_row(value: Any) -> TypeIs[]