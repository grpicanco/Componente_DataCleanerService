# This is a sample Python script.
from Componente import *
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi():
    regra = Componente()
    for item in regra.listar_regras():
        print(item)

    print(regra.detalhar_regra('RG002'))
    print(regra.detalhar_regra('RG015'))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
