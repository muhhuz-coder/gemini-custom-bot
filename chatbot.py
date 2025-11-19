#!/usr/bin/env python3
"""
Gemini Research Papers Chatbot

Interactive chatbot that uses a pre-created File Search store (Corpus) to answer
questions about research papers with automatic citations.

Requirements:
- google-genai package (pip install google-genai)
- Google Cloud API key with Gemini API enabled
- A created File Search store ID from create_store.py

Usage:
1. Set your API_KEY below
2. Set the STORE_ID to the ID printed by create_store.py
3. Run: python chatbot.py
4. Ask questions, type 'quit' to exit
"""

import sys
import json
import google.generativeai as genai

# Configuration
API_KEY = "AIzaSyC68Y9pohX1X88ejs2jt_K0522tFSRUXms"  # Replace with your actual Google Gemini API key
STORE_ID = "f9abee98-c29b-4cc2-bf22-aa008d32271d"  # Replace with the Store ID from create_store.py output

# Model settings (Gemini 1.5 Flash for speed/cost, easily switchable to Pro)
MODEL_NAME = "gemini-1.5-flash"  # Change to "gemini-1.5-pro" for higher quality if needed

def extract_citations(response):
    """
    Extract and format citations from the response.
    Returns a formatted string with source information.
    """
    citations = []
    if hasattr(response, 'candidates') and response.candidates:
        candidate = response.candidates[0]
        if hasattr(candidate, 'grounding_attributions'):
            for attr in candidate.grounding_attributions:
                if hasattr(attr, 'title') and attr.title:
                    citations.append(attr.title)
                elif hasattr(attr, 'uri') and attr.uri:
                    # Extract filename from URI
                    source = attr.uri.split('/')[-1]
                    citations.append(source)

    if citations:
        unique_sources = list(set(citations))  # Remove duplicates
        return f"\n📚 Sources: {', '.join(unique_sources)}"
    return ""

def run_chatbot():
    """
    Main function to run the interactive chatbot.
    """
    try:
        # Configure the Gemini client
        genai.configure(api_key=API_KEY)
        print("✓ Connected to Google Gemini API")

        # Load the store data
        store_file = f"{STORE_ID}.json"
        try:
            with open(store_file, "r") as f:
                store_data = json.load(f)
            print(f"✓ Loaded file search store: {store_data.get('name', 'Unknown')}")
            print(f"  Store ID: {store_data['id']}")
        except FileNotFoundError:
            print(f"❌ Store file '{store_file}' not found. Run create_store.py first.")
            sys.exit(1)

        # Get the uploaded files
        file_names = store_data["files"]
        files = []
        for name in file_names:
            try:
                file_obj = genai.get_file(name)
                files.append(file_obj)
            except Exception as e:
                print(f"⚠ Warning: Could not load file {name}: {e}")

        if not files:
            print("❌ No files available in the store")
            sys.exit(1)

        print(f"✓ Loaded {len(files)} document(s)")

        # Create the model with fallback (prioritizing free models)
        model_names = ["gemini-2.5-flash", "gemini-2.0-flash-001", "gemini-flash-latest", "gemini-2.0-flash"]
        model = None
        
        for model_name in model_names:
            try:
                model = genai.GenerativeModel(model_name)
                # Test if model works by trying to get model info
                _ = model.model_name
                print(f"✓ Using model: {model_name}")
                break
            except Exception:
                continue
        
        if model is None:
            # List available models
            try:
                available_models = genai.list_models()
                available_names = [m.name for m in available_models if 'generateContent' in m.supported_generation_methods]
                print(f"❌ No suitable model found. Available models: {', '.join(available_names)}")
                sys.exit(1)
            except Exception as list_error:
                print(f"❌ No suitable model found. List models error: {str(list_error)}")
                sys.exit(1)

        print("🤔 Initializing with documents...")
        # No initialization needed, files will be included in each query
        print("✓ Ready to answer questions")

        print("\n" + "=" * 50)
        print("🤖 Research Papers Chatbot Ready!")
        print("Ask questions about your papers. Type 'quit' to exit.")
        print("=" * 50)

        # Conversation history
        history = []

        # Interactive chat loop
        while True:
            try:
                # Get user input
                user_input = input("\n❓ Your question: ").strip()

                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break

                if not user_input:
                    continue

                # Build the prompt with history
                system_prompt = "You are a helpful Q&A assistant for research papers. Answer questions based on the provided documents. Include citations to specific sources when possible."
                if history:
                    context = "\n".join(history[-4:])  # Keep last 4 messages for context
                    full_prompt = f"{system_prompt}\n\nPrevious conversation:\n{context}\n\nCurrent question: {user_input}"
                else:
                    full_prompt = f"{system_prompt}\n\nQuestion: {user_input}"

                # Generate response with files
                print("🤔 Thinking...")
                response = model.generate_content([full_prompt] + files)

                # Display the answer
                if response.text:
                    print(f"\n🤖 Answer: {response.text}")
                    # Add citations if available
                    citations = extract_citations(response)
                    if citations:
                        print(citations)
                    
                    # Update history
                    history.append(f"User: {user_input}")
                    history.append(f"Assistant: {response.text}")
                else:
                    print("\n🤖 Sorry, I couldn't generate a response.")

            except Exception as e:
                print(f"❌ Error: {e}")

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("Gemini Research Papers Chatbot")
    print("=" * 40)
    run_chatbot()