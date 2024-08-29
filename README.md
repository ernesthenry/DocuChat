# Chat with Documents

This project provides an application that allows users to upload documents and interact with the content via a chat interface. It includes a frontend built with Streamlit and a backend built with FastAPI. Users can upload PDF or DOCX files and ask questions about the content, with responses generated by a conversational AI model.

## Problem Statement

In many professional and academic settings, users often need to extract and interact with specific information from lengthy documents. Manual searching and reading through documents can be time-consuming and inefficient. The challenge is to develop an application that simplifies document interaction by enabling users to upload documents and engage in a conversational manner to retrieve relevant information.

## Action

To address this problem, we developed the **Chat with Documents** application with the following steps:

1. **Frontend Development**: We used Streamlit to create an intuitive user interface that allows users to upload PDF and DOCX files and interact with them via a chat interface.
2. **Backend Development**: We built a FastAPI backend to handle file uploads, process user queries, and integrate with AWS S3 for file storage. The backend also utilizes a conversational AI model to generate responses based on document content.
3. **Integration**: Implemented session management to maintain context throughout the chat and integrated AWS S3 for efficient file handling and storage.

## Result

The **Chat with Documents** application effectively enables users to upload documents and interact with them through a conversational interface. Users can easily upload their files, ask questions about the content, and receive contextually relevant responses generated by the AI model. This solution streamlines the process of extracting information from documents, making it more efficient and user-friendly.

## Features

- **File Upload**: Supports uploading PDF and DOCX files.
- **Interactive Chat**: Ask questions about the uploaded document and receive responses based on the document content.
- **Session Management**: Maintains chat sessions to keep context.
- **AWS S3 Integration**: Handles file uploads and downloads from AWS S3.

## Technologies Used

- **Frontend**: Streamlit for the user interface.
- **Backend**: FastAPI for handling API requests and processing.
- **Python Libraries**: `requests`, `streamlit`, `fastapi`, `uvicorn`, `pydantic`, `python-dotenv`
- **AWS**: For file storage and retrieval.

## Installation

### Backend

1. **Clone the Repository**

    ```bash
    git clone https://github.com/ernesthenry/DocuChat.git
    cd DocuChat
    ```

2. **Install Backend Dependencies**

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

4. **Run the Backend Server**

    ```bash
    uvicorn main:app --reload
    ```

### Frontend

1. **Install Frontend Dependencies**

    ```bash
    pip install requests streamlit
    ```

2. **Set Backend URL**

    - Update the `BACKEND_URL` variable in `app.py` with the URL of your FastAPI backend server.

3. **Run the Frontend Application**

    ```bash
    streamlit run app.py
    ```

## Usage

1. **Upload a File**

    - On the Streamlit interface, click the "Input file" button to upload a PDF or DOCX file. The file will be uploaded to the backend server.

2. **Chat with the Document**

    - Once the file is uploaded, type questions related to the document in the chat input box. The application will respond based on the document's content.

## API Endpoints

### Backend `/chat` [POST]

- **Description**: Generates a response to the user's query based on the provided document and session history.
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

## Project Structure

- **Backend**
  - `main.py`: The entry point of the FastAPI application, including routes and logic.
  - `requirements.txt`: Lists all the Python dependencies for the backend.

- **Frontend**
  - `app.py`: Streamlit application for file uploading and chat interface.

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
