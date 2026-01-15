from typing import Union
import pygame

type NonStringSpriteIndexType = Union[
    int,
    tuple[int, int],
    tuple[int, slice],
    tuple[slice, int],
    tuple[slice, slice]
]

type SpriteIndexType = Union[
    NonStringSpriteIndexType,
    str
]

type GameSurfaceType = pygame.Surface

type SpriteFetchType = Union[
    list[pygame.Surface|None],
    GameSurfaceType
]

type ExportableSpriteType = Union[
    SpriteIndexType,
    GameSurfaceType
]

type AlphaType = Union[
    tuple[int, int],
    tuple[int, int, int]
]

type RGBType = tuple[int, int, int]

type SpriteGridRowType = list[GameSurfaceType | None]

type SpriteGridType = list[SpriteGridRowType]

type SpriteExtractionType = tuple[
    SpriteGridType,
    tuple[int, int],
    int
]