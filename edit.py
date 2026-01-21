# Copyright (C) 2026  Reno Greenleaf
from qtpy.QtWidgets import QApplication
from window import Window
from sys import argv


app = QApplication(argv)

window = Window()
window.build()
window.show()

app.exec()
