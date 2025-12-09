"""Making sure widgets are ready to be mapped to JSON data."""
from PyQt6.QtGui import QAction
from window import Window
from option import Option


def test_ids(qtbot):
	window = Window()
	window.build()
	expected_ids = ["1", "2", "3"]

	window.add()
	window.add()
	window.add()

	options = window.findChildren((Option,))
	ids = [option.objectName() for option in options]
	assert ids == expected_ids
