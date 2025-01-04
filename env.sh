#!/bin/bash

if ! command -v openssl &> /dev/null; then
    echo "Error: openssl is not installed. Please install it to proceed."
    exit 1
fi

# Generate a random API key
API_KEY=$(openssl rand -base64 32)

# Ask user for Flask environment selection
echo "Select Flask environment (default is set to 'production'):"
echo "1) development"
echo "2) production"
read -p "Enter your choice (1 or 2): " FLASK_ENV_OPTION

# Set FLASK_ENV based on the user input or default to production
case $FLASK_ENV_OPTION in
    1)
        FLASK_ENV="development"
        ;;
    2)
        FLASK_ENV="production"
        ;;
    *)
        echo "Invalid option. Setting Flask environment to production."
        FLASK_ENV="production"
        ;;
esac

# Ask user for the upload folder path
read -p "Enter the upload folder path (default: 'uploads' in the app directory): " UPLOAD_FOLDER
UPLOAD_FOLDER=${UPLOAD_FOLDER:-uploads}
if [[ $UPLOAD_FOLDER =~ [^a-zA-Z0-9/_-] ]]; then
    echo "Invalid upload folder path. Using default: 'uploads'."
    UPLOAD_FOLDER="uploads"
fi

# Ask user for the app domain
read -p "Enter the app domain (default is set to 'localhost'): " APP_DOMAIN
APP_DOMAIN=${APP_DOMAIN:-localhost}

# Create the .env file and write the variables
echo "API_KEY=$API_KEY" > .env
echo "FLASK_ENV=$FLASK_ENV" >> .env
echo "UPLOAD_FOLDER=$UPLOAD_FOLDER" >> .env
echo "APP_DOMAIN=$APP_DOMAIN" >> .env

# Print a message with the generated values
echo ".env file has been generated."
echo "Generated API_KEY: $API_KEY"
echo "FLASK_ENV: $FLASK_ENV"
echo "UPLOAD_FOLDER: $UPLOAD_FOLDER"
echo "APP_DOMAIN: $APP_DOMAIN"
