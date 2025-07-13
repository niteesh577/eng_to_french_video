import logging
from config import settings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

logger = logging.getLogger(__name__)

def translate_text(text: str, target_lang: str = "fr") -> str:
    """
    Translate text to French using LangChain + Gemini 2.0 Flash.
    Returns translated text (str).
    """
    try:
        if not settings.GOOGLE_API_KEY:
            logger.error("GOOGLE_API_KEY not set in environment.")
            return ""
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=settings.GOOGLE_API_KEY)
        prompt = f"Translate the following text to {target_lang} (French):\n{text}"
        response = llm([HumanMessage(content=prompt)])
        translated = response.content.strip()
        logger.info("Translation complete. Length: %d chars", len(translated))
        return translated
    except Exception as e:
        logger.error(f"Translation failed: {e}")
        return "" 