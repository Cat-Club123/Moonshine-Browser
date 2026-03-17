import os
import sys
from PyInstaller.__main__ import run

# Define the paths for the icon and the source script
icon_path = 'path/to/icon.ico'  # Specify your icon path here
script_path = 'path/to/your_script.py'  # Specify your main script path here

# Define the options for PyInstaller
options = [
    '--onefile',  # Bundle everything into a single executable
    '--icon=' + icon_path,  # Include the icon
    script_path  # The main entry script
]

# Add platform-specific options
if sys.platform == 'win32':
    options.append('--name=YourAppName-Windows')  # Change to your app name
elif sys.platform == 'darwin':
    options.append('--name=YourAppName-macOS')  # Change to your app name
else:
    options.append('--name=YourAppName-Linux')  # Change to your app name

# Run PyInstaller with the options specified
run(options)
