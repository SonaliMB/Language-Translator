# Language Translator

A small web app that translates text between 35 languages. A plain HTML/CSS/JavaScript frontend talks to a FastAPI backend, which uses the OpenAI Chat Completions API to do the translation.

## Features

- Choose the source and target language from dropdown lists, or let the app **auto-detect** the source language
- Swap button that reverses the language pair and moves the translation back into the input
- Character counter, Clear and Copy buttons, and a Ctrl + Enter shortcut
- Loading state and readable error messages (empty input, same language selected, server errors, backend unreachable)
- Responsive layout that works on desktop and mobile
- Input validation on the server for supported languages

## Project structure

```
.
├── frontend
|   ├── index.html               # Frontend markup and JavaScript
|   ├── style.css                # Frontend styles
├── backend
|   ├── fastapi_translator.py    # FastAPI backend
|   ├──.env                      # Your API key (not committed)
├── requirements.txt         # Python dependencies (see below)
├── .gitignore
└── README.md
```

## Requirements

- Python 3.9 or newer
- An [OpenAI API key](https://platform.openai.com/api-keys)

## Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/SonaliMB/Language-Translator.git
   cd Language-Translator
   ```

2. **Create a virtual environment (recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   Contents of `requirements.txt`:

   ```
   fastapi
   uvicorn
   openai
   python-dotenv
   pydantic
   ```

4. **Add your API key**

   Create a file named `.env` in the project folder:

   ```
   OPENAI_API_KEY=your-api-key-here
   ```
   Add `.env` to your `.gitignore` so your key is never pushed to GitHub:
   ```
   .env
   venv/
   __pycache__/
   ```

## Running the app

1. **Start the backend**

   ```bash
   uvicorn fastapi_translator:app --reload
   ```

   The API runs at `http://localhost:8000`. Interactive API docs are available at `http://localhost:8000/docs`.

2. **Open the frontend**

   Open `index.html` in your browser. If your backend runs on a different host or port, change `BACKEND_URL` at the top of the script in `index.html`.

3. Pick your languages, type or paste text, and click **Translate**.

## API reference

### `POST /translate/`

Translates text.

**Request body (JSON)**

| Field             | Type   | Required | Default   | Description                                         |
|-------------------|--------|----------|-----------|-----------------------------------------------------|
| `input_str`       | string | yes      |           | Text to translate                                   |
| `source_language` | string | no       | `English` | A supported language name, or `Auto-detect`         |
| `target_language` | string | no       | `German`  | A supported language name                           |

**Example**

```bash
curl -X POST http://localhost:8000/translate/ \
  -H "Content-Type: application/json" \
  -d '{"input_str": "Good morning", "source_language": "English", "target_language": "French"}'
```

**Response**

```json
{ "translated_text": "Bonjour" }
```

**Errors**

| Status | Meaning                                                         |
|--------|-----------------------------------------------------------------|
| 400    | Unsupported language, or source and target languages are equal  |
| 422    | Request body is missing a required field or is malformed        |
| 500    | The translation request to OpenAI failed                        |

### `GET /languages/`

Returns the supported languages as `{"source": [...], "target": [...]}`. The source list starts with `Auto-detect`.

## Supported languages

Arabic, Bengali, Chinese (Simplified), Chinese (Traditional), Czech, Dutch, English, Filipino, French, German, Greek, Hebrew, Hindi, Hungarian, Indonesian, Italian, Japanese, Korean, Malay, Marathi, Persian, Polish, Portuguese, Romanian, Russian, Spanish, Swahili, Swedish, Tamil, Telugu, Thai, Turkish, Ukrainian, Urdu, Vietnamese.

To add a language, add it to both `LANGUAGES` in `index.html` and `SUPPORTED_LANGUAGES` in `fastapi_translator.py`.

## Configuration notes

- **Model:** the backend uses `gpt-3.5-turbo`. Change the `model` argument in `translate_text()` to use a different model.
- **CORS:** the backend currently allows requests from any origin (`allow_origins=["*"]`) for easy local development. Restrict this to your frontend's origin before deploying.
- **Costs:** every translation is a paid OpenAI API call. Keep your key private and monitor your usage.

## Tech stack

- Frontend: HTML, CSS, vanilla JavaScript
- Backend: [FastAPI](https://fastapi.tiangolo.com/), [Pydantic](https://docs.pydantic.dev/), [Uvicorn](https://www.uvicorn.org/)
- Translation: [OpenAI API](https://platform.openai.com/docs)

## License

Add a license of your choice (for example, MIT) as a `LICENSE` file in the repository.
