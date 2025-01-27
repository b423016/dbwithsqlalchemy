from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import os
from typing import List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def setup_cors(app: FastAPI):
    """
    Configures and applies CORS middleware to the FastAPI application.

    Args:
        app (FastAPI): The FastAPI application instance.
    """
    # Retrieve allowed origins from environment variables or set defaults
    origins: List[str] = os.getenv("ALLOWED_ORIGINS", "http://localhost").split(",")

    # Log the configured origins for debugging purposes
    print(f"Allowed CORS Origins: {origins}")

    # Add CORS middleware to the FastAPI application
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,               # Allows specific origins
        allow_credentials=True,              # Allows cookies and authentication headers
        allow_methods=["*"],                 # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
        allow_headers=["*"],                 # Allows all HTTP headers
    )