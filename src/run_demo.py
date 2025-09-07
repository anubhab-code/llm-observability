from logger import log_interaction
from wrapper import LLMWrapper

# Choose provider: "dummy" or "openai"
provider = "dummy"   # switch to "openai" if you have an API key
llm = LLMWrapper(provider=provider)

prompt = "Write a haiku about data pipelines"

try:
    result = llm.generate(prompt)
    log_interaction(prompt, result, status="success")

    print("✅ Response:", result["response"])
    print(f"Latency: {result['latency_ms']:.2f} ms | Tokens: {result['total_tokens']} | Cost: ${result['cost_usd']:.4f}")

except Exception as e:
    error_result = {
        "response": str(e),
        "latency_ms": 0,
        "total_tokens": 0,
        "cost_usd": 0,
        "model": "unknown",
        "provider": provider
    }
    log_interaction(prompt, error_result, status="failed")
    print("❌ Error:", str(e))
