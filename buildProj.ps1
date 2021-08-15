# buildProj.ps1

$vnum = read-host "What is the version number (x.x.x)?"

rmdir -Recurse .\__pycache__ -erroraction ignore
rmdir -Recurse .\build -erroraction ignore
rmdir -Recurse .\dist -erroraction ignore
del BL3-Object-Explorer.spec -erroraction ignore

pyinstaller objectview.py --noconsole --onefile --name "BL3OE" --add-data "C:\Users\Angel LaVoie\Downloads\Coding\BL3-Object-Explorer\utils\;utils" --add-data "bl3data.py;."
cp $PSScriptRoot\dist\BL3OE.exe $PSScriptRoot\BL3OE.exe

# Open PowerShell Here, .\buildProj.ps1
# (powershell -ExecutionPolicy ByPass -File buildProj.ps1) <- this if not signed

# $configstring = @"
# ;!@Install@!UTF-8!
# Title=`"BL3 Object Explorer v$($vnum)`"
# BeginPrompt="Do you want to install BL3 Object Explorer?"
# RunProgram="setup.bat"
# InstallPath="C:\Program Files\BL3ObjectExplorer"
# MiscFlags="4"
# ;!@InstallEnd@!
# "@
# $setupstring = @'
# ICACLS "C:\Program Files\BL3ObjectExplorer" /grant Everyone:"(OI)(CI)(F)"
# '@

# echo $setupstring | out-file -encoding ascii $PSScriptRoot\dist\objectview\setup.bat

# echo $configstring | out-file -encoding ascii $PSScriptRoot\config.txt

# 7z a -r $PSScriptRoot\installer.7z $PSScriptRoot\dist\objectview\*

# cmd.exe /c copy /b 7zsd_All.sfx+config.txt+installer.7z BL3ObjectExplorerInstaller.exe

# rm installer.7z
# rm config.txt

rmdir -Recurse .\__pycache__
rmdir -Recurse .\build
rmdir -Recurse .\dist
# Get-ChildItem .\dist -Recurse | Remove-Item -Recurse -Force   #Necessary because even rmdir recurse isn't recursing
del ".\BL3OE.spec"
pause