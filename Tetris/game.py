from grid import Grid
from blocks import *
import random
import pygame


class Game:
    def __init__(self, sound_path, music_path):
        self.grid = Grid()
        self.blocks = [
            IBlock(),
            JBlock(),
            LBlock(),
            OBlock(),
            SBlock(),
            TBlock(),
            ZBlock(),
        ]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.game_over = False
        self.score = 0
        self.clear_sound = pygame.mixer.Sound(sound_path)
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)

    def update_score(self, lines_cleared, move_down_points):
        if lines_cleared == 1:
            self.score += 100
        elif lines_cleared == 2:
            self.score += 300
        elif lines_cleared == 3:
            self.score += 500
        self.score += move_down_points

    def get_random_block(self):
        if len(self.blocks) == 0:
            self.blocks = [
                IBlock(),
                JBlock(),
                LBlock(),
                OBlock(),
                SBlock(),
                TBlock(),
                ZBlock(),
            ]
        block = random.choice(self.blocks)
        self.blocks.remove(block)
        return block

    def move_left(self):
        self.current_block.move(0, -1)
        if not self.block_inside() or not self.block_fits():
            self.current_block.move(0, 1)

    def move_right(self):
        self.current_block.move(0, 1)
        if not self.block_inside() or not self.block_fits():
            self.current_block.move(0, -1)

    def move_down(self):
        self.current_block.move(1, 0)
        if not self.block_inside() or not self.block_fits():
            self.current_block.move(-1, 0)
            self.lock_block()

    def hard_drop(self):
        # Move the block down until it can't move further
        while True:
            self.current_block.move(1, 0)
            if not self.block_inside() or not self.block_fits():
                self.current_block.move(-1, 0)
                self.lock_block()
                break

    def lock_block(self):
        tiles = self.current_block.get_cell_position()
        for position in tiles:
            if self.grid.is_inside(position.row, position.column):
                self.grid.grid[position.row][position.column] = self.current_block.id
        self.current_block = self.next_block
        self.next_block = self.get_random_block()
        rows_cleared = self.grid.clear_full_rows()
        if rows_cleared > 0:
            self.clear_sound.play()
            self.update_score(rows_cleared, 0)
        # Check if the new block fits; if not, game over
        if not self.block_fits():
            self.game_over = True

    def reset(self):
        self.grid.reset()
        self.blocks = [
            IBlock(),
            JBlock(),
            LBlock(),
            OBlock(),
            SBlock(),
            TBlock(),
            ZBlock(),
        ]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.score = 0

    def block_fits(self):
        tiles = self.current_block.get_cell_position()
        for tile in tiles:
            if not self.grid.is_inside(tile.row, tile.column):
                return False
            if not self.grid.is_empty(tile.row, tile.column):
                return False
        return True

    def rotate(self):
        self.current_block.rotate()
        if self.block_inside() == False:
            self.current_block.undo_rotation()

    def block_inside(self):
        tiles = self.current_block.get_cell_position()
        for tile in tiles:
            if self.grid.is_inside(tile.row, tile.column) == False:
                return False
        return True

    def get_ghost_block(self):
        # Create a copy of the current block
        import copy

        ghost = copy.deepcopy(self.current_block)
        # Move it down until it can't move further
        while True:
            ghost.move(1, 0)
            tiles = ghost.get_cell_position()
            if not all(
                self.grid.is_inside(t.row, t.column)
                and self.grid.is_empty(t.row, t.column)
                for t in tiles
            ):
                ghost.move(-1, 0)
                break
        return ghost

    def draw_ghost(self, screen, offset_x, offset_y):
        ghost = self.get_ghost_block()
        ghost.draw(
            screen,
            color=(180, 180, 180),
            outline=True,
            offset_x=offset_x,
            offset_y=offset_y,
        )

    def draw(self, screen):
        self.grid.draw(screen)
        self.draw_ghost(screen, 11, 11)  # Draw ghost before the current block
        self.current_block.draw(screen, 11, 11)
        self.next_block.draw(screen, 270, 300)
