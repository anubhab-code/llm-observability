import datetime
from models import Session, Interaction
from llm_classifier import HybridClassifier

classifier = HybridClassifier(provider="openai")

def log_interaction(prompt, result, status="success", feedback=None):
    category = classifier.classify(prompt)
    session = Session()
    interaction = Interaction(
        timestamp=datetime.datetime.utcnow(),
        prompt=prompt,
        response=result.get("response", ""),
        latency_ms=result.get("latency_ms", 0),
        total_tokens=result.get("total_tokens", 0),
        cost_usd=result.get("cost_usd", 0),
        model=result.get("model", ""),
        provider=result.get("provider", ""),
        status=status,
        feedback=feedback,
        category=category
    )
    session.add(interaction)
    session.commit()
    session.close()
    return interaction
