from qtpy import QtWidgets as widgets, QtCore as core, QtGui as gui


class Option(widgets.QGroupBox):
	"""Groups parts of an option."""

	def build(self):
		layout = widgets.QVBoxLayout(self)

		fields = {
			'description': widgets.QLineEdit(),
			'message': widgets.QTextEdit(),
			'hidden': widgets.QCheckBox("Hidden"),
			'permanent': widgets.QCheckBox("Permanent"),
		}

		for name, field in fields.items():
			field.setObjectName(name)
			layout.addWidget(field)

		delete = widgets.QPushButton("Delete")
		delete.clicked.connect(self.deleteLater)
		layout.addWidget(delete)

	def mouseMoveEvent(self, event):
		if event.buttons() == core.Qt.LeftButton:
			pixmap = self.grab()
			drag = gui.QDrag(self)
			mime = core.QMimeData()
			drag.setMimeData(mime)
			drag.setPixmap(pixmap)
			drag.setHotSpot(event.pos())
			drag.exec()

	def normalize(self):
		return {
			'description': self.findChild(widgets.QLineEdit, 'description').text(),
			'message': self.findChild(widgets.QTextEdit, 'message').toPlainText(),
			'hidden': self.findChild(widgets.QCheckBox, 'hidden').isChecked(),
			'permanent': self.findChild(widgets.QCheckBox, 'permanent').isChecked(),
		}

	def denormalize(self, raw):
		self._get('description').setText(raw['description'])
		self._get('message').setPlainText(raw['message'])
		self._get('permanent').setChecked(raw['permanent'])
		self._get('hidden').setChecked(raw['hidden'])

	def _get(self, name):
		return self.findChild((widgets.QWidget,), name)
