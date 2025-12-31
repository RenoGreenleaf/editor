import json
import qtpynodeeditor as ne
from qtpy import QtWidgets as widgets, QtGui as gui
from option import Option
import nodes


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
		root_layout = widgets.QHBoxLayout(root)

		registry = ne.DataModelRegistry()
		registry.register_model(nodes.Option)
		scene = nodes.Scene(registry=registry)
		flow = ne.FlowView(scene)
		flow.setAcceptDrops(True)

		root_layout.addWidget(scroller)
		root_layout.addWidget(flow)
		self.setCentralWidget(root)

		toolbar = widgets.QToolBar()
		toolbar.setMovable(False)
		self.addToolBar(toolbar)

		add = gui.QAction("Add", self)
		add.triggered.connect(self.add)
		save = gui.QAction("Save", self)
		save.triggered.connect(self.save)
		load = gui.QAction("Load", self)
		load.triggered.connect(self.load)
		toolbar.addAction(add)
		toolbar.addAction(save)
		toolbar.addAction(load)

	def add(self):
		option = Option()
		option.build()
		self.options_layout.addWidget(option)

		self.last_id += 1
		option.setObjectName(str(self.last_id))

	def save(self):
		path, _ = widgets.QFileDialog.getSaveFileName(self)

		with open(path, 'w') as world_file:
			json.dump(self.normalize(), world_file, indent=4)

	def load(self):
		path, _ = widgets.QFileDialog.getOpenFileName(self)
		options = self.findChildren((Option,))

		for option in options:
			option.deleteLater()

		with open(path, 'r') as world_file:
			self.denormalize(json.load(world_file))

	def normalize(self):
		options = self.findChildren((Option,))

		normalized = {
			option.objectName(): option.normalize()
			for option in options
		}

		return {'available': normalized}

	def denormalize(self, raw_world):
		for name, raw_option in raw_world['available'].items():
			option = Option()
			option.build()
			option.denormalize(raw_option)
			option.setObjectName(name)
			self.options_layout.addWidget(option)

		self.last_id = int(max(raw_world['available'].keys()))
