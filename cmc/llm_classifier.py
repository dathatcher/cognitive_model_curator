import json
import os
import re
from openai import OpenAI
from pathlib import Path

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ensure_not_defined(model: dict) -> None:
    if "NOT_DEFINED" not in model:
        model["NOT_DEFINED"] = []

def classify_entity_with_llm(entity: dict, distinctions: list, context: str = "IT Organization") -> dict:
    distinctions_str = ", ".join(distinctions)
    prompt = f"""You are a cognitive systems analyst with expert knowledge of enterprise IT systems and subsystems. 
You apply integrated reasoning based on Systems Thinking (DSRP), Chaos Theory, Karma (ethical cause and effect), 
and Complex Adaptive Systems to evaluate how each data object fits into the organization.

System Context: {context}
Available Top-Level Distinctions (classifications): {distinctions_str}

Your task:
- Analyze the object from all systemic dimensions (infrastructure, applications, tools, people, processes, governance, external dependencies, security, etc.)
- Consider both technical and human dynamics
- Return your answer as a JSON object with two keys:
  - classification: one of the distinctions or 'NOT_DEFINED'
  - reasoning: an expert-level rationale that includes how the classification aligns with the system context and governing frameworks

Here is the data object to classify:
{json.dumps(entity, indent=2)}

Respond ONLY with the raw JSON object, no explanation or markdown.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a systems thinking AI classification assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        raw_response = response.choices[0].message.content.strip()
        print(f"🧠 Raw LLM response: {raw_response}")  # Debug log

        # Extract JSON object using regex
        match = re.search(r'{.*}', raw_response, re.DOTALL)
        json_str = match.group(0) if match else raw_response

        # Sanitize potential formatting issues
        json_str = json_str.replace("“", '"').replace("”", '"').replace("’", "'")

        return json.loads(json_str)

    except Exception as e:
        return {
            "classification": "NOT_DEFINED",
            "reasoning": f"Failed to parse LLM output. Defaulting to NOT_DEFINED. Error: {str(e)}"
        }

def load_model(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Mental model not found at {path}")
    with open(path) as f:
        return json.load(f)

def save_model(path: Path, model: dict) -> None:
    with open(path, "w") as f:
        json.dump(model, f, indent=2)

def add_entity_to_model(entity: dict, model_path: str, context: str = "IT Organization"):
    model_path = Path(model_path)
    model = load_model(model_path)
    ensure_not_defined(model)
    distinctions = [key for key in model.keys() if key != "NOT_DEFINED"]

    classification_result = classify_entity_with_llm(entity, distinctions, context)
    classification = classification_result.get("classification", "NOT_DEFINED")
    reasoning = classification_result.get("reasoning", "No reasoning provided.")

    annotated_entry = {
        "data": entity,
        "llm_reasoning": reasoning
    }

    model.setdefault(classification, []).append(annotated_entry)
    save_model(model_path, model)
    print(f"✅ Entity classified as '{classification}' and saved.")
