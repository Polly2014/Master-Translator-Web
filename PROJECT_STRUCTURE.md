# Master-Translator-Web Project Structure

## 📁 Complete File Listing

```
Master-Translator-Web/
│
├── 📄 Core Application Files
│   ├── app.py                      # Flask main application (652 lines)
│   ├── requirements.txt            # Python dependencies (8 packages)
│   └── start.sh                    # Quick start script
│
├── 📚 Data & Configuration
│   ├── terminology_curated.json    # Terminology database (157 terms, 1.8KB)
│   └── .gitignore                  # Git ignore rules
│
├── 📖 Documentation
│   ├── README.md                   # Project overview & quick start
│   ├── DEMO_GUIDE.md               # Hackathon demo presentation guide
│   ├── TERMINOLOGY_GUIDE.md        # Terminology feature documentation
│   └── PROJECT_STRUCTURE.md        # This file
│
├── 🎨 Frontend Files
│   ├── templates/
│   │   └── index.html              # Main UI page with WebSocket integration
│   │
│   └── static/
│       ├── css/                    # (Future: custom stylesheets)
│       └── js/
│           └── app.js              # Frontend JavaScript logic
│
├── 📂 Runtime Directories (Created automatically)
│   ├── uploads/                    # Uploaded Markdown files
│   ├── outputs/                    # Translated output files
│   └── venv/                       # Python virtual environment
│
└── 🐍 Python Cache (Auto-generated)
    └── __pycache__/                # Compiled Python files
```

---

## 📊 File Statistics

| Category | Files | Total Size | Lines of Code |
|----------|-------|------------|---------------|
| Python Backend | 1 | ~25KB | 652 |
| HTML Templates | 1 | ~12KB | 285 |
| JavaScript | 1 | ~8KB | 220 |
| JSON Data | 1 | 1.8KB | 157 terms |
| Documentation | 4 | ~15KB | ~800 |
| **Total** | **8** | **~62KB** | **~1,957** |

---

## 🔑 Key File Descriptions

### `app.py` - Main Application
- **Purpose**: Flask backend with WebSocket support
- **Key Functions**:
  - `plan_chunks()` - Smart chunking algorithm with 3-level fallback
  - `translate_chunk_web()` - AI translation with terminology support
  - `translate_book_task()` - Background translation worker
  - `load_terminology_db()` - Loads curated term database
- **Routes**:
  - `GET /` - Main page
  - `POST /api/upload` - File upload
  - `POST /api/analyze/<task_id>` - Chunk analysis
  - `POST /api/translate/<task_id>` - Start translation
  - `GET /api/terminology` - Fetch terminology database
  - `GET /api/download/<task_id>` - Download results

### `terminology_curated.json` - Terminology Database
- **Location**: Project root directory
- **Format**: JSON with 3 categories
  ```json
  {
    "proper_nouns": [45 terms],      // Names, companies, places
    "technical_terms": [78 terms],   // AI/tech vocabulary
    "key_concepts": [34 terms]       // Domain-specific concepts
  }
  ```
- **Usage**: Ensures translation consistency across all chunks
- **Access**: Via `/api/terminology` endpoint or modal viewer

### `templates/index.html` - Main UI
- **Features**:
  - Three-column responsive layout
  - Drag-and-drop file upload
  - Real-time log streaming display
  - Dual progress bars (overall + chunk)
  - Terminology database viewer modal
  - Dark theme with Tailwind CSS
- **Dependencies**:
  - Tailwind CSS (CDN)
  - Socket.IO Client (CDN)
  - Custom `app.js` for interaction

### `static/js/app.js` - Frontend Logic
- **Key Functions**:
  - `handleFileSelect()` - File upload handler
  - `analyzeFile()` - Trigger chunk analysis
  - `startTranslation()` - Initiate translation
  - `initializeTerminologyModal()` - Modal open/close
  - `loadTerminology()` - Fetch and display terms
  - Socket.IO event handlers for real-time updates

