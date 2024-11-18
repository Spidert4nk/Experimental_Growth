The original creator of this app is someone on Fiverr. I was merely tasked with fixing it and making additions as it would crash when trying to duplicate or remove cells, and Use Random Added wasn't working properly.

Also fixed a bug when using Group Times: the program would create an ever-stacking amount of popup windows, for each of the grouped values. These grouped values would persist through deletion for the purposes of creating the popups.

When saving, a homebrewed function is used to handle path names and to identify whether the OS is Linux or Windows, instead of Python-specific solutions. This function wouldn't allow any periods to exist at any point in the path and would quietly quit the saving process if that happened. I decided to modify the existing function as it would be faster than rewriting it for a program that will ever only output .txt files. Now it only checks for ".txt" in the path, as that means the user is overwriting an existing file.

Furthermore, I added the "Value by times" functionality and made sure it works properly with "Use Random Added".

Here's how to install and run the program on Windows :

Install :

1. Download the latest version of python from this page : https://www.python.org/downloads/windows/

2. Run the downloaded executable. For more help refer to this page : https://docs.python.org/3/using/windows.html#installation-steps

3. To be sure :
    1. Run this executable once again
    2. Select "modify"
    3. Be sure that "pip" is checked and Click next
    4. Be sure that "Add python to the environment variables" is checked.
    5. Click install.

3. Install PyQt5 on your system :
    1. Click on the search bar.
    2. Search for "cmd" or "command prompt".
    3. Run the program called "command prompt".
    4. A window should be open now.
    5. In this window type "pip install pyqt5" and press enter.
    6. Wait until everything is installed.

Run :

1. Go into the project folder.

2. Press 'shift' and right click inside the folder.

3. Click on 'Open PowerShell window here'.

4. Type 'python gui.py' and press enter.

5. The app should be running.
