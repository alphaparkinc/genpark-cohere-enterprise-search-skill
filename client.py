import math

class CohereEnterpriseSearchClient:
    def _embed_score(self, query: str, doc: str) -> float:
        """Simulate cosine similarity via shared term overlap."""
        q_words = set(query.lower().split())
        d_words = set(doc.lower().split())
        overlap = len(q_words & d_words)
        return round(overlap / math.sqrt(max(len(q_words) * len(d_words), 1)), 3)

    def search(self, query: str, documents: list, top_k: int = 3) -> dict:
        # Step 1: Embed + initial score (semantic similarity simulation)
        scored = []
        for i, doc in enumerate(documents):
            text = doc.get("text", "") if isinstance(doc, dict) else str(doc)
            title = doc.get("title", f"Document {i+1}") if isinstance(doc, dict) else f"Document {i+1}"
            score = self._embed_score(query, text)
            scored.append({"rank": 0, "title": title, "text": text[:100], "embed_score": score})

        # Step 2: Rerank (boost docs with query terms in first 20 words)
        for item in scored:
            first_20 = " ".join(item["text"].split()[:20]).lower()
            if any(w in first_20 for w in query.lower().split() if len(w) > 3):
                item["embed_score"] = min(item["embed_score"] + 0.15, 1.0)

        # Step 3: Sort and assign ranks
        scored.sort(key=lambda x: x["embed_score"], reverse=True)
        for i, item in enumerate(scored):
            item["rank"] = i + 1
        top_results = scored[:top_k]

        # Step 4: Command — generate grounded answer
        best_text = top_results[0]["text"] if top_results else "No relevant documents found."
        answer = f"[Command R+ | Grounded] Based on '{top_results[0]['title']}': {best_text}..." if top_results else "No answer available."
        return {"ranked_results": top_results, "generated_answer": answer}
