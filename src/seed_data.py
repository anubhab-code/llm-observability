import datetime
import random
from models import Session, Interaction

session = Session()

prompts = [
    "Summarize the history of data engineering",
    "Write a haiku about AI",
    "How do I optimize a SQL query?",
    "What is the capital of France?",
    "Generate a funny story about a penguin",
    "Explain quantum computing in simple terms",
    "List top 5 Python libraries for data science",
    "Translate 'Hello World' to Spanish",
    "Draft an email to request a meeting",
    "Describe the process of photosynthesis",
    "Give me a recipe for chocolate cake",
    "What are the benefits of meditation?",
    "Write a poem about autumn",
    "How to fix a flat tire?",
    "Tell a joke about computers",
    "Summarize the plot of Hamlet",
    "What is the Pythagorean theorem?",
    "Generate a motivational quote",
    "Explain blockchain technology",
    "List famous paintings by Van Gogh"
]

responses = [
    "Data engineering evolved from ETL pipelines to modern cloud-based solutions.",
    "Neural nets awake / Whispering in silent code / Dawn of thought in steel",
    "Use indexes, avoid SELECT *, and analyze execution plans.",
    "The capital of France is Paris.",
    "Once upon a time, a penguin slipped into a tech conference...",
    "Quantum computing uses qubits to perform complex calculations.",
    "Popular libraries include pandas, numpy, scikit-learn, matplotlib, and seaborn.",
    "'Hola Mundo' is 'Hello World' in Spanish.",
    "Dear team, I would like to request a meeting to discuss project updates.",
    "Photosynthesis converts sunlight into energy for plants.",
    "Mix flour, cocoa, sugar, eggs, and bake at 350°F for 30 minutes.",
    "Meditation improves focus and reduces stress.",
    "Leaves fall gently / Crisp air whispers through the trees / Autumn's gold arrives",
    "Remove the wheel, patch the hole, and inflate the tire.",
    "Why did the computer get cold? It left its Windows open.",
    "Hamlet is a tragedy about revenge and madness.",
    "a² + b² = c² describes the sides of a right triangle.",
    "Believe in yourself and all that you are.",
    "Blockchain is a decentralized ledger for digital transactions.",
    "Starry Night, Sunflowers, and The Potato Eaters are by Van Gogh."
]

models = ["gpt-3.5-turbo", "gpt-4", "llama-2", "mistral-7b", "gemini-pro"]
providers = ["openai", "google", "meta", "mistral", "anthropic"]
statuses = ["success", "error", "timeout", "rate_limited"]
categories = [
    "Summarization", "Creative Writing", "Coding/Technical", "Q&A",
    "Translation", "Email", "Science", "Recipe", "Wellness", "Poetry",
    "How-To", "Joke", "Literature", "Math", "Motivation", "Technology", "Art"
]
feedback_options = [None, "👍", "👎", "⭐", "Needs improvement", "Excellent", "Too slow"]

sample_data = []
for i in range(100):
    prompt = random.choice(prompts)
    response = random.choice(responses)
    latency_ms = round(random.uniform(50, 300), 2)
    total_tokens = random.randint(10, 200)
    cost_usd = round(total_tokens * random.uniform(0.00001, 0.0002), 5)
    model = random.choice(models)
    provider = random.choice(providers)
    status = random.choice(statuses)
    feedback = random.choice(feedback_options)
    category = random.choice(categories)
    timestamp = datetime.datetime.utcnow() - datetime.timedelta(minutes=random.randint(0, 10000))

    # Simulate hallucination: 15% chance, more likely for certain categories/models
    hallucination = random.random() < (
        0.15 if category in ["Creative Writing", "Joke", "Motivation", "Art"] or model in ["llama-2", "mistral-7b"] else 0.07
    )

    # Simulate similarity score: lower if hallucination, higher otherwise
    similarity_score = round(random.uniform(0.2, 0.7), 2) if hallucination else round(random.uniform(0.7, 1.0), 2)

    interaction = Interaction(
        timestamp=timestamp,
        prompt=prompt,
        response=response,
        latency_ms=latency_ms,
        total_tokens=total_tokens,
        cost_usd=cost_usd,
        model=model,
        provider=provider,
        status=status,
        feedback=feedback,
        category=category,
        hallucination=hallucination,
        similarity_score=similarity_score
    )
    sample_data.append(interaction)

session.add_all(sample_data)
session.commit()
session.close()

print("✅ 100 sample interactions inserted!")