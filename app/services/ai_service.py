import os

USE_LLM = False  # 🔥 toggle later

def rule_based_analysis(text: str) -> dict:
    text = text.lower()

    category_map = {
        "technical": ["internet", "wifi", "network", "server"],
        "billing": ["fee", "payment", "refund", "money"],
        "harassment": ["harassment", "abuse", "threat"],
        "infrastructure": ["water", "electricity", "hostel", "room"]
    }

    priority_map = {
        "high": ["urgent", "immediately", "danger", "exam", "threat"],
        "medium": ["not working", "down", "failed"]
    }

    category = "general"
    for key, words in category_map.items():
        if any(w in text for w in words):
            category = key
            break

    priority = "low"
    for key, words in priority_map.items():
        if any(w in text for w in words):
            priority = key
            break

    return {
        "category": category,
        "priority": priority,
        "confidence": 0.65
    }


def llm_based_analysis(text: str) -> dict:
    """
    Placeholder for OpenAI / HuggingFace / Azure / Gemini
    """
    return {
        "category": "general",
        "priority": "medium",
        "confidence": 0.90
    }


def analyze_complaint(text: str) -> dict:
    if USE_LLM:
        return llm_based_analysis(text)
    return rule_based_analysis(text)
