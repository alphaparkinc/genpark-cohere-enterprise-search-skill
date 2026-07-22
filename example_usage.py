from client import CohereEnterpriseSearchClient
client = CohereEnterpriseSearchClient()
result = client.search(
    query="What is our refund policy for enterprise customers?",
    documents=[
        {"title": "Enterprise SLA", "text": "Enterprise customers receive dedicated SLA with 99.99% uptime guarantee and priority support."},
        {"title": "Billing FAQ", "text": "Refund policy: Enterprise customers may request refunds within 30 days. Contact enterprise-billing@company.com."},
        {"title": "Product Roadmap", "text": "Q3 2026 roadmap includes multimodal features and expanded API rate limits."},
    ],
    top_k=2
)
print(f"Answer: {result['generated_answer'][:120]}")
for r in result["ranked_results"]:
    print(f"  Rank {r['rank']}: {r['title']} (score: {r['embed_score']})")
