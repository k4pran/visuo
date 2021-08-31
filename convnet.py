from typing import Sequence

from manim import *


class GridGroup(VGroup):
    def align_points_with_larger(self, larger_mobject):
        pass

    def __init__(
        self,
        rows,
        cols,
        colors: Sequence = (WHITE),
        buff=0.0,
        cell_scale_factor=1.0,
        *vmobjects,
        **kwargs
    ):
        super().__init__(*vmobjects, **kwargs)
        self.rows = rows
        self.cols = cols
        self.colors = colors
        self.buff = buff
        self.cell_scale_factor = cell_scale_factor
        self.generate_colored_grid()

    def generate_cell(self, color):
        square = Square(fill_color=color, fill_opacity=1)
        return square

    def generate_colored_grid(self):
        for i in range(self.rows * self.cols):
            cell = self.generate_cell(self.colors[i % len(self.colors)]).scale(
                self.cell_scale_factor
            )
            self.add(cell)
        self.arrange_in_grid(self.rows, self.cols, buff=self.buff)
        self[2].set_fill(WHITE, opacity=0.2)

    def get_flattened_index(self, row, col):
        assert row >= 0 and col >= 0
        assert row < self.rows and col < self.cols
        return row * self.cols + col

    def get_cell_at(self, row, col):
        return self[self.get_flattened_index(row, col)]

    def get_cell_block(self, row_start, col_start, size: tuple = (2, 2)):
        assert len(size) == 2
        start_index = self.get_flattened_index(row_start, col_start)
        start_cells = self[start_index : start_index + size[1]]

        end_index = self.get_flattened_index(row_start + size[0] - 1, col_start)
        end_cells = self[end_index : end_index + size[1]]

        return start_cells + end_cells


class Grid(Scene):
    def get_scale_factor(self, rows, cell_height, padding=0.4):
        target_height = config.frame_height - (padding * 2)
        return target_height / (cell_height * rows)

    def construct(self):
        kernel_size = (2, 2)
        rows = 4
        cols = 4
        scale_factor = self.get_scale_factor(rows, Square().height)
        grid = GridGroup(
            rows, cols, [RED, BLUE, YELLOW], buff=0, cell_scale_factor=scale_factor
        )
        kernal_loc = grid[0 : kernel_size[0]] + grid[cols : kernel_size[1] + cols]
        kernal = SurroundingRectangle(kernal_loc, color=BLACK, buff=0, fill_opacity=0.5)

        self.add(grid)
        self.play(FadeIn(kernal))

        for i in range(rows - kernel_size[0] + 1):
            for j in range(cols - kernel_size[1] + 1):
                kernal_loc = grid.get_cell_block(i, j)
                self.play(kernal.animate.move_to(kernal_loc))
