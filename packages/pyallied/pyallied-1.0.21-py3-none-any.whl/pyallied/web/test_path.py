import os


def printName():
    filepath = __file__.split("\\")

    print(os.path.dirname(__file__), "my name --")


printName()
