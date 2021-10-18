echo off


rem Requirements
rem ------------
rem - install Python 3.8 (add to system path)
rem - run the prepare_venv.bat script in the directory containing the utility script
rem
rem - Install TortoiseSVN, make sure to add commandline SVN tools
rem   * If context menu items disappear / don't appear then rerun the installer and select the 'repair' option



rem IMPORTANT INFORMATION
rem ---------------------
rem - The code to be assessed must have been checked into SVN, the wrong working copy revision will be reported if it hasn't
rem - The code to be assessed must have been build sucessfully, the wrong memory metrics will be reported if it hasn't 

rem activate the script's virtual environment so that we have access to the correct packages
call venv/Scripts/activate

python main.py

rem disable the script's virtual environment so that we are using the system settings again
call venv/Scripts/deactivate


rem uncomment to stop the commandline window from closing automatically
pause
