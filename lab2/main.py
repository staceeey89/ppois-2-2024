import tkinter

from src.view.main_window import MainWindow
from src.presenter.main_window_presenter import MainWindowPresenter
from src.model.DAO.db_repository import DBRepository


window = MainWindow()
presenter = MainWindowPresenter(window)

window.mainloop()
