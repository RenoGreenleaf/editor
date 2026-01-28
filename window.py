# Copyright (C) 2026  Reno Greenleaf
"""Root widget."""
import json
import qtpynodeeditor as ne
from qtpy import QtWidgets as widgets, QtGui as gui
from option import Option
import nodes


class Window(widgets.QMainWindow):
	"""An app needs a main window."""

	def __init__(self):
		"""Define initial properties to be sure they're available later."""
		self.last_id = 0
		self.options_layout = widgets.QVBoxLayout()
		super().__init__()

	def build(self):
		"""Prepare base layout. Call it right after instantiation."""
		self.setFixedHeight(600)
		self.setFixedWidth(800)

		options = widgets.QWidget()
		options.setLayout(self.options_layout)

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
		"""Add option. Called via UI."""
		option = Option()
		option.build()
		self.options_layout.addWidget(option)

		self.last_id += 1
		option.setObjectName(str(self.last_id))

	def save(self):
		"""Preserve current state to a file."""
		path, _ = widgets.QFileDialog.getSaveFileName(self)

		with open(path, 'w', encoding='utf-8') as world_file:
			json.dump(self.normalize(), world_file, indent=4)

	def load(self):
		"""Restore state from a file."""
		path, _ = widgets.QFileDialog.getOpenFileName(self)
		options = self.findChildren((Option,))

		for option in options:
			option.deleteLater()

		with open(path, 'r', encoding='utf-8') as world_file:
			self.denormalize(json.load(world_file))

	def normalize(self):
		"""Prepare raw data for saving."""
		options = self.findChildren((Option,))
		normalized_options = {
			option.objectName(): option.normalize()
			for option in options
		}

		view = self.findChild((ne.FlowView,))
		return {
			'ai': view.scene.normalize(),
			'available': normalized_options,
		}

	def denormalize(self, raw_world):
		"""Fill a window from raw data."""
		for name, raw_option in raw_world['available'].items():
			option = Option()
			option.build()
			option.denormalize(raw_option)
			option.setObjectName(name)
			self.options_layout.addWidget(option)

		view = self.findChild((ne.FlowView,))
		view.scene.denormalize(raw_world, self)

		ids = map(int, raw_world['available'].keys())
		self.last_id = max(ids)

	def get(self, key, identifier):
		"""Retrieve a widget to create a node from it."""
		if key != 'option':
			raise KeyError()

		return self.findChild((Option,), identifier)

	def unid(self):
		"""Implement relationships interface."""
