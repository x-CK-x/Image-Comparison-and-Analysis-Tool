@echo off

set "ENV_NAME=image_tool_env"
set "YML_FILE=environment.yml"

REM Function to list packages in the environment
:ListPackages
echo Installed packages in environment '%ENV_NAME%':
conda list -n %ENV_NAME%
goto :EOF

REM Check if the environment exists
for /f "tokens=1" %%i in ('conda env list ^| findstr /R "^%ENV_NAME%[ ]"') do (
    if "%%i"=="%ENV_NAME%" (
        echo Environment '%ENV_NAME%' already exists. Updating dependencies...
        conda env update -n %ENV_NAME% -f %YML_FILE% --prune
        echo Environment '%ENV_NAME%' has been updated.
        call :ListPackages
        goto :EOF
    )
)

echo Creating environment '%ENV_NAME%'...
conda env create -f %YML_FILE%
echo Environment '%ENV_NAME%' has been created.
call :ListPackages
