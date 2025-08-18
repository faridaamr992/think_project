from typing import List, Optional, Dict, Any
import re
from app.schemas.answer_schemas import RetrievedDocument
from langdetect import detect, DetectorFactory
from app.repository.prompt_repository import PromptRepository
# ---- Language detection ----
try:
    
    DetectorFactory.seed = 0
    def _detect_lang(text: str) -> str:
        try:
            return detect(text)
        except Exception:
            return "en"
except Exception:
    def _detect_lang(text: str) -> str:
        has_ar = bool(re.search(r"[\u0600-\u06FF]", text))
        has_en = bool(re.search(r"[A-Za-z]", text))
        if has_ar and not has_en:
            return "ar"
        if has_en and not has_ar:
            return "en"
        return "en"

async def build_rag_prompt(
    query: str,
    docs: List[RetrievedDocument],
    prompt_repo: PromptRepository,
    history: Optional[List[Dict[str, Any]]] = None,
    max_history: int = 10,
    template_id: str = "rag_prompt_v1"
) -> str:
    lang = _detect_lang(query)

    if lang == "ar":
        language_instruction = "أجب بالعربية."
        dont_know = "لا أعرف."
        user_label = "المستخدم"
        assistant_label = "المساعد"
    else:
        language_instruction = "Answer in English."
        dont_know = "I don't know."
        user_label = "User"
        assistant_label = "Assistant"

    # History
    history = history or []
    trimmed = history[-max_history:]
    history_text = "\n".join(
        f"{user_label if m.get('role') == 'user' else assistant_label}: {m.get('content','').strip()}"
        for m in trimmed if m and m.get("content")
    )
    history_block = f"\nConversation so far:\n{history_text}\n" if history_text else ""

    # Context
    context_text = "\n\n".join(
        f"Document {i+1}:\n{doc.content}"
        for i, doc in enumerate(docs)
        if getattr(doc, 'content', None)
    )

    # Fetch template from Mongo
    template = await prompt_repo.get_prompt_template(template_id)

    # Fill placeholders
    final_prompt = template.format(
        language_instruction=language_instruction,
        dont_know=dont_know,
        history_block=history_block,
        context_text=context_text,
        query=query,
    )

    # Optionally save the generated prompt for auditing
    await prompt_repo.save_generated_prompt(query, final_prompt)

    return final_prompt
