@echo off

pushd "%~dp0"

echo ========================================= > project_tree.txt
echo VITESSE CONTROL CENTER PROJECT STRUCTURE >> project_tree.txt
echo ========================================= >> project_tree.txt
echo. >> project_tree.txt

tree /F /A >> project_tree.txt

echo. >> project_tree.txt
echo ========================================= >> project_tree.txt
echo PYTHON FILES >> project_tree.txt
echo ========================================= >> project_tree.txt
echo. >> project_tree.txt

dir /S /B *.py >> project_tree.txt

popd

echo.
echo Klaar.
pause