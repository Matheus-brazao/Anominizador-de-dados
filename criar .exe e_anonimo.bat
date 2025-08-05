@echo off
rd /s /q build
rd /s /q dist
del /q e_anonimo.spec
pyinstaller --onefile --noconsole --icon=e_anonimo.ico --name=E-Anonimo e_anonimo.py

pause
