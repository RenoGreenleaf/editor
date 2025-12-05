import PyQt6.QtWidgets as widgets


class Option(widgets.QGroupBox):
	"""Groups parts of an option."""

	def build(self):
		layout = widgets.QVBoxLayout(self)
		layout.addWidget(widgets.QLineEdit())
		layout.addWidget(widgets.QTextEdit())
		layout.addWidget(widgets.QCheckBox("Hidden"))
		layout.addWidget(widgets.QCheckBox("Permanent"))

		delete = widgets.QPushButton("Delete")
		delete.clicked.connect(self.deleteLater)
		layout.addWidget(delete)
