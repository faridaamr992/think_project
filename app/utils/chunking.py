from typing import List


def simple_chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size

        if end < text_length:
            last_period = text[start:end].rfind('.')
            last_newline = text[start:end].rfind('\n')
            break_point = max(last_period, last_newline)

            if break_point != -1:
                end = start + break_point + 1
        else:
            end = text_length

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        if end <= start:
            # Prevent infinite loop
            break

        start = end - overlap if end - overlap > start else end

    return chunks
