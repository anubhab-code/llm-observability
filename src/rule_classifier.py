def rule_classify(prompt: str) -> str:
    p = prompt.lower()

    if "summarize" in p or "summary" in p:
        return "Summarization"
    elif "how" in p or "what" in p or "why" in p or "?" in p:
        return "Q&A"
    elif "poem" in p or "story" in p or "haiku" in p or "joke" in p:
        return "Creative Writing"
    elif "code" in p or "python" in p or "sql" in p or "debug" in p:
        return "Coding/Technical"
    else:
        return "Other"
