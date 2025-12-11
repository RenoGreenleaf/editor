"""Making sure widgets are ready to be mapped to JSON data."""
import tempfile
import os
from PyQt6.QtWidgets import QFileDialog
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


def test_saving(qtbot, monkeypatch, tmp_path):
	path = tmp_path / 'empty.json'

	def mock_save_dialog(*args, **kwargs):
		return (path, 'JSON files (*.json)')

	monkeypatch.setattr(QFileDialog, 'getSaveFileName', mock_save_dialog)
	window = Window()
	window.build()

	window.save()

	assert os.path.isfile(path)
