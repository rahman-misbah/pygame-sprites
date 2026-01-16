from typing import Union
import pygame

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

type NamedGroup = Union[
    SpriteGrid,
    SpriteGridRow
]

type NamedGroupMap = dict[str, NamedGroup]

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