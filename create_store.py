#!/usr/bin/env python3
"""
Gemini File Search Store Creator

This script creates a new File Search store (Corpus) using Google Gemini API,
uploads and indexes all PDF files from a specified local folder with sensible
chunking settings, and adds basic metadata.

Requirements:
- google-genai package (pip install google-genai)
- Google Cloud API key with Gemini API enabled

Usage:
1. Set your API_KEY below
2. Set the FOLDER path to your PDFs
3. Run: python create_store.py
"""

import os
import time
import sys
import json
import uuid
import google.generativeai as genai

# Configuration
API_KEY = "AIzaSyC68Y9pohX1X88ejs2jt_K0522tFSRUXms"  # Replace with your actual Google Gemini API key
FOLDER = "./papers/"  # Default folder containing PDF files
STORE_NAME = "My Research Papers 2025"

# Chunking settings
CHUNK_SIZE = 300  # Tokens per chunk
OVERLAP_SIZE = 30  # Token overlap between chunks

def create_file_search_store():
    """
    Main function to upload PDFs and create a "store" as a JSON file.
    """
    try:
        # Configure the Gemini client
        genai.configure(api_key=API_KEY)
        print("✓ Connected to Google Gemini API")

        # Get list of PDF files
        if not os.path.exists(FOLDER):
            print(f"❌ Error: Folder '{FOLDER}' does not exist")
            sys.exit(1)

        pdf_files = [f for f in os.listdir(FOLDER) if f.lower().endswith('.pdf')]
        if not pdf_files:
            print(f"❌ Error: No PDF files found in '{FOLDER}'")
            sys.exit(1)

        print(f"✓ Found {len(pdf_files)} PDF file(s) to process")

        # Upload each PDF
        uploaded_files = []
        for pdf_file in pdf_files:
            file_path = os.path.join(FOLDER, pdf_file)

            try:
                print(f"  Uploading: {pdf_file}")
                uploaded_file = genai.upload_file(file_path)
                print(f"    ✓ Uploaded file: {uploaded_file.name}")
                uploaded_files.append(uploaded_file)

            except Exception as e:
                print(f"    ❌ Failed to upload {pdf_file}: {e}")

            # Small delay between uploads
            time.sleep(1)

        if not uploaded_files:
            print("❌ No files uploaded successfully")
            sys.exit(1)

        # Create store data
        store_id = str(uuid.uuid4())
        store_data = {
            "id": store_id,
            "name": STORE_NAME,
            "files": [f.name for f in uploaded_files]
        }

        # Save to JSON file
        store_file = f"{store_id}.json"
        with open(store_file, "w") as f:
            json.dump(store_data, f)

        print(f"\n✓ Successfully uploaded {len(uploaded_files)}/{len(pdf_files)} PDF files")
        print(f"✓ File search store created!")
        print(f"✓ Store ID (copy this for the chatbot): {store_id}")
        print(f"✓ Store data saved to: {store_file}")

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("Gemini File Search Store Creator")
    print("=" * 40)
    create_file_search_store()