# Yellow Pages Sports Chatbot API

Professional modular Flask API for the Sports Chatbot.

## 🚀 Deployment

### Railway (Recommended)

1.  **Repo Structure**: Ensure your repo matches this folder structure.
2.  **Entry Point**: `run.py` (configured in `Procfile` as `run:app`).
3.  **Environment Variables**:
    *   `OPENAI_API_KEY`: Your OpenAI API Key.

The project is ready for one-click deployment on Railway using the included `Procfile`.

### Render (Free Tier Alternative)

Render offers a generous free tier for web services.

1.  **Sign up**: Go to [render.com](https://render.com).
2.  **New Web Service**: Connect your GitHub repository.
3.  **Settings**:
    *   **Runtime**: Python 3
    *   **Build Command**: `pip install -r requirements.txt`
    *   **Start Command**: `gunicorn run:app`
4.  **Environment Variables**:
    *   Add `OPENAI_API_KEY` in the "Environment" tab.


## 📁 Project Structure

```text
.
├── app/
│   ├── api/                 # API Routes
│   ├── agents/              # Intelligent Agents (Search, Knowledge, Router)
│   ├── core/                # Configuration (Env vars, Constants)
│   └── services/            # Integrations (LLM, VectorStore)
├── data/
│   ├── raw/                 # Original Excel data
│   └── vectorstore/         # FAISS Vector Index
├── run.py                   # Application Entry Point
├── Procfile                 # Deployment Config
└── requirements.txt         # Dependencies
```

## 🛠️ Local Development

1.  **Create Virtual Environment** (Recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run Application**:
    ```bash
    export OPENAI_API_KEY=your-key-here
    python run.py
    ```

4.  **Test API**:
    ```bash
    curl -X POST http://localhost:5000/chat \
      -H "Content-Type: application/json" \
      -d '{"message": "หาโยคะในกรุงเทพ"}'
    ```
