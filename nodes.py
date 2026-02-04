# Copyright (C) 2026  Reno Greenleaf
"""Node editor stuff."""
from qtpy.QtWidgets import QWidget, QLineEdit, QMessageBox, QPushButton
from qtpy.QtCore import QPointF
import qtpynodeeditor as ne


class Boolean(ne.NodeData):
	"""Required for a nodes ports."""

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

	def get_id(self):
		return self.widget.objectName()

	def bind(self, widget):
		self.widget = widget
		delete = widget.findChild((QPushButton,))
		description = widget.findChild((QLineEdit,))
		description.textChanged.connect(self.setCaption)
		delete.clicked.connect(self.delete)

		self.setCaption(description.text())


class Conjunction(ne.NodeDataModel):

	def __init__(self, *args, **kwargs):
		"""Declare custom properties."""
		super().__init__(*args, **kwargs)
		self.widget = QWidget()

	name = 'conjunction'
	port_caption_visible = True
	port_caption = {
		'input': {0: 'a', 1: 'b'},
		'output': {0: '&'}
	}
	num_ports = {
		ne.PortType.input: 2,
		ne.PortType.output: 1,
	}
	data_type = Boolean.data_type
	caption_visible = False

	def get_id(self):
		return self.objectName()

	def bind(self, widget):
		pass


class Scene(ne.FlowScene):
	"""The editor itself."""

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.node_created.connect(self._node_created)

	def dragMoveEvent(self, event):
		"""Accept event. Required for a drag-drop event to work."""
		event.acceptProposedAction()

	def dropEvent(self, event):
		"""Happens when a widget is dropped on the editor."""
		widget = event.source()

		if widget in self._iterate_over_widgets():
			QMessageBox.information(widget, " ", "It's dropped already.")
			return

		node = self.create_node(Option)
		node.model.bind(widget)
		node.graphics_object.setPos(event.scenePos())

	def normalize(self):
		"""Prepare for saving."""
		result = {'connections': [], 'nodes': {}}

		for connection in self._iterate_over_connections():
			result['connections'].append(self._normalize_connection(connection))

		for node in self.iterate_over_nodes():
			result['nodes'][node.model.get_id()] = self._normalize_node(node)

		return result

	def denormalize(self, json, relationships):
		"""Load."""
		nodes = {}

		for identifier in json['ai']['nodes']:
			widget = relationships.get('option', identifier)
			raw_node = json['ai']['nodes'][identifier]
			position = QPointF(raw_node['x'], raw_node['y'])
			model = self.registry.create(raw_node['type'])
			node = self.create_node(model)
			node.graphics_object.setPos(position)
			node.model.bind(widget)
			nodes[identifier] = node

		for connection in json['ai']['connections']:
			index = connection['input']
			trigger = nodes[connection['trigger']]
			affected = nodes[connection['affected']]
			self.create_connection_by_index(affected, index, trigger, 0, None)

	def _normalize_connection(self, connection):
		input_, _ = connection.ports

		return {
			'trigger': connection.output_node.model.get_id(),
			'affected': connection.input_node.model.get_id(),
			'input': input_.index,
		}

	def _normalize_node(self, node):
		position = node.graphics_object.scenePos()
		return {
			'type': node.model.name,
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

	def _node_created(self, node):
		node.model.node = node
		node.model.scene = self
		node.model.graphics_object = node.graphics_object
		node.model.setObjectName(node.id)
