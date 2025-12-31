import qtpynodeeditor as ne


class Boolean(ne.NodeData):
	data_type = ne.NodeDataType('boolean', 'Boolean')


class Option(ne.NodeDataModel):
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


class Scene(ne.FlowScene):
	"""Things can be dropped here."""

	def dragMoveEvent(self, event):
		event.acceptProposedAction()

	def dropEvent(self, event):
		node = self.create_node(Option)
		node.graphics_object.setPos(event.scenePos())
