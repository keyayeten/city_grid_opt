from random import randint
import seaborn as sns
import matplotlib.pyplot as plt


class SideRange:
    def __set_name__(self, owner, name):
        self.param_name = '_' + name

    def __get__(self, instance, owner):
        return getattr(instance, self.param_name)

    def __set__(self, instance, value):
        self.validate(value)
        setattr(instance, self.param_name, value)

    def validate(self, value):
        if value < 1 or not isinstance(value, int):
            raise ValueError


class CoverageRange:
    def __set_name__(self, owner, name):
        self.param_name = '_' + name

    def __get__(self, instance, owner):
        return getattr(instance, self.param_name)

    def __set__(self, instance, value):
        self.validate(value)
        setattr(instance, self.param_name, value)

    def validate(self, value):
        if value < 0.3 or not isinstance(value, float):
            raise ValueError


class CityGrid:
    rows = SideRange()
    columns = SideRange()
    coverage = CoverageRange()

    def __init__(self,
                 rows: int,
                 columns: int,
                 coverage: float):
        self.rows = rows
        self.columns = columns
        self.coverage = coverage
        self.city_map = [['-'
                          for _ in range(columns)]
                         for _ in range(rows)]
        self.towers = []
        self.blocks = []

        self.__init_blocks(self.city_map,
                           self.rows,
                           self.columns,
                           self.coverage)

    def __init_blocks(self, city_map, rows, columns, coverage):
        for _ in range(int(rows * columns * coverage)):
            x = randint(0, rows-1)
            y = randint(0, columns-1)
            while city_map[x][y] != 'block':
                city_map[x][y] = 'block'
                self.blocks.append((x, y))

    def __set_coverage_of_tover(self, x, y):
        try:
            if (self.city_map[x][y] != "Tower" and x >= 0
                    and y >= 0 and self.city_map[x][y] != "block"):
                self.city_map[x][y] = "т"
        except IndexError:
            pass

    def set_tower(self, x, y, radius):
        if self.city_map[y][x] == "block":
            raise ValueError("Cannot place tower on a block")
        self.city_map[y][x] = "Tower"
        self.towers.append({"coords": (x, y),
                            "radius": radius})
        for i in range(y-radius, y+radius+1):
            for j in range(x-radius, x+radius+1):
                self.__set_coverage_of_tover(i, j)

    def __str__(self):
        return "\n".join(map(lambda x: "\t".join(x), self.city_map))

    def __convert_for_vizualization(self) -> list[list[int]]:
        return [[0 if i == "-" else
                 1 if i == "Tower" or i == "т" else -1
                 for i in j]
                for j in self.city_map]

    def visualize_map(self):
        converted = self.__convert_for_vizualization()
        sns.heatmap(converted, cmap='coolwarm', annot=True)
        plt.show()

    def optimize_tower_placement(self, radius: int = 1):
        uncovered_blocks = []
        placed_towers = []

        for i in range(self.rows):
            for j in range(self.columns):
                if self.city_map[i][j] == '-':
                    uncovered_blocks.append((i, j, radius))

        while uncovered_blocks:
            max_coverage = 0
            best_block = None

            for block in uncovered_blocks:
                x, y, cov_rad = block
                coverage = self.calculate_block_coverage(x, y, cov_rad)
                if coverage > max_coverage:
                    max_coverage = coverage
                    best_block = block

            if best_block is None:
                break

            x, y, cov_rad = best_block
            self.set_tower(y, x, cov_rad)
            placed_towers.append(best_block)
            uncovered_blocks = [b for b in uncovered_blocks
                                if not self.is_block_covered(*b)]

    def is_block_covered(self, x, y, radius: int = 1):
        for i in range(x - radius, x + radius + 1):
            for j in range(y - radius, y + radius + 1):
                if 0 <= i < self.rows and 0 <= j < self.columns:
                    if self.city_map[i][j] == 'Tower':
                        return True
        return False

    def calculate_block_coverage(self, x, y, radius: int = 1):
        covered_blocks = set()

        for i in range(x - radius, x + radius + 1):
            for j in range(y - radius, y + radius + 1):
                if 0 <= i < self.rows and 0 <= j < self.columns:
                    if self.city_map[i][j] != 'block':
                        covered_blocks.add((i, j))

        return len(covered_blocks)


if __name__ == "__main__":
    c1 = CityGrid(10, 10, 0.3)
    # c1.set_tower(2, 1, 2)
    print(c1)

    c1.optimize_tower_placement(radius=2)
    print(c1.towers)
    print(c1.blocks)
    c1.visualize_map()
