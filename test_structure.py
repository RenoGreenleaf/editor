"""Making sure widgets are ready to be mapped to JSON data."""
import tempfile
import os
from PyQt6 import QtWidgets as widgets
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

	monkeypatch.setattr(
		widgets.QFileDialog,
		'getSaveFileName',
		mock_save_dialog
	)
	window = Window()
	window.build()

	window.save()

	assert os.path.isfile(path)


def test_normalization(qtbot):
	expected_option = {
		'description': "Test description.",
		'message': "Test message.",
		'permanent': False,
		'hidden': False
	}
	expected_structure = {
		'available': {
			'1': expected_option
		}
	}
	window = Window()
	window.build()
	window.add()
	option = window.findChild((Option,))
	option.findChild((widgets.QLineEdit,)).setText("Test description.")
	option.findChild((widgets.QTextEdit,)).setText("Test message.")

	result = window.normalize()

	assert result == expected_structure


def test_denormalization(qtbot):
	normalized_option = {
		'description': "Test description.",
		'message': "Test message.",
		'permanent': True,
		'hidden': True
	}
	normalized_structure = {
		'available': {
			'1': normalized_option
		}
	}
	window = Window()
	window.build()

	window.denormalize(normalized_structure)

	option = window.findChild((Option,))
	description = option.findChild((widgets.QLineEdit,), 'description').text()
	message = option.findChild((widgets.QTextEdit,), 'message').toPlainText()
	permanent = option.findChild((widgets.QCheckBox,), 'permanent').isChecked()
	hidden = option.findChild((widgets.QCheckBox,), 'hidden').isChecked()
	assert description == "Test description."
	assert message == "Test message."
	assert permanent
	assert hidden
	assert option.objectName() == '1'
