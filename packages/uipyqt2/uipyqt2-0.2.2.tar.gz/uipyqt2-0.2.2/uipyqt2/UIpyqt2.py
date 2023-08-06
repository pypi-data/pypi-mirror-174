import PyQt6
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt6.QtWidgets import *

import sys # Только для доступа к аргументам командной строки

# Приложению нужен один (и только один) экземпляр QApplication.
# Передаём sys.argv, чтобы разрешить аргументы командной строки для приложения.
# Если не будете использовать аргументы командной строки, QApplication([]) тоже работает
class WinUI():
    def __init__(self,arg = sys.argv):
        super().__init__()
        
    

    
class NewWin(WinUI):
    def __init__(self,arg = sys.argv,show = False):
        super().__init__()
        self.arg = arg
        self.app = QApplication(arg)
        self.window = QWidget()
        if show == True or show == 1:
            self.window.show()
    def SetFixedWinSize(self,x,y):
        self.window.setFixedSize(QSize(x, y))
    def SetMaxWinSize(self,x,y):
        self.window.setMaximumSize(QSize(x, y))
    def SetMinWinSize(self,x,y):
        self.window.setMinimumSize(QSize(x, y))
    def mainloop(self):
        self.app.exec()
    def show(self):
        self.window.show()
    def hide(self):
        self.window.hide()  # Важно: окно по умолчанию скрыто.
    def Title(self,text):
        text = str(text)
        self.window.setWindowTitle(text)
        
        
class Button(WinUI):
    def __init__(self,text):
        super().__init__()
        self.text = text
        button = QPushButton(text)
     
win = NewWin(show=1)
win.mainloop()
    # Запускаем цикл событий.

    # Создаём виджет Qt — окно.
    