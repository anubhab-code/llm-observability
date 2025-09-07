from wrapper import LLMWrapper
from vector_store import VectorStore
from rule_classifier import rule_classify

class HybridClassifier:
    def __init__(self, provider="openai", similarity_threshold=0.85):
        self.llm = LLMWrapper(provider=provider)
        self.store = VectorStore()
        self.similarity_threshold = similarity_threshold

    def classify(self, prompt: str) -> str:
        cached_category, sim = self.store.search(prompt)
        if cached_category and sim >= self.similarity_threshold:
            print(f"⚡ Semantic cache hit (sim={sim:.2f}): {cached_category}")
            return cached_category

        classification_prompt = f"""
        Classify the following prompt into one of these categories:
        - Summarization
        - Q&A
        - Creative Writing
        - Coding/Technical
        - Other

        Prompt: "{prompt}"
        Just return the category name.
        """
        try:
            result = self.llm.generate(classification_prompt)
            category = result["response"].strip()
            self.store.add(prompt, category)
            print(f"🤖 LLM classified: {category}")
            return category
        except Exception:
            category = rule_classify(prompt)
            print(f"🛟 Fallback (rule-based): {category}")
            return category
