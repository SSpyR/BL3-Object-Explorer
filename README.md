# BL3 Object Explorer

Welcome to the BL3 Object Explorer, this is a program developed for ease of use to view data within Borderlands 3, namely JSON data.

This program is very simple, once you launch it it will proceed to download the necessary files to browse through from GitHub before
properly loading for the first time and update said files automatically whenever new versions of the files are uploaded to the repo.

Once the program properly starts you can enter in what you would like to search for in the text box at the top and then hit search,
it will then take a few seconds to load before displaying a list of file paths that match the search term, if any

You can then select one of the files by clicking on the file path in the results box and depending on which option you have selected
in the top right of the window (Object JSON or Object Refs), you will either see a window displaying the JSON text data of the file or 
a window displaying the files that either reference said file, or files that said file references in its data. 

Quick note: you can further select more files within the Object Refs window to view their references

You can get started by downloading the newest released exe from the [Releases Tab](https://github.com/SSpyR/BL3-Object-Explorer/releases)

# Disclaimers/Information

Utilizes Grimm's Zip File of Serialized Data which [Can be Found Here](https://www.nexusmods.com/borderlands3/mods/247)

As stated in the Source Code also utilizes apocalyptech's SQLite Database for Object References which [Can be Found Here](https://apocalyptech.com/games/bl3-refs/)

Data Excluded for Size and Convience Purposes: L10N Folders, FaceFX files, Any Leftover *.umap files, Any Leftover *.mp4 files

Currently a Windows Only Program (exe)

Will create a folder in C:\ titled BL3OE, this is to store the data to use for searching. Do not delete this folder or its contents unless you are removing the program

If you find yourself browsing this folder you will notice that one of the files is a Zip File, this is done on purpose, you do not need to unpack this file, the program specifically looks for it to be a Zip File

# Contact

If you have any sort of feedback, comments, or questions please feel free to open an Issue here on the GitHub

# Support

If you would like to support my efforts in 

BL3 Modding/BL3 Utility App Development you made do so here:

[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=E9YJB3Q2ZX72G&item_name=BL3+Modding&currency_code=USD)