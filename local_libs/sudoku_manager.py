from sudokugen.solver import solve
from sudokugen.generator import generate, Difficulty
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import copy

class SudokuManager:
    def __init__(self):
        self.problem = None
        self.solution = None
        self.user_solution = None
        self.difficulty = Difficulty.HARD

        self.font_file = 'simhei'
        self.font_size = 100
        self.bold = 10
        self.regular = 2
        self.image_height = 900
        self.image_width = 900
        self.horizontal_offset = 20
        self.vertical_offset = 0
        self.bg_color = (255, 255, 255)
        self.problem_color = '#660874'
        self.user_color = '#0066CC'
        self.font = ImageFont.truetype(self.font_file, self.font_size)

    def generate(self):
        while True:
            try:
                problem = generate(difficulty=self.difficulty)
                break
            except Exception as e:
                pass

        self.solution = problem[1]
        self.problem = [problem[0][9 * row: 9 * (row + 1)] for row in range(9)]
        self.user_solution = copy.deepcopy(self.problem)

        print(self.problem)
        #self.solution = solve(self.problem)
        print(self.solution)

    def user_fill(self, row, col, number):
        if not self.problem:
            return False, '未加载题目！'
        elif row < 0 or row >= 9 or col < 0 or col >= 9:
            return False, '不能往那儿填，超出边界啦！'
        elif self.problem[row][col] != 0:
            return False, '往这儿填会把题改掉的！'
        else:
            self.user_solution[row][col] = number

            if self.user_solution == self.solution:
                return True, 'Finished'

            out_str = ''

            for row in range(9):
                out_str += str(self.user_solution[row])
                out_str += '\n'

            return True, out_str

    def generate_image(self, filename='test.jpg', option='user'):
        if not self.problem:
            return '未加载题目！'
        else:
            pass

        im = Image.new('RGB', (self.image_width, self.image_height), self.bg_color)
        d = ImageDraw.Draw(im)

        row_unit = self.image_height / 9
        col_unit = self.image_width / 9

        d.line([(0, row_unit * 1), (self.image_width, row_unit * 1)], fill='#888888', width=self.regular)
        d.line([(0, row_unit * 2), (self.image_width, row_unit * 2)], fill='#888888', width=self.regular)

        d.line([(0, row_unit * 3), (self.image_width, row_unit * 3)], fill='#000000', width=self.bold)

        d.line([(0, row_unit * 4), (self.image_width, row_unit * 4)], fill='#888888', width=self.regular)
        d.line([(0, row_unit * 5), (self.image_width, row_unit * 5)], fill='#888888', width=self.regular)

        d.line([(0, row_unit * 6), (self.image_width, row_unit * 6)], fill='#000000', width=self.bold)

        d.line([(0, row_unit * 7), (self.image_width, row_unit * 7)], fill='#888888', width=self.regular)
        d.line([(0, row_unit * 8), (self.image_width, row_unit * 8)], fill='#888888', width=self.regular)

        # ===============================================================================

        d.line([(col_unit * 1, 0), (col_unit * 1, self.image_height)], fill='#888888', width=self.regular)
        d.line([(col_unit * 2, 0), (col_unit * 2, self.image_height)], fill='#888888', width=self.regular)

        d.line([(col_unit * 3, 0), (col_unit * 3, self.image_height)], fill='#000000', width=self.bold)

        d.line([(col_unit * 4, 0), (col_unit * 4, self.image_height)], fill='#888888', width=self.regular)
        d.line([(col_unit * 5, 0), (col_unit * 5, self.image_height)], fill='#888888', width=self.regular)

        d.line([(col_unit * 6, 0), (col_unit * 6, self.image_height)], fill='#000000', width=self.bold)

        d.line([(col_unit * 7, 0), (col_unit * 7, self.image_height)], fill='#888888', width=self.regular)
        d.line([(col_unit * 8, 0), (col_unit * 8, self.image_height)], fill='#888888', width=self.regular)

        if option.lower() == 'user':
            table = self.user_solution
        elif option.lower() == 'answer':
            table = self.solution
        else:
            table = self.problem

        for row in range(9):
            for col in range(9):
                start_x = col_unit * col
                start_y = row_unit * row

                if table[row][col] == 0:
                    continue
                elif self.problem[row][col] == 0:
                    color = self.user_color
                else:
                    color = self.problem_color

                d.text((start_x + self.horizontal_offset, start_y + self.vertical_offset),
                       str(table[row][col]), fill=color, font=self.font)

        im.save(filename)


if __name__ == '__main__':
    manager = SudokuManager()
    manager.generate()
    manager.generate_image()
    manager.generate_image('solution.jpg', option='answer')
