# objectview.py
# Build exe via auto-py-to-exe

# Baseline of GUI and Search Engine derived from tutorial from Izzy Analytics
# Video: https://www.youtube.com/watch?v=IWDC9vcBIFQ
# Repo: https://github.com/israel-dryer/File-Search-Engine
# bl3refs.sqlite3 provided by apocalyptech

# Copyright (C) 2021-2022 Angel LaVoie
# https://github.com/SSpyR
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

#TODO Probably needs more error handling
#TODO Window resizing?
#TODO Find a way to make Enter press Search?
#TODO Reduce exe size (imports that arent needed?)
#TODO Look into whether zipping the data, or unpacking it directly from user's files is better

import os, sys
import PySimpleGUI as gui
from zipfile import ZipFile
from bl3data import BL3Data

"""
Initializing some Global Values for ease of use
Version Number: 0.1.0
"""
data=BL3Data()
results=[]
try:
	cwd=sys._MEIPASS
except AttributeError:
	cwd=os.path.dirname(__file__)
zipname=os.path.join(cwd, 'utils/objects.zip')

class BL3Object:
	"""
	Creating an Object for BL3 Objects (good naming I know)
	"""

	def __init__(self, name):
		"""
		Takes in the Object Name being searched for
		And the path its located in
		"""
		self.name=name
	
	def get_refs_to(self, name):
		"""
		Utilizes bl3data.py from apocalyptech to get all Objects
		Which reference the Object given
		"""
		name=name.replace('.json','')
		name=f'/{name}'
		return data.get_refs_to(name)

	def get_refs_from(self, name):
		"""
		Utilizes bl3data.py from apocalyptech to get all Objects
		Which the given Object references
		"""
		name=name.replace('.json','')
		name=f'/{name}'
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

		gui.change_look_and_feel('DarkGrey6')
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
	
	def jsonwindow(self, file_name):
		"""
		Window for Displaying JSON Object data
		"""
		gui.change_look_and_feel('DarkGrey6')
		layout=[
			[gui.Text(f'Showing Object JSON for {get_obj_name(file_name)}', size=(50, 1), key='jsontitle')],
			[gui.Output(size=(90, 30))]
		]

		self.window=gui.Window('Object JSON Viewer', layout=layout, finalize=True)
		print(get_json(file_name))
		self.window.read()

	def refwindow(self, file_name):
		"""
		Window for Displaying Object Ref data
		"""
		object=BL3Object(file_name)
		refs_to=object.get_refs_to(file_name)
		refs_from=object.get_refs_from(file_name)
		refs_to_text=f'Showing Objects that Reference {get_obj_name(file_name)}'
		refs_from_text=f'Showing Objects that {get_obj_name(file_name)} References'

		gui.change_look_and_feel('DarkGrey6')
		layout=[
			[gui.Text(refs_to_text, size=(100, 1), key='refstitle')],
			[gui.Listbox(values=refs_to, size=(100, 10), enable_events=True, key='resultsto')],
			[gui.Text(refs_from_text, size=(100, 1), key='refstitle2')],
			[gui.Listbox(values=refs_from, size=(100,10), enable_events=True, key='resultsfrom')]
		]

		self.window=gui.Window('Object Refs Viewer', layout=layout, finalize=True)

		while True:
			event, values=self.window.read()
			if event is None:
				break
			if event=='resultsto' or event=='resultsfrom':
				file_name=values[event]
				file_name[0]=file_name[0].replace('/','',1)
				self.window['refstitle'].update(f'Showing Objects that Reference {get_obj_name(file_name[0])}')
				self.window['resultsto'].update(values=object.get_refs_to(file_name[0]))
				self.window['refstitle2'].update(f'Showing Objects that {get_obj_name(file_name[0])} References')
				self.window['resultsfrom'].update(values=object.get_refs_from(file_name[0]))


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
		if values['term']=='':
			gui.PopupError('Please Enter a Term to Search For')
			return
		window['results'].update(values=self.results)
		window['info'].update(value='Searching for objects...')

		count=0
		with ZipFile(self.zipname, 'r') as zip:
			for info in zip.infolist():
				if values['term'].lower() in info.filename.lower() and '.' in info.filename.lower():
					self.results.append(f'{info.filename}'.replace('\\', '/'))
					window['results'].update(self.results)
					count=count+1
				if count>200:
					gui.popup('More Than 200 Matches. Showing First 200')
					break
		window['info'].update('Enter a search term and press `Search`')


def get_json(file_name):
	"""
	Function for getting JSON data of Object
	"""
	global zipname

	with ZipFile(zipname, 'r') as zip:
		with zip.open(file_name) as file:
			data=file.read()
			data=data.decode('utf-8')
			data=data.strip('\n')
			
			return data


def get_obj_name(file_name):
	"""
	Helper Function to get Object name from path
	"""
	file_name=file_name.split('/')
	obj_name=file_name[len(file_name)-1]
	obj_name=obj_name.replace('.json','')
	
	return obj_name


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
				if values['json']:
					pygui.jsonwindow(file_name[0])
				if values['refs']:
					pygui.refwindow(file_name[0])


if __name__=='__main__':
	print('Starting program')
	main()