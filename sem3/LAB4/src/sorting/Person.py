
class Person:
    """
    Simple user-defined class to demonstrate sorting of custom objects.
    Comparable by (age, name) via key functions, not by __lt__ to keep flexibility.
    """
    __slots__ = ("name", "age")
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def __repr__(self):
        return f"{self.name}({self.age})"
