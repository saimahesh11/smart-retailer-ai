

from deep_translator import GoogleTranslator

LANGUAGES = {
    "English": "en",
    "Telugu": "te",
    "Hindi": "hi",
    "Tamil": "ta",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Bengali": "bn",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Punjabi": "pa",
}

def translate_text(text, target_language):
    """
    Translate text into the selected language.
    """

    if target_language == "en":
        return text

    try:
        return GoogleTranslator(
            source="auto",
            target=target_language
        ).translate(text)

    except Exception as e:
        print(f"Translation error: {e}")
        return text