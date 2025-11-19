# Gemini Research Papers Chatbot

A Python-based chatbot that uses Google Gemini AI to answer questions about research papers. Upload PDF documents, create a searchable knowledge base, and interact with an AI assistant that provides accurate answers with citations.

## Features

- 📄 **PDF Upload & Indexing**: Automatically upload and index PDF research papers
- 🤖 **AI-Powered Q&A**: Interactive chatbot using Google Gemini Pro
- � **Conversation History**: Maintains context across multiple questions
- 🎨 **Web Interface**: Modern Streamlit-based UI for easy interaction
- �📚 **Automatic Citations**: Answers include source references from your documents
- 🔄 **Easy Model Switching**: Switch between different Gemini models
- 🛡️ **Rate Limiting**: Built-in handling for API rate limits
- 🌐 **Cross-Platform**: Works on Windows, Mac, and Linux

## Prerequisites

- Python 3.8 or higher
- Google Gemini API key (from [Google AI Studio](https://aistudio.google.com/))

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/gemini-research-chatbot.git
   cd gemini-research-chatbot
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Get your Google Gemini API key:**
   - Visit [Google AI Studio](https://aistudio.google.com/)
   - Create a new API key
   - Copy the API key

## Usage

### Option 1: Web Interface (Recommended)

The easiest way to use the chatbot is through the modern web interface:

1. **Run the Streamlit app:**
   ```bash
   streamlit run app.py
   ```

2. **Open your browser** to the URL shown (usually http://localhost:8501)

3. **Configure your API key** in the sidebar

4. **Upload PDF files** or load an existing document store

5. **Start chatting!** Ask questions in the chat interface

**Web UI Features:**
- 🎨 Modern, intuitive interface
- 📤 Drag & drop PDF upload
- 💬 Real-time chat with conversation history
- 📊 Document store management
- 📚 Automatic citation display
- 🔄 Easy switching between document collections

### Option 2: Command Line Interface

For advanced users or automation:

#### Step 1: Prepare Your Documents

1. Create a `papers/` folder in the project directory
2. Place all your PDF research papers in the `papers/` folder

### Step 2: Configure API Key

Edit both `create_store.py` and `chatbot.py` and replace:
```python
API_KEY = "your_api_key_here"
```
with your actual Google Gemini API key:
```python
API_KEY = "AIzaSy...your_actual_key..."
```

### Step 3: Create the Document Store

Run the store creation script:
```bash
python create_store.py
```

This will:
- Upload all PDFs from the `papers/` folder
- Create a searchable knowledge base
- Generate a unique Store ID
- Save store metadata to a JSON file

**Example output:**
```
Gemini File Search Store Creator
========================================
✓ Connected to Google Gemini API
✓ Found 2 PDF file(s) to process
✓ Uploaded file: files/abc123
✓ Uploaded file: files/def456
✓ Successfully uploaded 2/2 PDF files
✓ File search store created!
✓ Store ID (copy this for the chatbot): f9abee98-c29b-4cc2-bf22-aa008d32271d
✓ Store data saved to: f9abee98-c29b-4cc2-bf22-aa008d32271d.json
```

### Step 4: Run the Chatbot

1. The Store ID is automatically configured in `chatbot.py`
2. Run the chatbot:
   ```bash
   python chatbot.py
   ```

3. Start asking questions about your research papers!

**Example interaction:**
```
==================================================
🤖 Research Papers Chatbot Ready!
Ask questions about your papers. Type 'quit' to exit.
==================================================

❓ Your question: What are the main findings about metabolic regulation?

🤔 Thinking...

🤖 Answer: The research shows that metabolic regulation involves complex interactions between insulin signaling pathways and glucose uptake mechanisms. Key findings include...

📚 Sources: research_paper_1.pdf, research_paper_2.pdf

❓ Your question: Can you explain the methodology used in the Roth study?
...
```

## Configuration Options

### Model Selection

In `chatbot.py`, you can change the model:
```python
MODEL_NAME = "gemini-pro"  # Current default
# MODEL_NAME = "gemini-1.5-pro"  # For higher quality (if available)
```

### File Organization

- `create_store.py`: Handles PDF upload and store creation
- `chatbot.py`: Interactive Q&A interface
- `papers/`: Place your PDF files here
- Store data is saved as JSON files (auto-generated)

## Project Structure

```
gemini-research-chatbot/
├── app.py                  # Streamlit web interface (recommended)
├── create_store.py         # Store creation script (CLI)
├── chatbot.py              # Interactive chatbot (CLI)
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore rules
├── README.md              # This file
├── papers/                # Your PDF files (create this folder)
└── .venv/                 # Virtual environment (auto-created)
```

## Troubleshooting

### Common Issues

1. **API Key Invalid**
   - Ensure your API key is correct and has Gemini API access
   - Check that billing is enabled on your Google Cloud project

2. **Model Not Found**
   - Some models may not be available in all regions
   - Try switching to "gemini-pro" in the configuration

3. **No Files Found**
   - Ensure PDFs are in the `papers/` folder
   - Check file permissions

4. **Rate Limiting**
   - The scripts automatically handle rate limits
   - Wait and retry if you hit limits

### Error Messages

- `"API key not valid"`: Check your API key configuration
- `"No files available in the store"`: Run `create_store.py` first
- `"Store file not found"`: Ensure you ran the store creation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source. Please check the license file for details.

## Disclaimer

This tool uses Google's Gemini AI service. Ensure compliance with Google's terms of service and your organization's policies regarding AI usage and data privacy.