from controller import Controller
from view import View

if __name__ == '__main__':
    V = View()
    C = Controller(V)

    C.start()
