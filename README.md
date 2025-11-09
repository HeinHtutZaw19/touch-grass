# Touch Grass

## Description

**Touch Grass** will be a subscription base chrome extension service which turns self discovery into a game. Instead of long lessons or recommendations, users will receive random “side quests” like go dance, or go on a walk and be asked to take a photo or video to submit. To build accountability, users can invite a friend to verify when a quest is completed. Touch Grass uses a Vite + React frontend and a Chrome Extension UI, with a Flask backend and Supabase for auth, database, and storage. OpenAI generates personalized quests and Firecrawl provides contextual data


## How to Run
### Chrome Extension

* Please request the required `.env` file from our team: **heinzaw.official@gmail.com**

```bash
# Go into the project directory
cd touch-grass-chs

# Build the Chrome extension
npm run build
```
* This will create a build in the build folder
* Then open chrome and go to `chrome://extensions`
* Toggle on the **developer mode**
* Click on **Load unpacked** and select the **build folder made above**
* This will load the touch-grass chrome extension

### Landing Page

```bash
cd frontend
npm install
npm run dev
```
* This will open the `http://localhost:5173/`

### Backend

* Create a conda / python virtual environment
```bash
cd backend
pip install -r requirements.txt
python -m dotenv -f .env run python -m app.main
```
* This would run in `http://localhost:5001`