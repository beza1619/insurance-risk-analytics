@echo off
REM DVC wrapper for Windows
REM This uses the Python that has DVC installed

REM Try different Python paths
IF EXIST "C:\Users\b\AppData\Local\Python\pythoncore-3.14-64\python.exe" (
    SET PYTHON_PATH=C:\Users\b\AppData\Local\Python\pythoncore-3.14-64\python.exe
) ELSE IF EXIST "C:\Python314\python.exe" (
    SET PYTHON_PATH=C:\Python314\python.exe
) ELSE (
    SET PYTHON_PATH=python
)

REM Run DVC command
"%PYTHON_PATH%" -m dvc %*
