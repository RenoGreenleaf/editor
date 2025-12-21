import qtpynodeeditor as ne


class Data(ne.NodeData):
	data_type = ne.NodeDataType('data', 'Data')


class Option(ne.NodeDataModel):
	name = 'option'
	caption = 'Option'
	caption_visible = True
	num_ports = {
		ne.PortType.input: 2,
		ne.PortType.output: 1,
	}
	data_type = Data.data_type
