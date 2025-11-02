# Telegram-Ecommerce-Bot

Telegram-Ecommerce-Bot is a small project combining a Django backend (simple ecommerce API) with a Telegram bot and an AI agent. The bot can interact with the ecommerce backend to list products, show details and assist users via an AI agent.

## Key features
- Django backend with product models and REST endpoints
- Telegram bot implementation to interact with users
- Optional AI agent notebook and script for advanced interactions
- SQLite for local development

## Repository layout
- `.env` / `.env.example` - environment variables (keep secrets out of git)
- `backend/` - Django project and app
  - `manage.py`, `ecommerce/` (Django project), `app/` (Django app)
- `src/` - Telegram bot and AI agent scripts
  - `telegram_bot.py` - main bot script
  - `ai_agent.py` - AI helper script
- `notebook/` - Jupyter notebook for experiments
- `requirements.txt` - Python dependencies

## Requirements
- Python 3.10+ (match your environment)
- pip
- Windows (instructions below target Windows shells)

## Quick setup (Windows)
1. Clone repo and open project folder:
   - Use your existing folder: `e:\personal project\ecommerxe-telegram\Telegram-Ecommerce-Bot`

2. Create and activate virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Prepare environment variables:
   - Copy `.env.example` to `.env` and fill values (common variables shown below).
   - Required variables (example names — adapt to your `.env.example`):
     - `TELEGRAM_BOT_TOKEN` — your Telegram bot token
     - `DJANGO_SECRET_KEY` — Django SECRET_KEY
     - `DEBUG` — `True`/`False`
     - `ALLOWED_HOSTS` — comma separated hosts

   On Windows you can temporarily set a variable for a session:
   ```
   set TELEGRAM_BOT_TOKEN=xxxx:yyyy
   set DJANGO_SECRET_KEY=your_django_secret
   ```

5. Database migrations:
   ```
   cd backend
   python manage.py migrate
   python manage.py createsuperuser   # optional, for admin
   ```

## Running services
- Start Django backend (development):
  ```
  cd backend
  python manage.py runserver
  ```
  Backend API will default to `http://127.0.0.1:8000/api/products?search=<product>`.

- Run Telegram bot:
  ```
  cd ..
  venv\Scripts\activate   # if not already active
  python src\telegram_bot.py
  ```
  Ensure `TELEGRAM_BOT_TOKEN` is set in the environment or loaded by your `.env` handling.

- Run AI agent (script or notebook):
  ```
  python src\ai_agent.py
  ```
  Or open `notebook/ai_agent.ipynb` in Jupyter.

## Testing
Run Django tests:
```
cd backend
python manage.py test
```

## Development notes
- Database is SQLite (`backend/db.sqlite3`) for local development.
- Add/modify API endpoints in `backend/app/views.py` and serializers in `backend/app/serializers.py`.
- Bot logic is in `src/telegram_bot.py`. AI helper code in `src/ai_agent.py`.

## Troubleshooting
- If imports fail, ensure virtual environment is active and dependencies installed.
- Check the bot token and that the bot is started; look for error messages in the terminal.
- For Django issues, read the development server traceback in the terminal.

## Contributing
- Open an issue or PR with a clear description.
- Keep sensitive keys out of commits; use `.env`.

## License
Add your preferred license or COPYRIGHT information here.

