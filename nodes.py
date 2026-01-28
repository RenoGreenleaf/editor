# Copyright (C) 2026  Reno Greenleaf
"""Node editor stuff."""
from qtpy.QtWidgets import QWidget, QLineEdit, QMessageBox, QPushButton
from qtpy.QtCore import QPointF
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
		self.node = ne.Node(self)
		registry = ne.DataModelRegistry()
		self.scene = ne.FlowScene(registry=registry)

	def setCaption(self, text):
		"""Synchronize widgets description with node caption."""
		self.caption = text
		self.graphics_object.setFocus()
		self.graphics_object.clearFocus()

	def delete(self):
		self.scene.remove_node(self.node)


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

		self._create_node(widget, event.scenePos())

	def normalize(self):
		"""Prepare for saving."""
		result = {'connections': [], 'nodes': {}}

		for connection in self._iterate_over_connections():
			result['connections'].append(self._normalize_connection(connection))

		for node in self.iterate_over_nodes():
			result['nodes'][node.model.widget.objectName()] = self._normalize_node(node)

		return result

	def denormalize(self, json, relationships):
		"""Load."""
		nodes = {}

		for identifier in json['ai']['nodes']:
			widget = relationships.get('option', identifier)
			raw_node = json['ai']['nodes'][identifier]
			position = QPointF(raw_node['x'], raw_node['y'])
			nodes[identifier] = self._create_node(widget, position)

		for connection in json['ai']['connections']:
			index = 0 if connection['action'] == 'hide' else 1
			trigger = nodes[connection['trigger']]
			affected = nodes[connection['affected']]
			self.create_connection_by_index(affected, index, trigger, 0, None)

	def _normalize_connection(self, connection):
		input_, _ = connection.ports

		return {
			'trigger': connection.output_node.model.widget.objectName(),
			'affected': connection.input_node.model.widget.objectName(),
			'action': 'show' if input_.index == 1 else 'hide',
		}

	def _normalize_node(self, node):
		position = node.graphics_object.scenePos()
		return {
			'x': position.x(),
			'y': position.y()
		}

	def _iterate_over_widgets(self):
		for node in self.iterate_over_node_data():
			yield node.widget

	def _iterate_over_connections(self):
		for node in self.iterate_over_nodes():
			for connection in node.state.output_connections:
				yield connection

	def _create_node(self, widget, position):
		node = self.create_node(Option())
		node.model.node = node
		node.model.scene = self
		node.model.widget = widget
		node.model.graphics_object = node.graphics_object

		delete = widget.findChild((QPushButton,))
		description = widget.findChild((QLineEdit,))
		description.textChanged.connect(node.model.setCaption)
		delete.clicked.connect(node.model.delete)

		node.graphics_object.setPos(position)
		node.model.setCaption(description.text())

		return node
