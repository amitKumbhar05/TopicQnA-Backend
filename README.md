# Topic & Question Tracker (Serverless Backend)

A lightweight, serverless-ready backend API built with **FastAPI**, **Neon (PostgreSQL)**, and **Firebase Authentication**. This system allows users to create topics, log interview/study questions, and store answers in Markdown format with revision tracking.

## 🚀 Tech Stack

*   **Framework:** FastAPI (Python 3.10+)
*   **Database:** Neon (Serverless PostgreSQL)
*   **ORM:** SQLModel (SQLAlchemy wrapper)
*   **Auth:** Firebase Admin SDK (Bearer Token Middleware)
*   **Package Manager:** [uv](https://github.com/astral-sh/uv) (An extremely fast Python package installer and resolver)

---

## 🛠️ Prerequisites

Before starting, ensure you have the following:

1.  **uv installed:**
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
2.  **Neon Database:** A project created on [Neon.tech](https://neon.tech) with the connection string ready.
3.  **Firebase Project:** A project on [Firebase Console](https://console.firebase.google.com/) with a generated **Service Account Private Key** (`.json` file).

---

## ⚙️ Installation & Setup

### 1. Initialize & Install Dependencies
Since you initialized the project with `uv`, we will add the required packages to your `pyproject.toml` and virtual environment in one go.

Run the following command in your project root:

```bash
uv sync
```

### 2. Environment Configuration
Create a `.env` file in the root directory to store your secrets.

```bash
touch .env
```

Open `.env` and paste the following (replace with your actual values):

```env
DATABASE_URL=postgresql://user:password@ep-something.aws.neon.tech/neondb?sslmode=require

GOOGLE_APPLICATION_CREDENTIALS=./firebase-creds.json
```

> **⚠️ Security Note:** Ensure `.env` and your `firebase-creds.json` are included in your `.gitignore` file so they are not pushed to GitHub.

---

## ▶️ Running the Application

Use `uv` to run the Uvicorn server. This ensures the command runs within the correct virtual environment managed by `uv`.

```bash
uv run uvicorn app.main:app --reload
```

*   **API Root:** `http://127.0.0.1:8000`
*   **Interactive Docs (Swagger UI):** `http://127.0.0.1:8000/docs`
*   **Alternative Docs (ReDoc):** `http://127.0.0.1:8000/redoc`

---

## 📡 API Documentation

### Authentication
**All endpoints (except Health Check) require Authentication.**
You must send a valid Firebase ID Token in the request header.

*   **Header:** `Authorization`
*   **Value:** `Bearer <YOUR_FIREBASE_ID_TOKEN>`

### 1. Topics API
*Manage the subjects or categories you are studying.*

| Method | Endpoint | Description | Payload (JSON) |
| :--- | :--- | :--- | :--- |
| **GET** | `/topics` | List all topics belonging to the authenticated user. | N/A |
| **POST** | `/topics` | Create a new topic. | `{"name": "Python Interview"}` |
| **PUT** | `/topics/{id}` | Rename a topic. | `{"name": "Advanced Python"}` |
| **DELETE** | `/topics/{id}` | Delete a topic **and all its questions**. | N/A |

### 2. Questions API
*Manage questions and Markdown answers within specific topics.*

| Method | Endpoint | Description | Payload (JSON) |
| :--- | :--- | :--- | :--- |
| **POST** | `/topics/{id}/questions` | Add a new question to a specific topic. | `{"question_text": "What is GIL?", "answer_text": "## Markdown Answer..."}` |
| **GET** | `/topics/{id}/questions` | Get all questions for a specific topic. | N/A |
| **GET** | `/questions/{id}` | Get details of a single question. | N/A |
| **PUT** | `/questions/{id}` | Update question text or markdown answer. | `{"answer_text": "Updated markdown..."}` |
| **DELETE** | `/questions/{id}` | Delete a specific question. | N/A |

### 3. Revision Logic
*Track how often you review a question.*

| Method | Endpoint | Description | Purpose |
| :--- | :--- | :--- | :--- |
| **POST** | `/questions/{id}/revise` | Increment revision counter. | Call this when you finish reviewing a question to track progress. |

---

## 📂 Project Structure

```text
/topic-tracker-backend
├── app/
│   ├── main.py              # App entry point & DB init
│   ├── database.py          # Neon DB connection
│   ├── dependencies.py      # Firebase Auth middleware
│   ├── models/              # SQLModel Database Tables
│   ├── routers/             # API Route Handlers
│   └── schemas/             # Pydantic Data Validation
├── .env                     # Secrets (Excluded from Git)
├── firebase-creds.json      # Firebase Keys (Excluded from Git)
├── pyproject.toml           # uv dependency file
└── uv.lock                  # uv lock file
```

## 🐳 Deployment (Docker)

If you need to build a container (e.g., for Google Cloud Run), a `Dockerfile` is included.

```bash
# Build
docker build -t topic-tracker .

# Run (Requires passing env vars)
docker run -p 8080:8080 --env-file .env topic-tracker
```