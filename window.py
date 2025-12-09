from PyQt6 import QtWidgets as widgets, QtGui as gui
from option import Option


class Window(widgets.QMainWindow):
	"""An app needs a main window."""

	def __init__(self):
		self.last_id = 0
		super().__init__()

	def build(self):
		self.setFixedHeight(600)
		self.setFixedWidth(800)

		options = widgets.QWidget()
		self.options_layout = widgets.QVBoxLayout(options)

		scroller = widgets.QScrollArea()
		scroller.setWidgetResizable(True)
		scroller.setWidget(options)

		root = widgets.QWidget()
		root_layout = widgets.QVBoxLayout(root)
		root_layout.addWidget(scroller)
		self.setCentralWidget(root)

		toolbar = widgets.QToolBar()
		self.addToolBar(toolbar)

		add = gui.QAction("Add", self)
		add.triggered.connect(self.add)
		toolbar.addAction(add)

	def add(self):
		option = Option()
		option.build()
		self.options_layout.addWidget(option)

		self.last_id += 1
		option.setObjectName(str(self.last_id))
