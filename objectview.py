# objectview.py
# Build exe via auto-py-to-exe

# Baseline of GUI and Search Engine derived from tutorial from Izzy Analytics
# Video: https://www.youtube.com/watch?v=IWDC9vcBIFQ
# Repo: https://github.com/israel-dryer/File-Search-Engine
# bl3refs.sqlite3 provided by apocalyptech

# Copyright (C) 2021-2022 Angel LaVoie
# https://github.com/SSpyR
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the development team nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL ANGEL LAVOIE BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

#TODO Probably needs more error handling
#TODO Window resizing?
#TODO Find a way to make Enter press Search?
#TODO Properly do a progress bar?

import os, requests
from PySimpleGUI.PySimpleGUI import WIN_CLOSED
import PySimpleGUI as gui
from zipfile import ZipFile
from bl3data import BL3Data
"""
Initializing some Global Values for ease of use
Version Number: 0.2.0
"""
data=BL3Data()
results=[]
data_path='C:\BL3OE'
zipname=os.path.join(data_path, 'objects.zip')
sqlname=os.path.join(data_path, 'bl3refs.sqlite3')

class BL3Object:
	"""
	Creating an Object for BL3 Objects (good naming I know)
	"""

	def __init__(self, name, sql_path):
		"""
		Takes in the Object Name being searched for
		And the path its located in
		"""
		self.name=name
		self.sql_path=sql_path
	
	def get_refs_to(self, name, sql_path):
		"""
		Utilizes bl3data.py from apocalyptech to get all Objects
		Which reference the Object given
		"""
		name=name.replace('.json','')
		name=f'/{name}'
		return data.get_refs_to(name, sql_path)

	def get_refs_from(self, name, sql_path):
		"""
		Utilizes bl3data.py from apocalyptech to get all Objects
		Which the given Object references
		"""
		name=name.replace('.json','')
		name=f'/{name}'
		return data.get_refs_from(name, sql_path)


class PyGui:
	"""
	Creating a GUI Object
	"""
	def __init__(self):
		"""
		Base Init
		"""

	def searchwindow(self):
		"""
		Creating the Main Search GUI
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

		search=FileSearch().search
		pygui=PyGui()

		while True:
			event, values=self.window.read()
			if event is None:
				break
			if event=='search':
				search(values, self.window)
			if event=='results':
				file_name=values['results']
				if file_name:
					if values['json']:
						pygui.jsonwindow(file_name[0])
					if values['refs']:
						pygui.refwindow(file_name[0])
	
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
		global sqlname

		object=BL3Object(file_name, sqlname)
		refs_to=object.get_refs_to(file_name, sqlname)
		refs_from=object.get_refs_from(file_name, sqlname)
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
				self.window['resultsto'].update(values=object.get_refs_to(file_name[0], sqlname))
				self.window['refstitle2'].update(f'Showing Objects that {get_obj_name(file_name[0])} References')
				self.window['resultsfrom'].update(values=object.get_refs_from(file_name[0], sqlname))

	def downloadwindow(self):
		"""
		Window for Displaying the downloading progress of backend data
		"""
		gui.change_look_and_feel('DarkGrey6')
		layout=[
			[gui.Text('Downloading/Updating Object Data...', size=(35, 1), key='dwnldtext')],
			#[gui.ProgressBar(max_value=100, size=(50, 10), key='dwnldbar', metadata=5)]
		]

		self.window=gui.Window('Object Data Retrieval', layout=layout, finalize=True)
		#self.window['dwnldbar'].Widget.config(mode='indeterminate')
		#progress_value=0

		data_check=get_object_data(self.window)
		#while True:
			#progress_value+=self.window['dwnldbar'].metadata
			#self.window['dwnldbar'].update(current_count=progress_value)
			

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


def get_object_data(window):
	"""
	Function for acquiring bundled data from GitHub repo
	"""
	global data_path

	if not os.path.exists(zipname):
		zipurl='https://github.com/SSpyR/BL3-Object-Explorer/blob/main/utils/objects.zip?raw=true'
		zr=requests.get(zipurl, allow_redirects=True)
		open(os.path.join(data_path, 'objects.zip'), 'wb').write(zr.content)

	if not os.path.exists(sqlname):
		sqlurl='https://github.com/SSpyR/BL3-Object-Explorer/blob/main/utils/bl3refs.sqlite3?raw=true'
		sr=requests.get(sqlurl, allow_redirects=True)
		open(os.path.join(data_path, 'bl3refs.sqlite3'), 'wb').write(sr.content)

	window.close()
	return True


def data_validity_check():
	"""
	Function to check whether we need to acquire new object data
	"""
	global data_path

	pygui=PyGui()

	if not os.path.exists(data_path):
		os.mkdir(data_path)

	url='https://raw.githubusercontent.com/SSpyR/BL3-Object-Explorer/main/data_ver.txt'
	data_ver_path=os.path.join(data_path, 'data_ver.txt')

	if not os.path.exists(data_ver_path):
		r=requests.get(url)
		open(data_ver_path, 'wb').write(r.content)
		pygui.downloadwindow()
		return True
	if os.path.exists(data_ver_path):
		r=requests.get(url)
		with open(data_ver_path, 'r') as foo:
			if foo.read() in r.content.__str__():
				print('Version up to date')
				if not os.path.exists(zipname) or not os.path.exists(sqlname):
					pygui.downloadwindow()
				pass
			else:
				print('Version not up to date')
				open(data_ver_path, 'wb').write(r.content)
				pygui.downloadwindow()

	return True


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
	data_checked=data_validity_check()

	if data_checked==True:
		pygui=PyGui()
		pygui.searchwindow()


if __name__=='__main__':
	print('Starting program')
	main()