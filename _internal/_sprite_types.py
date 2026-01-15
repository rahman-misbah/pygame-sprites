from typing import Union
import pygame

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
    list[pygame.Surface|None],
    pygame.Surface
]

type ExportableSprite = Union[
    SpriteIndex,
    pygame.Surface
]

type Alpha = Union[
    tuple[int, int],
    RGB
]

type RGB = tuple[int, int, int]

type SpriteGridRow = list[pygame.Surface | None]

type SpriteGrid = list[SpriteGridRow]

type SpriteExtraction = tuple[
    SpriteGrid,
    tuple[int, int],
    int
]