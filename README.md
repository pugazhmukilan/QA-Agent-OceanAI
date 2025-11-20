# 🤖 Autonomous QA Agent

An intelligent Quality Assurance automation system powered by Google Gemini AI that generates test cases and Selenium scripts automatically from documentation and HTML sources.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Usage Guide](#usage-guide)
- [Support Documents](#support-documents)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Troubleshooting](#troubleshooting)

## 🎯 Overview

The Autonomous QA Agent is a comprehensive testing solution that leverages AI to automate the entire QA workflow:

1. **Knowledge Base Building**: Ingests HTML files, specifications, and documentation
2. **Semantic Search**: Uses ChromaDB vector database for intelligent document retrieval
3. **Test Case Generation**: AI-powered test case creation based on business rules
4. **Script Automation**: Generates executable Selenium Python scripts
5. **Interactive Q&A**: Chat interface for querying documentation

## ✨ Features

- **AI-Powered Analysis**: Utilizes Google Gemini 2.0 Flash for intelligent test generation
- **Vector Database**: ChromaDB integration for semantic search and context retrieval
- **Multi-Format Support**: Handles HTML, PDF, Markdown, TXT, and JSON files
- **Dual Interface**: FastAPI backend + Streamlit frontend
- **Test Planning Modes**: 
  - Standard Functional Testing
  - Edge Cases & Security Testing
- **Selenium Code Generation**: Automatic creation of executable test scripts
- **Real-time Logging**: Monitor system operations and debugging
- **CORS Enabled**: Ready for cross-origin requests

## 🏗️ Architecture

```
┌─────────────────┐
│   Streamlit UI  │ (Frontend - Port 8501)
└────────┬────────┘
         │
         ├──► Knowledge Base Builder
         ├──► QA Chat Interface
         ├──► Test Case Planner
         └──► Selenium Script Generator
         │
         ▼
┌─────────────────┐
│   ChromaDB      │ (Vector Database)
└─────────────────┘
         │
         ▼
┌─────────────────┐
│  FastAPI Server │ (Backend - Port 8000)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Gemini 2.0 API │ (AI Processing)
└─────────────────┘
```

## 📦 Prerequisites

### System Requirements
- **Python**: 3.10 or higher (recommended: 3.11+)
- **Operating System**: Windows, macOS, or Linux
- **RAM**: Minimum 4GB (8GB recommended)
- **Disk Space**: 500MB free space

### API Requirements
- **Google Gemini API Key**: Required ([Get it here](https://aistudio.google.com))

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/pugazhmukilan/QA-Agent-OceanAI.git
cd QA-Agent-OceanAI
```

### 2. Set Up Backend

```powershell
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv backvenv

# Activate virtual environment
.\backvenv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirement.txt
```

### 3. Set Up Frontend

```powershell
# Navigate to frontend directory
cd ..\frontend

# Create virtual environment
python -m venv qavenv

# Activate virtual environment
.\qavenv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

## ⚙️ Configuration

### Backend Configuration

Create a `.env` file in the `backend` directory (optional):

```env
# Optional environment variables
HOST=0.0.0.0
PORT=8000
```

### Frontend Configuration

The frontend uses `variables.py` for configuration:

```python
# Location: frontend/variables.py
CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "qa_knowledge_base"
```

## 🎮 Running the Application

### Option 1: Run Both Services (Recommended)

**Terminal 1 - Backend (FastAPI)**
```powershell
cd backend
.\backvenv\Scripts\Activate.ps1
uvicorn app:app --reload --port 8000
```

**Terminal 2 - Frontend (Streamlit)**
```powershell
cd frontend
.\qavenv\Scripts\Activate.ps1
streamlit run app.py
```

### Option 2: Production Deployment

**Backend:**
```powershell
cd backend
.\backvenv\Scripts\Activate.ps1
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4
```

**Frontend:**
```powershell
cd frontend
.\qavenv\Scripts\Activate.ps1
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

### Access the Application

- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 📖 Usage Guide

### Step 1: Configure API Key

1. Open the application at `http://localhost:8501`
2. In the sidebar, enter your **Gemini API Key**
3. The key is required for all AI operations

### Step 2: Build Knowledge Base

1. **Upload checkout.html**: The HTML file you want to test
2. **Upload Specs/Docs**: Supporting documentation (PDF, MD, TXT, JSON)
3. Click **"Build Knowledge Base"** button
4. Wait for the processing to complete

**Supported Files:**
- `checkout.html` - Target HTML for testing
- `product_specs.md` - Business rules and specifications
- `api_endpoints.json` - API documentation
- `ui_ux_guide.txt` - UI/UX guidelines

### Step 3: Explore Knowledge Base

Navigate to the **"📊 Knowledge Base"** tab to:
- View loaded HTML context
- Check ChromaDB status
- See document chunk count
- Inspect stored data structure

### Step 4: Chat with Documentation

In the **"💬 QA Chat"** tab:
1. Ask questions about your documentation
2. Examples:
   - "What is the discount logic?"
   - "What are the shipping rules?"
   - "How should payment validation work?"
3. Get AI-powered answers based on your uploaded documents

### Step 5: Generate Test Cases

In the **"📝 Test Planner"** tab:
1. Select generation mode:
   - **Standard Functional**: Happy path test cases
   - **Edge Cases & Security**: Boundary testing, XSS, injection tests
2. Click **"Generate Test Cases"**
3. Review generated test cases with:
   - Test Case ID
   - Feature description
   - Scenario details
   - Expected results
   - Source grounding (traceability)
4. Select a test case for automation

### Step 6: Generate Selenium Scripts

In the **"💻 Script Gen"** tab:
1. View your selected test case
2. Click **"Generate Python Script"**
3. Wait for AI to generate executable Selenium code
4. Click **"Explain Code"** for detailed explanation
5. Copy and execute the generated script

**Generated Script Features:**
- Uses Selenium WebDriver (Chrome)
- Includes explicit waits
- Proper element selectors (IDs, names, CSS)
- Comprehensive comments
- Error handling
- Based on actual HTML structure

## 📚 Support Documents

The `assets` folder contains example documents that demonstrate the system's capabilities:

### 1. `checkout.html`
**Purpose**: Sample e-commerce checkout page for testing

**Contents**:
- Product catalog with add-to-cart functionality
- Shopping cart display
- Discount code input field
- Shipping method selection (Standard/Express)
- Payment method options (Credit Card/PayPal)
- Customer information form (Name, Email, Address)
- Form validation logic
- Order submission functionality

**Usage**: Upload this file to test the entire QA automation workflow

### 2. `product_specs.md`
**Purpose**: Business rules and functional specifications

**Contains**:
- **Discount Rules**: SAVE15 code provides 15% discount
- **Shipping Rules**: Free standard, $10 express
- **Payment Rules**: Validation requirements, supported methods
- **Cart Behavior**: Add items, totals calculation
- **Success Criteria**: Expected user feedback

**Usage**: Helps AI understand business logic for test generation

### 3. `api_endpoints.json`
**Purpose**: API documentation for backend integration

**Defines**:
- **POST /apply_coupon**: Coupon validation endpoint
  - Parameters: code (string)
  - Example: "SAVE15"
- **POST /submit_order**: Order submission endpoint
  - Parameters: name, email, address, items, payment_method, shipping_method

**Usage**: Enables API testing scenarios and integration tests

### 4. `ui_ux_guide.txt`
**Purpose**: UI/UX design specifications and guidelines

**Covers**:
- **Color & Styling**: Error messages (red), buttons (green), success messages
- **Layout**: Center-aligned, bordered cards for products
- **Validation Rules**: Mandatory fields, inline error placement
- **Button Placement**: Add-to-cart, discount application
- **Accessibility**: Labels, radio button grouping

**Usage**: Ensures generated tests verify UI/UX compliance

## 📁 Project Structure

```
QA-Agent/
├── assets/                      # Support documents
│   ├── api_endpoints.json       # API documentation
│   ├── checkout.html            # Sample HTML to test
│   ├── product_specs.md         # Business specifications
│   └── ui_ux_guide.txt          # UI/UX guidelines
│
├── backend/                     # FastAPI Server
│   ├── app.py                   # Main FastAPI application
│   ├── models.py                # Pydantic models
│   ├── requirement.txt          # Backend dependencies
│   ├── Dockerfile               # Container configuration
│   ├── .dockerignore            # Docker ignore rules
│   ├── .gitignore               # Git ignore rules
│   └── backvenv/                # Virtual environment
│
├── frontend/                    # Streamlit UI
│   ├── app.py                   # Main Streamlit app
│   ├── init_app.py              # Session state initialization
│   ├── utils.py                 # Helper functions
│   ├── variables.py             # Configuration variables
│   ├── requirements.txt         # Frontend dependencies
│   ├── .gitignore               # Git ignore rules
│   ├── chroma_db/               # Vector database storage
│   └── qavenv/                  # Virtual environment
│
└── chroma_db/                   # Shared ChromaDB storage
```

## 🔌 API Documentation

### Backend Endpoints

#### `GET /`
**Description**: Health check endpoint

**Response**:
```json
{
  "message": "Welcome to the FastAPI application!"
}
```

#### `POST /generate`
**Description**: Generate AI response using Gemini

**Request Body**:
```json
{
  "apikey": "your-gemini-api-key",
  "prompt": "Your prompt text here"
}
```

**Response**:
```json
{
  "response": "AI generated response"
}
```

**Error Responses**:
- `400 Bad Request`: API key missing
- `500 Internal Server Error`: Generation failed

### Frontend Functions

#### `build_vector_db(docs, html, api_key)`
Ingests documents into ChromaDB vector database

#### `search_vector_db(query, api_key, top_k=3)`
Performs semantic search on knowledge base

#### `generate_with_gemini(prompt, api_key)`
Calls backend API for AI generation

#### `createresponse(input, api_key)`
Creates contextualized chat responses

## 🛠️ Troubleshooting

### Common Issues

#### 1. "API Key is required!" Error
**Solution**: Enter your Gemini API key in the sidebar before building knowledge base

#### 2. ChromaDB Collection Not Found
**Solution**: Upload files and click "Build Knowledge Base" first

#### 3. PDF Files Not Loading
**Solution**: 
- Ensure `pypdf` is installed: `pip install pypdf`
- Check PDF is not corrupted
- Try with a different PDF

#### 4. Port Already in Use
**Backend:**
```powershell
# Use different port
uvicorn app:app --port 8001
```

**Frontend:**
```powershell
streamlit run app.py --server.port 8502
```

#### 5. Import Errors
**Solution**: 
```powershell
# Recreate virtual environment
deactivate
Remove-Item -Recurse -Force qavenv
python -m venv qavenv
.\qavenv\Scripts\Activate.ps1
pip install -r requirements.txt
```

#### 6. CORS Issues
The backend already has CORS enabled for all origins. If issues persist, check your browser console.

### Debug Mode

**Enable verbose logging in Streamlit:**
```powershell
streamlit run app.py --logger.level=debug
```

**Check ChromaDB data:**
Navigate to the "📊 Knowledge Base" tab and expand "View Stored Data Structure"

## 🐳 Docker Deployment (Backend)

The backend includes a Dockerfile for containerization:

```powershell
cd backend
docker build -t qa-agent-backend .
docker run -p 8000:8000 qa-agent-backend
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is part of the OceanAI initiative.

## 🙏 Acknowledgments

- **Google Gemini AI**: Powering intelligent test generation
- **ChromaDB**: Vector database for semantic search
- **Streamlit**: Beautiful UI framework
- **FastAPI**: Modern web framework for APIs

## 📞 Support

For issues and questions:
- **GitHub Issues**: [Create an issue](https://github.com/pugazhmukilan/QA-Agent-OceanAI/issues)
- **Repository**: [QA-Agent-OceanAI](https://github.com/pugazhmukilan/QA-Agent-OceanAI)

## 🔮 Future Enhancements

- [ ] Support for more test frameworks (Playwright, Cypress)
- [ ] API testing automation
- [ ] Test execution dashboard
- [ ] CI/CD integration
- [ ] Multi-language support
- [ ] Performance testing capabilities
- [ ] Visual regression testing

---

**Made with ❤️ for Quality Assurance Automation**
