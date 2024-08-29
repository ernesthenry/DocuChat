# Chat with Documents API

This project provides an API for conversational interactions with documents using the FastAPI framework. It supports loading documents, splitting them into manageable chunks, and generating responses to user queries using a conversational AI model.

## Features

- **Upload and Process Documents**: Supports `.docx` and `.pdf` files.
- **Conversational Retrieval Chain**: Uses OpenAI's GPT models to generate responses based on document content.
- **Session Management**: Tracks conversation history using MongoDB.
- **AWS Integration**: Downloads files from AWS S3 and processes them.
- **CORS Support**: Allows Cross-Origin Resource Sharing to enable interaction with frontend applications.

## Requirements

- Python 3.7+
- FastAPI
- MongoDB
- AWS S3
- Pydantic
- Langchain
- OpenAI API Key

## Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/ernesthenry/DocuChat.git
    cd DocuChat
    ```

2. **Install the Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

3. **Set Up Environment Variables**

    - Create a `.env` file in the root directory.
    - Add your OpenAI API key, MongoDB connection URL, and AWS S3 credentials.

    ```env
    OPENAI_API_KEY=your_openai_api_key
    MONGO_URL=your_mongo_url
    S3_KEY=your_s3_key
    S3_SECRET=your_s3_secret
    S3_BUCKET=your_s3_bucket
    S3_REGION=your_s3_region
    ```

## Usage

1. **Start the FastAPI Application**

    ```bash
    uvicorn main:app --reload
    ```

2. **Send a POST Request to the `/chat` Endpoint**

    - **Request Body:**

      ```json
      {
          "session_id": "your_session_id",
          "user_input": "Your question",
          "data_source": "path/to/your/document.pdf"
      }
      ```

    - **Response:**

      ```json
      {
          "response": {
              "answer": "Generated response from the document"
          },
          "session_id": "your_session_id"
      }
      ```

3. **Track Conversation History**

    - Conversation history is stored in MongoDB under the `chat-history` collection. Each session is identified by a unique `session_id`.

## API Endpoints

### `/chat` [POST]

- **Description**: Generates a response to the user's query based on the provided document and session history.
- **Parameters**:
  - `session_id` (optional): Unique identifier for the session.
  - `user_input`: The user's query.
  - `data_source`: The file name of the document to be used.

## Project Structure

- `main.py`: The entry point of the FastAPI application.
- `models.py`: Contains Pydantic models for request and response schemas.
- `utils.py`: Utility functions for processing documents and managing sessions.
- `requirements.txt`: Lists all the Python dependencies.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a Pull Request.

## Contact

- **Author**: Kato Ernest Henry
- **Email**: henry38ernest@gmail.com
- **GitHub**: [ernesthenry](https://github.com/ernesthenry)
