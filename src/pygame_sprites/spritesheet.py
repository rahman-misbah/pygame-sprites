# Sprite class
# Handles sprite extraction and storage
# TODO: Implement a validation method that check if for a given sheet, tile_size, padding, etc. valid tiles can be extracted

import pygame
from pathlib import Path
from typing import Optional, Any, cast
from beartype import beartype

import pygame_sprites.definitions as definitions
import pygame_sprites._internal.validators as validators



class SpriteSheet:
    @beartype
    def __init__(
            self, 
            sheet_path : str, 
            tile_size : definitions.Size, 
            padding : int = 0, 
            sheet_margin : int = 0, 
            alpha : Optional[definitions.Alpha] = None, 
            verbose : bool = False
            ):
        '''
            alpha:  tuple (x, y) - coordinate to sample transparency color
                    OR tuple (r, g, b) - specific color to use as transparent
        '''
        
        self.__sheet_path = sheet_path
        self.__tile_size = tile_size
        self.__padding = padding
        self.__sheet_margin = sheet_margin
        self.__verbose = verbose

        self.__spritesheet = self.__load_spritesheet()
        self.__alpha : Optional[definitions.RGB] = self.__set_alpha(alpha)
        self.__sprite_count, self.__grid_dim, self.__sprites = self.__extract_sprites()
        self.__map : definitions.NamedGroupMap = dict()
    
    
    #   =============== PUBLIC INTERFACE ===============  #

    @beartype
    def name_tiles(
            self,
            index : definitions.NonStringSpriteIndex,
            name : str
            ) -> None:
        
        pass
    
    @beartype
    def png(self,
            sprite : Optional[definitions.ExportableSprite] = None,
            name : str = "sprite",
            path : str = "png"
            ) -> None:

        directory = Path(path)
        if not directory.exists():
            directory.mkdir()
            if self.__verbose: print(f"Created directory '{path}'")
        
        export_count = 0

        if sprite is None:
            pass
        
        elif isinstance(sprite, pygame.Surface):
            pygame.image.save(sprite, f"{path}/{name}.png")
            export_count += 1

        else:
            tiles = self[sprite]

            if isinstance(tiles, pygame.Surface):
                pygame.image.save(tiles, f"{path}/{name}.png")
                export_count += 1
            
            elif True:
                pass
        


        if self.__verbose:
            print(f"Exported {export_count} images to directory '{path}'")

    #   =============== GETTERS AND SETTERS ===============  #

    @beartype
    def __getitem__(
            self, 
            pos : definitions.SpriteIndex
            ) -> Optional[definitions.SpriteFetch]:
        if isinstance(pos, int):
            try:
                return self.__sprites[pos]
            except IndexError:
                raise IndexError(f"Index {pos} out of range")

        if isinstance(pos, str):
            # Fetch by key logic
            pass

        if validators.is_coordinate(pos):
            try:
                return self.__sprites[pos[0]][pos[1]]
            except IndexError:
                raise IndexError(f"Index [{pos[0]}, {pos[1]}] out of range")

        if validators.is_row_slice(pos):
            try:
                row = self.__sprites[pos[0]]
                return row[pos[1]]
            except IndexError:
                raise IndexError(f"Invalid row index {pos[0]}")

        if validators.is_column_slice(pos):
            try:
                rows = self.__sprites[pos[0]]
                result = [row[pos[1]] for row in rows]

                return result
            except:
                raise IndexError(f"Invalid column index {pos[1]}")

        if validators.is_region(pos):
            rows = self.__sprites[pos[0]]
            result = [row[pos[1]] for row in rows]
            
            return result

    @property
    def sprite_count(self) -> int:
        return self.__sprite_count

    @property
    def row_count(self) -> int:
        return self.__grid_dim[0]
    
    @property
    def column_count(self) -> int:
        return self.__grid_dim[1]
    
    def toggle_verbose(self) -> None:
        self.__verbose = not self.__verbose

    #   =============== PRIVATE IMPLEMENTATION ===============  #

    def __load_spritesheet(self) -> pygame.Surface:
        try:
            spritesheet = pygame.image.load(self.__sheet_path)

            if self.__verbose:
                print("Loaded spritesheet", self.__sheet_path)
        except:
            raise ValueError(f"Cannot load spritesheet {self.__sheet_path}")
        
        return spritesheet

    def __set_alpha(
            self, 
            alpha : Optional[definitions.Alpha]
            ) -> Optional[definitions.RGB]:
        if alpha is None:       # Uses per-pixel alpha
            self.__spritesheet = self.__spritesheet.convert_alpha()

            if self.__verbose:
                print("Using per-pixel alpha (conver_alpha)")
        
            return None
        
        # Uses provided alpha
        self.__spritesheet = self.__spritesheet.convert()

        # Alpha provided from spritesheet pixel
        if validators.is_coordinate(alpha):
            try:
                bg_color = self.__spritesheet.get_at(alpha)
                self.__spritesheet.set_colorkey(bg_color)

                if self.__verbose:
                    print(f"Set colorkey from pixel {alpha}: {bg_color}")
                
                return (bg_color.r, bg_color.g, bg_color.b)
            
            except IndexError:
                raise ValueError(f"Invalid alpha coordinates {alpha}")
        
        # Alpha provided using (r, g, b) value
        else:
            self.__spritesheet.set_colorkey(alpha)

            if self.__verbose:
                print(f"Set colorkey to color: {alpha}")
            
            return alpha
    
    def __extract_sprites(self) -> definitions.SpriteExtraction:
        sheet_size = self.__spritesheet.get_size()
        sprite_count : int = 0
        transparent_count : int = 0
        
        cols = (sheet_size[0] - self.__sheet_margin * 2) // (self.__tile_size[0] + 2 * self.__padding)
        rows = (sheet_size[1] - self.__sheet_margin * 2) // (self.__tile_size[1] + 2 * self.__padding)
        tile_rect = pygame.Rect(0, 0, self.__tile_size[0], self.__tile_size[1])
        
        sprites : definitions.SpriteGrid = []

        for i in range(rows):
            row : definitions.SpriteGridRow = []
            sprites.append(row)

            for j in range(cols):
                x = self.__sheet_margin + ((self.__tile_size[0] + self.__padding * 2) * j) + self.__padding
                y = self.__sheet_margin + ((self.__tile_size[1] + self.__padding * 2) * i) + self.__padding

                tile_rect.x = x
                tile_rect.y = y

                tile = self.__spritesheet.subsurface(tile_rect)

                if not self.__transparent_tile(tile, self.__alpha):
                    sprites[i].append(tile)
                    sprite_count += 1
                else:
                    sprites[i].append(None)
                    transparent_count += 1
                    
        
        if self.__verbose:
            print(f"Extracted {sprite_count} sprites")
            print(f"Detected {transparent_count} transparent tiles")
        
        sprite_dim = (len(sprites), len(sprites[0]))
        
        return sprite_count, sprite_dim, sprites 
    
    def __transparent_tile(
            self, 
            tile : pygame.Surface, 
            alpha : Optional[definitions.RGB]
        ) -> bool:
        tile.lock()
        pixel_array : Optional[pygame.PixelArray] = None

        try:
            width, height = tile.get_size()
            pixel_array = pygame.PixelArray(tile)

            for x in range(width):
                column = cast(Any, pixel_array[x])
                    
                for y in range(height):
                    pixel_value = cast(int, column[y])
                    pixel_color = tile.unmap_rgb(pixel_value)

                    if alpha is not None:
                        if pixel_color[:3] != alpha:
                            return False
                    elif len(pixel_color) == 4 and pixel_color[3] > 0:
                        return False
            
            return True

        except Exception as e:
            raise e

        finally:
            if pixel_array is not None:
                pixel_array.close()
                del pixel_array
            tile.unlock()
