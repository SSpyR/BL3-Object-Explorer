# objectview.py
# GUI and Search Engine derived from tutorial from Izzy Analytics
# Video: https://www.youtube.com/watch?v=IWDC9vcBIFQ
# Repo: https://github.com/israel-dryer/File-Search-Engine

import os, json
import PySimpleGUI as gui
from zipfile import ZipFile
from bl3data import BL3Data

data=BL3Data()
results=[]
cwd=os.path.dirname(__file__)
zipname=os.path.join(cwd, 'utils/objects.zip')
zipname=zipname.replace('\\', '/')

class BL3Object:
	"""
	Creating an Object for BL3 Objects (good naming I know)
	"""

	def __init__(self, name, path):
		"""
		Takes in the Object Name being searched for
		And the path its located in
		"""
		self.name=name
		self.path=path
	
	def get_refs_to(self, name):
		"""
		Utilizes bl3data.py from apocalyptech to get all Objects
		Which reference the Object given
		"""
		return data.get_refs_to(name)

	def get_refs_from(self, name):
		"""
		Utilizes bl3data.py from apocalyptech to get all Objects
		Which the Object given references
		"""
		return data.get_refs_from(name)


class PyGui:
	"""
	Creating a GUI Object
	"""

	def __init__(self):
		"""
		Creating the GUI itself
		"""
		global results

		gui.change_look_and_feel('Black')
		layout=[
			[gui.Text('Search Term', size=(11, 1)), gui.Input('', size=(40, 1), key='term'),
			gui.Radio('Object JSON', group_id='view_type', size=(10, 1), default=True, key='json'),
			gui.Radio('Object Refs', group_id='view_type', size=(10, 1), key='refs')],
			[gui.Button('Search', size=(10, 1), key='search')],
			[gui.Text('Enter an object name and press `Search`', key='info')],
			[gui.Listbox(values=results, size=(100, 28), enable_events=True, key='results')]
		]

		self.window=gui.Window('BL3 Object Explorer', layout=layout, finalize=True, return_keyboard_events=True)
		self.window['results'].expand(expand_x=True, expand_y=True)	


class FileSearch:
	"""
	Creating File Search Object
	"""

	def __init__(self):
		"""
		Initializing here for formality
		"""
		global results, zipname
		self.results=results
		self.zipname=zipname
		
	def search(self, values, window):
		"""
		Function to search through the serialized objects
		"""
		self.results.clear()
		window['results'].update(values=self.results)
		window['info'].update(value='Searching for objects...')

		with ZipFile(self.zipname, 'r') as zip:
			for info in zip.infolist():
				if values['term'].lower() in info.filename.lower() and '.' in info.filename.lower():
					self.results.append(f'{info.filename}'.replace('\\', '/'))
					window['results'].update(self.results)
		window['info'].update('Enter a search term and press `Search`')


#TODO Actually write this
def open_file(file_name):
	"""
	Function for Opening JSON Viewer of Object
	"""
	global zipname

	with ZipFile(zipname, 'r') as zip:
		with zip.open(file_name) as file:
			print(file.read())


#TODO Actually write this
def get_refs(file_name):
	"""
	Function for getting References of Object
	"""
	pass


def main():
	"""
	Function to start the whole thing
	"""
	pygui=PyGui()
	window=pygui.window

	search=FileSearch().search

	while True:
		event, values=window.read()
		if event is None:
			break
		if event=='search':
			search(values, window)
		if event=='results':
			file_name=values['results']
			if file_name:
				open_file(file_name[0])


if __name__=='__main__':
	print('Starting program')
	main()





