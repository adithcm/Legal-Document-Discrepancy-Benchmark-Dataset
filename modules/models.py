from abc import ABC, abstractmethod
import os
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

############################################################################
# ABSTRACT MODEL
############################################################################ 
class Model(ABC):
    @abstractmethod
    def generate(self, prompt):
        pass
    
############################################################################
# GEMINI
############################################################################
class GeminiModel(Model):
    def __init__(self, api_keys):
        self.api_keys = api_keys
        self.key_index = 0
        self._set_key(self.api_keys[self.key_index])
    
    def _set_key(self, key):
        os.environ["GOOGLE_API_KEY"] = key
        genai.configure(api_key=key)
        self.model = genai.GenerativeModel("gemini-2.0-flash")

    def generate(self, prompt, max_retries=5):
        for attempt in range(max_retries):
            try:
                response = self.model.generate_content(prompt)
                return response.to_dict()["candidates"][0]["content"]["parts"][0]["text"]
            except ResourceExhausted:
                print(f"⚠️ API key {self.api_keys[self.key_index]} exhausted. Switching...")
                self.key_index = (self.key_index + 1) % len(self.api_keys)
                self._set_key(self.api_keys[self.key_index])
        print("❌ All keys exhausted or failed.")
        return ""

############################################################################
# SELF-VERIFICATION MODEL
############################################################################    
class SelfVerificationModel(Model):
    def __init__(self, model: Model):
        self.model = model

    def generate(self, prompt):

        failed = True

        while failed:
            print("💡 Asking questions")
            response = self.model.generate(prompt)
            is_model_sure_response = self.model.generate(
                f"You are a grader. Verify if the following response to the question is correct. If the answer is correct, say yes. Otherwise, say no.\nQuestion: {prompt}\nAnswer: {response}"
            )

            print("🤖 Model response:", response)
            print("🤓 Model sure response:", is_model_sure_response)

            if "yes" in is_model_sure_response.lower():
                print("✅ Model is sure about the answer.")
                failed = False
            else:
                print("❌ Model is not sure. Retrying...")


        return response