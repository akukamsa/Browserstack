import requests

class Translator:
    def __init__(self, api_key):
        self.api_key = api_key
        self.endpoint = "https://google-translate113.p.rapidapi.com/api/v1/translator/text"
        self.headers = {
            "Content-Type": "application/json",
            "x-rapidapi-host": "google-translate113.p.rapidapi.com",
            "x-rapidapi-key": self.api_key
        }

    def translate_text(self, text, source_lang="auto", target_lang="en"):
        payload = {
            "from": source_lang,
            "to": target_lang,
            "text": text
        }

        try:
            response = requests.post(self.endpoint, json=payload, headers=self.headers)
            response.raise_for_status()
            return response.json().get("trans", "")
        except Exception as e:
            print(f"Translation failed for '{text}': {e}")
            return ""
        
   