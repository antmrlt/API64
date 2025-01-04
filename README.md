# API64

This is a Flask-based API for securely uploading files in Base64 format and serving them via HTTP. It validates requests using an API key, dynamically determines file extensions based on MIME types, and saves files with read-only permissions. The app is easy to configure using environment variables and supports Dockerized deployment for seamless integration into any environment.

### Features
- File upload : Accepts files in Base64 format and saves them with appropriate extensions based on MIME types.
- Secure access: Validates API requests using an API key.
- File serving: Provides access to uploaded files via HTTP.
- Environment configuration: Allows dynamic setup of Flask environment, API key, and upload directory via .env file.
- Dockerized deployment: Simplified containerized setup for running the API.

## Installation and setup

### Prerequiseites
- Docker and docker compose

### Setup 

1. Clone the repository
```
git clone https://github.com/antmrlt/API64
cd API64
```

2. Generate `.env` file
```
chmod +x env.sh
./env.sh
```

1. Run
```
docker compose up
```

## Environment Variables

The application uses the following environment variables, configurable via `.env`:

| Variable      | Description                                      | Default Value |
|---------------|--------------------------------------------------|---------------|
| `API_KEY`     | API key for request validation                   | Randomly generated |
| `FLASK_ENV`   | Flask environment (`development` or `production`) | `production`   |
| `UPLOAD_FOLDER` | Directory for saving uploaded files             | `uploads`      |
| `APP_DOMAIN`  | Domain of the app                                | `localhost`     |

## API Endpoints

1. Upload File
- URL: /upload
- Method: POST
- Headers:
    - API-Key: Your API key

Payload:
```json
{
  "base64_string": "Base64EncodedFileContent",
  "content_type": "MIMETypeOfTheFile"
}
```

Response:
- 200 OK:
```json
{
  "message": "File saved as file_name.extension",
  "file_url": "http://file.get.api:5000/uploads/file_name.extension"
}
```
- 400 Bad Request: Missing or invalid data
- 403 Forbidden: Invalid API key
- 500 Internal Server Error: File saving issues

## Security

- **API Key Validation**: Ensures that only authorized users can upload files.
- **Read-Only Files**: Uploaded files are saved with restricted permissions (`444`).

## Notes

- Ensure the `UPLOAD_FOLDER` is writable by the application.
- For production, use a secure and unique API key.
- The default Flask environment is set to `production`. Use `development` for debugging purposes.
