authentication_url = 'http://localhost:1721/serversync_auth'
bash_script_content_for_container= '''#!/bin/bash

# Variables
REPO_DIR="/path/to/your/repo"  # Path to your Git repository
CONTAINER_NAME="your_container_name"  # Name of your Docker container

# Navigate to the repository directory
cd "$REPO_DIR" || { echo "Failed to change directory to $REPO_DIR"; exit 1; }

# Perform git pull
echo "Pulling the latest changes from the repository..."
git pull origin main  # Change 'main' to your branch if different

# Check if git pull was successful
if [ $? -ne 0 ]; then
    echo "Failed to pull the latest changes from the repository."
    exit 1
fi

# Restart the Docker container
echo "Restarting the Docker container..."
docker restart "$CONTAINER_NAME"

# Check if docker restart was successful
if [ $? -ne 0 ]; then
    echo "Failed to restart the Docker container."
    exit 1
fi

echo "Git pull and Docker container restart completed successfully."
'''


batch_script_content_for_container= '''@echo off
REM Variables
set REPO_DIR=C:\\path\\to\\your\\repo  REM Path to your Git repository
set CONTAINER_NAME=your_container_name  REM Name of your Docker container

REM Navigate to the repository directory
cd %REPO_DIR% || (echo Failed to change directory to %REPO_DIR% & exit /b 1)

REM Perform git pull
echo Pulling the latest changes from the repository...
git pull origin main  REM Change 'main' to your branch if different

REM Check if git pull was successful
if %ERRORLEVEL% neq 0 (
    echo Failed to pull the latest changes from the repository.
    exit /b 1
)

REM Restart the Docker container
echo Restarting the Docker container...
docker restart %CONTAINER_NAME%

REM Check if docker restart was successful
if %ERRORLEVEL% neq 0 (
    echo Failed to restart the Docker container.
    exit /b 1
)

echo Git pull and Docker container restart completed successfully.
'''


bash_script_content_for_service = '''#!/bin/bash

# Variables
REPO_DIR="/path/to/your/repo"  # Path to your Git repository
SERVICE_NAME="your_service_name"  # Name of the service to restart

# Navigate to the repository directory
cd "$REPO_DIR" || { echo "Failed to change directory to $REPO_DIR"; exit 1; }

# Perform git pull
echo "Pulling the latest changes from the repository..."
git pull origin main  # Change 'main' to your branch if different

# Check if git pull was successful
if [ $? -ne 0 ]; then
    echo "Failed to pull the latest changes from the repository."
    exit 1
fi

# Restart the system service
echo "Restarting the service..."
sudo systemctl restart "$SERVICE_NAME"

# Check if service restart was successful
if [ $? -ne 0 ]; then
    echo "Failed to restart the service."
    exit 1
fi

echo "Git pull and service restart completed successfully."
'''


batch_script_content_for_service = '''@echo off
REM Variables
set REPO_DIR=C:\\path\\to\\your\\repo  REM Path to your Git repository
set SERVICE_NAME=your_service_name  REM Name of your service to restart

REM Navigate to the repository directory
cd /d %REPO_DIR% || (echo Failed to change directory to %REPO_DIR% & exit /b 1)

REM Perform git pull
echo Pulling the latest changes from the repository...
git pull origin main  REM Change 'main' to your branch if different

REM Check if git pull was successful
if %ERRORLEVEL% neq 0 (
    echo Failed to pull the latest changes from the repository.
    exit /b 1
)

REM Restart the service
echo Restarting the service...
net stop %SERVICE_NAME%
if %ERRORLEVEL% neq 0 (
    echo Failed to stop the service %SERVICE_NAME%.
    exit /b 1
)

net start %SERVICE_NAME%
if %ERRORLEVEL% neq 0 (
    echo Failed to start the service %SERVICE_NAME%.
    exit /b 1
)

echo Git pull and service restart completed successfully.
'''
