@echo off

set "ENV_NAME=image_tool_env"
set "PYTHON_SCRIPT=inspect_image_tool.py"

REM Activate the conda environment
echo Activating conda environment '%ENV_NAME%'...
call conda activate "%ENV_NAME%"

REM Run the Python script
echo Running '%PYTHON_SCRIPT%'...
python "%PYTHON_SCRIPT%"
