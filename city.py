from random import randint


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

        self.__init_blocks(self.city_map,
                           self.rows,
                           self.columns,
                           self.coverage)

    @staticmethod
    def __init_blocks(city_map, rows, columns, coverage):
        for _ in range(int(rows * columns * coverage)):
            x = randint(0, rows-1)
            y = randint(0, columns-1)
            while city_map[x][y] != 'block':
                city_map[x][y] = 'block'

    def __set_coverage_of_tover(self, x, y):
        try:
            if self.city_map[x][y] != "Tower" and x >= 0 and y >= 0:
                self.city_map[x][y] = "т"
        except IndexError:
            pass

    def set_tower(self, x, y, radius):
        self.city_map[y][x] = "Tower"
        for i in range(y-radius, y+radius+1):
            for j in range(x-radius, x+radius+1):
                self.__set_coverage_of_tover(i, j)

    def __str__(self):
        return "\n".join(map(lambda x: "\t".join(x), self.city_map))


if __name__ == "__main__":
    c1 = CityGrid(7, 7, 0.3)
    c1.set_tower(0, 0, 2)
    print(c1)