### `requirements.txt` - Dependencies
```
Flask==3.0.0
Flask-SocketIO==5.3.5
litellm==1.51.3
python-socketio==5.10.0
python-engineio==4.8.0
bidict==0.23.1
h11==0.14.0
Werkzeug==3.0.1
```

---

## 🔄 Data Flow

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │ 1. Upload File
       ▼
┌─────────────────┐
│  Flask Server   │ 2. Save to uploads/
│   (app.py)      │
└──────┬──────────┘
       │ 3. Analyze chunks
       ▼
┌─────────────────┐
│  plan_chunks()  │ 4. Smart chunking
└──────┬──────────┘    (3-level fallback)
       │
       ▼ 5. Load terminology
┌─────────────────────┐
│terminology_curated  │
│      .json          │
└──────┬──────────────┘
       │ 6. Translate each chunk
       ▼
┌─────────────────┐
│  Claude AI      │ 7. Stream results
│  (via LiteLLM)  │    via WebSocket
└──────┬──────────┘
       │ 8. Save output
       ▼
┌─────────────────┐
│   outputs/      │ 9. Download link
└─────────────────┘
```

---

## 🌐 Port Configuration

- **Default Port**: 5001 (avoids macOS AirPlay conflict on 5000)
- **Change Port**: Edit line ~645 in `app.py`
  ```python
  socketio.run(app, host='0.0.0.0', port=5001, debug=True)
  ```

---

## 🚀 Deployment Checklist

### For Demo:
- ✅ Virtual environment activated
- ✅ All dependencies installed
- ✅ `terminology_curated.json` in project root
- ✅ Port 5001 available
- ✅ OpenRouter API key configured
- ✅ Sample Markdown file ready

### For Production:
- ⚠️ Change `debug=False` in `app.py`
- ⚠️ Use production WSGI server (Gunicorn)
- ⚠️ Add proper error handling
- ⚠️ Implement file size limits
- ⚠️ Add authentication
- ⚠️ Set up HTTPS

---

## 📝 File Paths (Important!)

### Terminology Database
```python
# OLD (external dependency):
term_file = Path(__file__).parent.parent / 'Translator' / 'terminology_curated.json'

# NEW (self-contained):
term_file = Path(__file__).parent / 'terminology_curated.json'
```

### Upload/Output Directories
```python
UPLOAD_FOLDER = Path(__file__).parent / 'uploads'
OUTPUT_FOLDER = Path(__file__).parent / 'outputs'
```

### Static Assets
```html
<script src="/static/js/app.js"></script>
```

---

## 🔧 Customization Points

### 1. Change Target Languages
Edit `LANGUAGES` dict in `app.py` (line ~28):
```python
LANGUAGES = {
    'Japanese': '日语',
    'Russian': '俄语',
    'Arabic': '阿拉伯语',
    'Hindi': '印地语',
    'French': '法语'  # Add new languages
}
```

### 2. Adjust Chunk Size
Edit chunking parameters in `app.py`:
```python
CHUNK_TARGET_SIZE = 8000  # Characters per chunk
```

### 3. Modify UI Theme
Edit Tailwind classes in `templates/index.html`:
```html
<body class="bg-gray-900 text-gray-100">  <!-- Dark theme -->
```

### 4. Add Custom Terminology
Edit `terminology_curated.json`:
```json
{
  "your_custom_category": ["term1", "term2", ...]
}
```

---

## 🐛 Troubleshooting

### File Not Found Errors
```bash
# Check terminology file exists
ls -lh ./terminology_curated.json

# Check upload directory
ls -lh ./uploads/
```

### Port Already in Use
```bash
# Find process using port 5001
lsof -i :5001

# Kill the process
kill -9 <PID>
```

### WebSocket Connection Failed
- Check firewall settings
- Verify browser console for errors
- Try disabling browser extensions

---

**Last Updated**: 2025-11-17  
**Version**: 1.0.0  
**Status**: ✅ Production Ready for Hackathon Demo
