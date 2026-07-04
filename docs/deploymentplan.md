# Deployment Plan: Railway (Backend) & Vercel (Frontend)

This document outlines the steps to deploy the Mutual Fund RAG Assistant to production.

## 1. Prerequisites
- A GitHub repository containing this entire codebase, completely pushed and up-to-date.
- Accounts on [Railway.app](https://railway.app/) and [Vercel.com](https://vercel.com/).
- Your Groq API Key.

## 2. Code Changes Required Before Deployment

### Frontend Updates (`frontend/src/App.jsx`)
Currently, the frontend hardcodes the backend URL to localhost. We need to make it dynamic.
Change the fetch call in `frontend/src/App.jsx` from:
```javascript
const response = await fetch('http://localhost:8001/chat', {
```
To:
```javascript
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001';
const response = await fetch(`${API_URL}/chat`, {
```

### Backend Updates (Root Directory)
Railway needs to know exactly how to start your FastAPI server.
Create a file named `Procfile` (no extension) in the root of your project folder (`d:\NEXTLEAP\Mutual fund RAG\Procfile`) with this exact content:
```text
web: uvicorn src.api:app --host 0.0.0.0 --port $PORT
```

---

## 3. Backend Deployment (Railway)

1. Log in to **Railway** and create a **New Project** -> **Deploy from GitHub repo**.
2. Select your repository. If you are asked to select a root directory, keep it as the default root (`/`).
3. Once the initial build starts, it might fail because it lacks the API key. Go to the **Variables** tab for the service and add:
   - `GROQ_API_KEY`: `your-actual-groq-api-key`
4. Go to the **Settings** tab:
   - Under **Environment**, find **Public Networking** and click **Generate Domain**.
   - Copy this newly generated domain URL (e.g., `https://mutual-fund-api.up.railway.app`). **This is your Backend API URL.**
5. **Continuous Data Updates:** Railway handles the database updates perfectly. Because the daily GitHub Action scheduler commits the new `chroma_db` back to the GitHub repository, Railway will detect the new commit and automatically re-deploy the API with the fresh data every single day!

---

## 4. Frontend Deployment (Vercel)

1. Log in to **Vercel** and click **Add New...** -> **Project**.
2. Import your GitHub repository.
3. Configure the Project:
   - **Framework Preset**: Vercel should auto-detect `Vite`.
   - **Root Directory**: Click "Edit" and select the `frontend` folder. (This is critical).
4. Open the **Environment Variables** section and add:
   - **Name**: `VITE_API_URL`
   - **Value**: The Railway backend URL you copied earlier (e.g., `https://mutual-fund-api.up.railway.app`). Ensure there is no trailing slash.
5. Click **Deploy**. Vercel will run `npm run build` inside the frontend directory and give you a live, public URL.

---

## 5. Verification
- Open your live Vercel URL in your browser.
- Try asking: *"What is the exit load for the Nippon India Small Cap fund?"*
- The frontend will securely ping your Railway backend, process the chunks using the embedded database, and generate an answer using Groq!
