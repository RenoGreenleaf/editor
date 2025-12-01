import PyQt6.QtWidgets as widgets


class Window(widgets.QMainWindow):
	"""An app needs a main window."""

	def build(self):
		options = widgets.QWidget()
		options_layout = widgets.QVBoxLayout(options)

		for i in range(10):
			option = widgets.QGroupBox()
			option_layout = widgets.QVBoxLayout(option)
			option_layout.addWidget(widgets.QLineEdit())
			options_layout.addWidget(option)

		scroller = widgets.QScrollArea()
		scroller.setWidget(options)

		root = widgets.QWidget()
		root_layout = widgets.QVBoxLayout(root)
		root_layout.addWidget(scroller)
		self.setCentralWidget(root)
