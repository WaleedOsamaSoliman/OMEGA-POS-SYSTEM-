@ECHO off 
echo %cd%
cd "../"
echo %cd%
cd scripts
call "activate.bat"
cd "../"
cd "website"
start /MIN npm run cash
start /MIN python manage.py runserver 0.0.0.0:777
exit 0