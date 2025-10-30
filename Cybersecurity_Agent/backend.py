import os
from typing import Optional

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI


_MODEL_NAME = "gemini-2.5-flash-lite"


def _load_api_key_from_env() -> str:
    """Load the Google API key from .env or environment variables.

    Returns:
        str: The API key string.

    Raises:
        RuntimeError: If the API key is missing.
    """
    # Load variables from a local .env file if present
    load_dotenv(override=False)
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Missing GOOGLE_API_KEY. Please create a .env with GOOGLE_API_KEY=your_api_key_here"
        )
    return api_key


def _build_chain(temperature: float = 0.2, max_output_tokens: int = 512):
    """Construct and return a simple LangChain pipeline for cybersecurity Q&A.

    Args:
        temperature: Sampling temperature for the model.
        max_output_tokens: Maximum tokens to generate.
    """
    _load_api_key_from_env()

    llm = ChatGoogleGenerativeAI(
        model=_MODEL_NAME,
        temperature=temperature,
        max_output_tokens=max_output_tokens,
    )

    system_instructions = (
        "You are a concise cybersecurity assistant."
        " Answer in simple, beginner-friendly language."
        " Focus on core definitions, common signs, and practical steps."
        " Keep responses short (2-6 sentences)."
        " If asked about unsafe actions, refuse and explain safer alternatives."
        " Topics include phishing, DDoS, SIEM, ransomware, firewalls, MFA, and basic best practices."
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_instructions),
            (
                "human",
                "Question: {question}\n"
                "Provide a clear, direct answer. If relevant, include 2-3 bullet best practices.",
            ),
        ]
    )

    chain = prompt | llm | StrOutputParser()
    return chain


_DEFAULT_TEMPERATURE = 0.2
_DEFAULT_MAX_TOKENS = 512


def get_cyber_answer(
    question: str,
    temperature: Optional[float] = None,
    max_output_tokens: Optional[int] = None,
) -> str:
    """Return a concise answer to a basic cybersecurity question.

    Args:
        question: User question about cybersecurity.
        temperature: Optional model temperature override from frontend.
        max_output_tokens: Optional max tokens override from frontend.

    Returns:
        Model answer as plain text.
    """
    if question is None:
        return "Please enter a question."

    cleaned = question.strip()
    if not cleaned:
        return "Please enter a question."

    temp = _DEFAULT_TEMPERATURE if temperature is None else float(temperature)
    max_tok = _DEFAULT_MAX_TOKENS if max_output_tokens is None else int(max_output_tokens)
    chain = _build_chain(temperature=temp, max_output_tokens=max_tok)
    try:
        return chain.invoke({"question": cleaned})
    except Exception as exc:  # Keep simple and beginner-friendly
        return (
            "Sorry, I couldn't process that right now. Please verify your API key and try again."
        )


if __name__ == "__main__":
    # Simple manual test
    print(get_cyber_answer("What is phishing and how can I avoid it?"))


