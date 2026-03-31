import json
import os
from groq import Groq


class DDRGenerator:

    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)

        # ✅ FIXED PATH HANDLING
        base_dir = os.path.dirname(os.path.abspath(__file__))
        prompt_path = os.path.join(base_dir, "prompt_template.txt")

        with open(prompt_path, "r", encoding="utf-8") as f:
            self.prompt_template = f.read()

    def generate(self, merged_json_path, output_path):

        with open(merged_json_path) as f:
            data = json.load(f)

        prompt = self.prompt_template.replace("{data}", json.dumps(data, indent=2))

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        output_text = response.choices[0].message.content

        try:
            start = output_text.find("{")
            end = output_text.rfind("}") + 1
            clean_json = output_text[start:end]

            parsed = json.loads(clean_json)

        except Exception as e:
            print("❌ JSON parsing failed:", e)
            parsed = {"error": output_text}

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "w") as f:
            json.dump(parsed, f, indent=4)

        print("✅ DDR Generated")

        return parsed
