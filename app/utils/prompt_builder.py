from typing import List
from app.schemas.answer_schemas import RetrievedDocument

def build_rag_prompt(query: str, docs: List[RetrievedDocument]) -> str:
    context_text = "\n\n".join(
        [f"Document {i+1}:\n{doc.content}" for i, doc in enumerate(docs)]
    )
    return f"""
You are a helpful assistant. 
Answer the following question based on the provided context. 
If the answer is not in the context, say "I don't know."

Context:
{context_text}

Question: {query}

Answer:
"""
