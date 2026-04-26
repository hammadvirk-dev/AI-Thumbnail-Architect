```python
import os
import json
import requests
import time

# --- Configuration ---
# The API key is provided by the environment at runtime.
API_KEY = ""
MODEL_NAME = "gemini-2.5-flash-preview-09-2025"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={API_KEY}"

class ThumbnailArchitect:
    """
    A Python tool to transform YouTube video titles into high-CTR 
    thumbnail concepts using generative AI.
    """
    
    def __init__(self):
        self.system_instruction = (
            "You are an expert YouTube Creative Director and Graphic Designer. "
            "Your task is to analyze a video title and provide 3 distinct thumbnail concepts: "
            "1. Emotional (Focus on human connection/reaction), "
            "2. Minimalist (Clean, bold, high-contrast), "
            "3. Action/Curiosity (Fast-paced or 'The Loop' style). "
            "For each concept, provide: Visual Elements, Text Overlay, and a detailed "
            "AI Image Generation Prompt (for Midjourney/DALL-E)."
        )

    def generate_concepts(self, video_title):
        """
        Calls the Gemini API with exponential backoff for reliability.
        """
        payload = {
            "contents": [{
                "parts": [{
                    "text": f"Video Title: '{video_title}'. Generate 3 thumbnail concepts with visual elements, text overlays, and AI image prompts."
                }]
            }],
            "systemInstruction": {
                "parts": [{ "text": self.system_instruction }]
            },
            "generationConfig": {
                "responseMimeType": "application/json",
                "responseSchema": {
                    "type": "OBJECT",
                    "properties": {
                        "concepts": {
                            "type": "ARRAY",
                            "items": {
                                "type": "OBJECT",
                                "properties": {
                                    "style": { "type": "STRING" },
                                    "visual_elements": { "type": "STRING" },
                                    "text_overlay": { "type": "STRING" },
                                    "ai_prompt": { "type": "STRING" }
                                }
                            }
                        }
                    }
                }
            }
        }

        # Exponential Backoff Implementation
        retries = 5
        for i in range(retries):
            try:
                response = requests.post(API_URL, json=payload)
                if response.status_code == 200:
                    result = response.json()
                    return json.loads(result['candidates'][0]['content']['parts'][0]['text'])
                elif response.status_code == 429:
                    time.sleep(2 ** i)
                else:
                    break
            except Exception as e:
                time.sleep(2 ** i)
        
        return {"error": "Failed to generate concepts after multiple attempts."}

def main():
    print("="*50)
    print("🎨 AI-Thumbnail-Architect: Master Your YouTube CTR")
    print("="*50)
    
    title = input("\n🎥 Enter your Video Title: ")
    print("\n[Thinking] Architecting your viral concepts...")
    
    architect = ThumbnailArchitect()
    data = architect.generate_concepts(title)
    
    if "error" in data:
        print(f"\n❌ Error: {data['error']}")
        return

    for idx, concept in enumerate(data.get("concepts", []), 1):
        print(f"\n--- Concept #{idx}: {concept['style']} ---")
        print(f"👀 Visuals: {concept['visual_elements']}")
        print(f"💬 Text: {concept['text_overlay']}")
        print(f"🤖 AI Image Prompt: {concept['ai_prompt']}")
        print("-" * 30)

    print("\n✅ Concepts generated successfully! Use the prompts in Midjourney, DALL-E, or Leonardo.ai.")

if __name__ == "__main__":
    main()

```
                  
