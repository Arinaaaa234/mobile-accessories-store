class Humanity:
    """Батьківський клас для прикладу ООП з лабораторної роботи."""

    def __init__(self, name, population, main_goal):
        self.name = name
        self._population = population
        self.main_goal = main_goal

    @property
    def population(self):
        return self._population

    @population.setter
    def population(self, value):
        if value < 0:
            raise ValueError("Кількість людей не може бути від'ємною")
        self._population = value

    def communicate(self):
        return f"{self.name} спілкується, щоб досягти мети: {self.main_goal}."

    def develop(self):
        return f"{self.name} розвивається через освіту, працю та технології."


class StoreCommunity(Humanity):
    """Дочірній клас, логічно пов'язаний з людством через спільноту покупців."""

    def __init__(self, name, population, main_goal, favorite_category):
        super().__init__(name, population, main_goal)
        self.favorite_category = favorite_category

    def communicate(self):
        return (
            f"{self.name} обмінюється відгуками про аксесуари, "
            f"особливо категорію: {self.favorite_category}."
        )

    def buy_accessory(self, product_name):
        return f"{self.name} купує товар: {product_name}."
