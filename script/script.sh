#!/bin/bash

# Store the password in a variable (not recommended for production)
PASSWORD='12345'

# Use the password with sudo to run the command
echo "$PASSWORD" | sudo -S docker restart 17bbfcd07c42






