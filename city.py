from random import randint, choice, uniform
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
        self.paths = {}

        self.__init_blocks()

    def __init_blocks(self):

        """Initializing blocks to city map"""

        for _ in range(int(self.rows * self.columns * self.coverage)):
            x = randint(0, self.rows-1)
            y = randint(0, self.columns-1)
            while self.city_map[x][y] != 'block':
                self.city_map[x][y] = 'block'
                self.blocks.append((x, y))

    def __set_coverage_of_tover(self, x: int, y: int):

        """Sets area of tower coverage."""

        try:
            if (self.city_map[x][y] != "Tower" and x >= 0
                    and y >= 0 and self.city_map[x][y] != "block"):
                self.city_map[x][y] = "т"
        except IndexError:
            pass

    def set_tower(self,
                  x: int,
                  y: int,
                  radius: int):

        """Sets tower with coverage area"""

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

        """Converts city map to integer lists"""

        return [[0 if i == "-" else
                 1 if i == "Tower" or i == "т" else -1
                 for i in j]
                for j in self.city_map]

    def visualize_map(self):

        """Vizuals city map as integer heatmap"""

        converted = self.__convert_for_vizualization()
        sns.heatmap(converted, cmap='coolwarm', annot=True)
        plt.show()

    def optimize_tower_placement(self, radius: int = 1):

        """Sets optimal number of towers."""

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

    def is_block_covered(self,
                         x: int,
                         y: int,
                         radius: int = 1) -> bool:

        """Checks coverage of a block"""

        for i in range(x - radius, x + radius + 1):
            for j in range(y - radius, y + radius + 1):
                if 0 <= i < self.rows and 0 <= j < self.columns:
                    if self.city_map[i][j] == 'Tower':
                        return True
        return False

    def calculate_block_coverage(self,
                                 x: int,
                                 y: int,
                                 radius: int = 1) -> int:

        """Returns block coverage"""

        covered_blocks = set()

        for i in range(x - radius, x + radius + 1):
            for j in range(y - radius, y + radius + 1):
                if 0 <= i < self.rows and 0 <= j < self.columns:
                    if self.city_map[i][j] != 'block':
                        covered_blocks.add((i, j))

        return len(covered_blocks)

    def get_path(self,
                 start: tuple[int, int],
                 end: tuple[int, int]) -> list[tuple[int, int]]:

        """Returns reliable path between two towers,
        or empty list if path doesn't exist.
        """

        if (start, end) in self.paths:
            return self.paths[(start, end)]

        paths = [[start]]

        while paths:
            curr_path = paths.pop(0)
            curr_pos = curr_path[-1]

            if curr_pos == end:
                self.paths[(start, end)] = curr_path
                return curr_path

            neighbors = self.get_neighbors(curr_pos)

            for neighbor in neighbors:
                if neighbor not in curr_path and neighbor not in self.blocks:
                    new_path = curr_path + [neighbor]
                    paths.append(new_path)

        return []

    def get_neighbors(self, coords: tuple[int, int]) -> list[tuple[int, int]]:

        """Returns list of towers neighbours"""

        x, y = coords
        neighbors = []

        for tower in self.towers:
            tower_coords = tower['coords']
            tower_radius = tower['radius']

            dx = tower_coords[0] - x
            dy = tower_coords[1] - y
            distance = (dx**2 + dy**2)**0.5

            if distance <= tower_radius:
                neighbors.append(tower_coords)
        return neighbors


if __name__ == "__main__":
    c1 = CityGrid(randint(10, 20),
                  randint(10, 20),
                  uniform(0.3, 0.9))

    # c1.set_tower(2, 1, 2)
    print(c1)

    c1.optimize_tower_placement(radius=randint(1, 10))
    print(c1.towers)
    print(c1.blocks)
    c1.visualize_map()
    print(c1.get_path(choice(c1.towers)["coords"],
                      choice(c1.towers)["coords"],))
