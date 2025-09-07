import streamlit as st
import pandas as pd
from models import Session, Interaction
import matplotlib.pyplot as plt

st.title("📊 LLM Observability Dashboard")

session = Session()
data = session.query(Interaction).all()
session.close()

df = pd.DataFrame([{
    "timestamp": d.timestamp,
    "prompt": d.prompt,
    "response": d.response,
    "latency_ms": d.latency_ms,
    "total_tokens": d.total_tokens,
    "cost_usd": d.cost_usd,
    "status": d.status,
    "model": d.model,
    "provider": d.provider,
    "feedback": getattr(d, "feedback", None),
    "hallucination": getattr(d, "hallucination", None),
    "similarity_score": getattr(d, "similarity_score", None),
    "category": getattr(d, "category", "Unknown")
} for d in data])

if not df.empty:
    filtered_df = df  # No filters applied for now

    st.subheader("Summary Statistics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Avg Latency (ms)", f"{filtered_df['latency_ms'].mean():.2f}")
    col2.metric("Total Cost (USD)", f"{filtered_df['cost_usd'].sum():.4f}")
    col3.metric("Success Rate", f"{(filtered_df['status']=='success').mean()*100:.1f}%")

    # 11. Prompt Search
    search_prompt = st.text_input("Search Prompt")
    if search_prompt:
        st.caption("Search for specific prompts to investigate individual interactions.")
        search_df = filtered_df[filtered_df["prompt"].str.contains(search_prompt, case=False)]
        st.dataframe(search_df)

    # 1. Prompt Categories
    st.subheader("Prompt Categories")
    st.caption("Shows the distribution of prompt categories. Use this to identify which types of queries are most common and focus optimization efforts accordingly.")
    category_counts = df["category"].value_counts()
    st.bar_chart(category_counts)

    # 2. Latency Over Time
    st.subheader("Latency Over Time")
    st.caption("Tracks latency trends. Spikes may indicate performance issues or bottlenecks at specific times.")
    st.line_chart(filtered_df.set_index("timestamp")["latency_ms"])

    # 3. Cost Over Time
    st.subheader("Cost Over Time")
    st.caption("Visualizes cost trends. Use this to monitor and control operational expenses over time.")
    st.line_chart(filtered_df.set_index("timestamp")["cost_usd"])

    # 4. Latency Distribution
    st.subheader("Latency Distribution")
    st.caption("Shows how latency is distributed. A long tail may indicate outliers or inconsistent performance.")
    st.bar_chart(filtered_df["latency_ms"].value_counts().sort_index())

    # 5. Token Distribution
    st.subheader("Token Distribution")
    st.caption("Displays the distribution of token usage. High token counts may correlate with higher costs or longer responses.")
    st.bar_chart(filtered_df["total_tokens"].value_counts().sort_index())

    # 6. Feedback Analysis
    if "feedback" in filtered_df.columns:
        st.subheader("Feedback")
        st.caption("Aggregates user feedback. Use this to gauge user satisfaction and identify areas for improvement.")
        feedback_counts = filtered_df["feedback"].value_counts()
        st.bar_chart(feedback_counts)

    # 7. Error Rate by Model
    st.subheader("Error Rate by Model")
    st.caption("Compares error rates across models. High error rates may indicate reliability issues with specific models.")
    error_rate_by_model = filtered_df.groupby("model")["status"].apply(lambda x: (x != "success").mean())
    st.bar_chart(error_rate_by_model)

    # 8. Cost per Provider
    st.subheader("Cost per Provider")
    st.caption("Shows which providers are most expensive. Use this to optimize provider selection for cost efficiency.")
    cost_per_provider = filtered_df.groupby("provider")["cost_usd"].sum()
    st.bar_chart(cost_per_provider)

    # 9. Latency by Category
    st.subheader("Avg Latency by Category")
    st.caption("Highlights which categories tend to be slower. Use this to target performance improvements for specific use cases.")
    latency_by_category = filtered_df.groupby("category")["latency_ms"].mean()
    st.bar_chart(latency_by_category)

    # 10. Success Rate by Provider
    st.subheader("Success Rate by Provider")
    st.caption("Compares reliability across providers. Use this to inform provider selection for critical workloads.")
    success_rate_by_provider = filtered_df.groupby("provider")["status"].apply(lambda x: (x == "success").mean())
    st.bar_chart(success_rate_by_provider)


    # 12. Hallucination Rate by Model (requires a 'hallucination' boolean column)
    if "hallucination" in filtered_df.columns:
        st.subheader("Hallucination Rate by Model")
        st.caption("Shows the percentage of outputs flagged as hallucinations for each model. High rates indicate models needing further investigation or retraining.")
        hallucination_rate_model = filtered_df.groupby("model")["hallucination"].mean()
        st.bar_chart(hallucination_rate_model)

    # 13. Hallucination Rate by Category
    if "hallucination" in filtered_df.columns:
        st.subheader("Hallucination Rate by Category")
        st.caption("Identifies which categories are most prone to hallucinations. Focus on high-risk categories for prompt engineering or model fine-tuning.")
        hallucination_rate_category = filtered_df.groupby("category")["hallucination"].mean()
        st.bar_chart(hallucination_rate_category)

    # 14. Prompt Complexity vs. Hallucination Rate
    if "hallucination" in filtered_df.columns:
        st.subheader("Prompt Complexity vs. Hallucination Rate")
        st.caption("Correlates prompt length (as a proxy for complexity) with hallucination frequency. Longer or more complex prompts may trigger more hallucinations.")
        filtered_df["prompt_length"] = filtered_df["prompt"].apply(lambda x: len(str(x).split()))
        st.scatter_chart(filtered_df, x="prompt_length", y="hallucination")

    # 15. Feedback Correlation with Hallucinations
    if "hallucination" in filtered_df.columns and "feedback" in filtered_df.columns:
        st.subheader("Feedback vs. Hallucination")
        st.caption("Compares user feedback with hallucination flags. Discrepancies may highlight gaps in detection or user perception.")
        feedback_hallucination = filtered_df.groupby("feedback")["hallucination"].mean()
        st.bar_chart(feedback_hallucination)

    # 16. Temporal Trends in Hallucinations
    if "hallucination" in filtered_df.columns:
        st.subheader("Hallucination Rate Over Time")
        st.caption("Tracks hallucination rates over time. Spikes may correlate with model updates or data drift.")
        time_hallucination = filtered_df.set_index("timestamp").resample("D")["hallucination"].mean()
        st.line_chart(time_hallucination)

    # 17. Token Usage in Hallucinated Responses
    if "hallucination" in filtered_df.columns:
        st.subheader("Token Usage in Hallucinated Responses")
        st.caption("Analyzes if hallucinated responses use more or fewer tokens than average. May reveal verbosity or brevity patterns.")
        avg_tokens_hallucinated = filtered_df[filtered_df["hallucination"] == True]["total_tokens"].mean()
        avg_tokens_non_hallucinated = filtered_df[filtered_df["hallucination"] == False]["total_tokens"].mean()
        st.metric("Avg Tokens (Hallucinated)", f"{avg_tokens_hallucinated:.2f}")
        st.metric("Avg Tokens (Non-Hallucinated)", f"{avg_tokens_non_hallucinated:.2f}")

    # 18. Success Rate vs. Hallucination Rate by Provider
    if "hallucination" in filtered_df.columns:
        st.subheader("Success vs. Hallucination Rate by Provider")
        st.caption("Compares reliability and hallucination rates across providers. Providers with high hallucination rates may need review.")
        provider_success = filtered_df.groupby("provider")["status"].apply(lambda x: (x == "success").mean())
        provider_hallucination = filtered_df.groupby("provider")["hallucination"].mean()
        st.dataframe(pd.DataFrame({
            "Success Rate": provider_success,
            "Hallucination Rate": provider_hallucination
        }))

    # # 19. Prompt-Response Similarity Score (requires a 'similarity_score' column)
    # if "similarity_score" in filtered_df.columns:
    #     st.subheader("Prompt-Response Similarity Score")
    #     st.caption("Low similarity scores may indicate off-topic or hallucinated responses. Use this to spot problematic interactions.")
    #     fig, ax = plt.subplots()
    #     ax.hist(filtered_df["similarity_score"].dropna(), bins=20, color='skyblue', edgecolor='black')
    #     ax.set_xlabel("Similarity Score")
    #     ax.set_ylabel("Count")
    #     st.pyplot(fig)