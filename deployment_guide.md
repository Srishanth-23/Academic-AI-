# 🚀 Deployment Guide

Follow these steps to deploy your application and generate a standalone mobile app (.apk for Android).

## 1. 📱 Generate standalone Mobile App (Android/iOS)

The easiest way to get an app file is using **Expo Application Services (EAS)**.

### Step-by-Step:
1.  **Install EAS CLI**:
    ```bash
    npm install -g eas-cli
    ```
2.  **Login to Expo**:
    ```bash
    eas login
    ```
3.  **Configure Project**:
    ```bash
    eas build:configure
    ```
4.  **Update backend URL**:
    In `src/services/apiClient.ts`, ensure `BASE_URL` points to your **deployed backend** (see section below) instead of `localhost`.
5.  **Build for Android (APK)**:
    ```bash
    eas build --platform android --profile preview
    ```
    *This will provide a link to download the `.apk` file once finished.*

---

## 2. 🌐 Deploy Backend (FastAPI)

You need to host your Python backend online so the mobile app can reach it from anywhere.

### Recommended: [Render](https://render.com) or [Railway](https://railway.app)
1.  **Connect GitHub**: Push your `academic_ai_backend` folder to a GitHub repository.
2.  **Create New Web Service**:
    - **Build Command**: `pip install -r requirements.txt`
    - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
3.  **Environment Variables**:
    Add all variables from your local `.env` file to the Render/Railway dashboard:
    - `DATABASE_URL` (Use a managed PostgreSQL like Supabase or Render DB)
    - `SECRET_KEY`, `ALGORITHM`, etc.
    - `SUPA_URL`, `SUPA_KEY`, `GEMINI_API_KEY`

---

## 3. 🗄️ Database (PostgreSQL)

Since you are currently using a local PostgreSQL, you must move it to a cloud provider.

### Recommended: [Supabase](https://supabase.com)
1.  Create a new project on Supabase.
2.  Go to **Project Settings > Database** to get your **Connection String**.
3.  Update your `DATABASE_URL` in your deployed backend environment variables.
4.  Run your initialization scripts (`sql_seed.py`) against the new database URL one time to populate it.

---

## 4. ⚙️ Environment Summary

| Component | Local URL | Deployment Strategy |
| :--- | :--- | :--- |
| **Backend (FastAPI)** | `http://localhost:8000` | Render / Railway / Heroku |
| **Frontend (Mobile)** | `Metro Bundler` | EAS Build (生成 APK/IPA) |
| **Secondary Backend** | `http://localhost:3000` | Render (Node.js Service) |
| **Database** | `Local Postgres` | Supabase / Managed Postgres |

> [!IMPORTANT]
> Once the backend is deployed (e.g., to `https://my-api.onrender.com`), you **MUST** update the `BASE_URL` in `SDG-HAck/src/services/apiClient.ts` before building the app.
