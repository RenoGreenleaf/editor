"""Node editor stuff."""

from qtpy.QtWidgets import QWidget, QLineEdit, QToolTip, QMessageBox
import qtpynodeeditor as ne


class Boolean(ne.NodeData):
	"""Required for a node."""

	data_type = ne.NodeDataType('boolean', 'Boolean')


class Option(ne.NodeDataModel):
	"""A node corresponding to an option widget."""

	name = 'option'
	port_caption_visible = True
	port_caption = {
		'input': {0: 'Hide', 1: 'Show'},
		'output': {0: 'When selected'}
	}
	caption = 'Option'
	caption_visible = True
	num_ports = {
		ne.PortType.input: 2,
		ne.PortType.output: 1,
	}
	data_type = Boolean.data_type

	def __init__(self, *args, **kwargs):
		"""Declare custom properties."""
		super().__init__(*args, **kwargs)
		self.widget = QWidget()

	def setCaption(self, text):
		"""Synchronize widgets description with node caption."""
		self.caption = text
		self.graphics_object.setFocus()
		self.graphics_object.clearFocus()


class Scene(ne.FlowScene):
	"""Node editor itself."""

	def dragMoveEvent(self, event):
		"""Accept event. Required for a drag-drop event to work."""
		event.acceptProposedAction()

	def dropEvent(self, event):
		"""Happens when a widget is dropped on the editor."""
		widget = event.source()
		if widget in self._iterate_over_widgets():
			QMessageBox.information(widget, " ", "It's dropped already.")
			return

		# node creation
		node = self.create_node(Option())
		node.graphics_object.setPos(event.scenePos())
		node.model.graphics_object = node.graphics_object
		description = widget.findChild((QLineEdit,))
		node.model.widget = widget
		node.model.setCaption(description.text())
		description.textChanged.connect(node.model.setCaption)

	def _iterate_over_widgets(self):
		for node in self.iterate_over_node_data():
			yield node.widget
