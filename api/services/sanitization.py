import json
import re
from typing import Any, Dict

def sanitize_ai_response(raw_text: str) -> Dict[str, Any]:
    """
    Cleans the AI response by removing markdown blocks and parsing it into a JSON object.
    """
    # Regex to extract content inside ```json blocks if present
    match = re.search(r"```json\s*(.*?)\s*```", raw_text, re.DOTALL)
    clean_text = match.group(1) if match else raw_text.strip("`").strip()

    try:
        return json.loads(clean_text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON from AI response: {str(e)}")