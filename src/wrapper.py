import time
import random
import openai

class LLMWrapper:
    def __init__(self, provider="dummy"):
        self.provider = provider

    def generate(self, prompt):
        start = time.time()

        if self.provider == "dummy":
            time.sleep(0.1)
            response = f"Dummy response for: {prompt}"
            tokens = len(prompt.split())
            cost = tokens * 0.000001
            latency = (time.time() - start) * 1000
            return {
                "response": response,
                "latency_ms": latency,
                "total_tokens": tokens,
                "cost_usd": cost,
                "model": "dummy-1.0",
                "provider": "dummy"
            }

        elif self.provider == "openai":
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            latency = (time.time() - start) * 1000
            tokens = response["usage"]["total_tokens"]
            cost = tokens * 0.000002
            return {
                "response": response["choices"][0]["message"]["content"],
                "latency_ms": latency,
                "total_tokens": tokens,
                "cost_usd": cost,
                "model": response["model"],
                "provider": "openai"
            }

        else:
            raise ValueError("Unsupported provider")
