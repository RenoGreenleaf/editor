from PyQt6.QtWidgets import QApplication
from window import Window
from sys import argv


app = QApplication(argv)

window = Window()
window.build()
window.show()

app.exec()
