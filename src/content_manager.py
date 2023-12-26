import torch
from transformers import BertTokenizer, BertForSequenceClassification
import asyncio
from concurrent.futures import ThreadPoolExecutor

class ContentManager:
    def __init__(self, model_path):
        self.tokenizer = BertTokenizer.from_pretrained(model_path)
        self.model = BertForSequenceClassification.from_pretrained(model_path)
        self.model.eval()
        self.executor = ThreadPoolExecutor(max_workers=1)

    def _predict(self, message):
        # Preprocess the message
        inputs = self.tokenizer.encode_plus(
            message,
            add_special_tokens=True,
            max_length=64,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )

        # Move tensors to the same device as the model
        inputs = {k: v.to(self.model.device) for k, v in inputs.items()}

        # Get model predictions
        with torch.no_grad():
            outputs = self.model(**inputs)

        # Interpret the model output
        prediction = torch.argmax(outputs.logits, dim=1).item()
        # Return the prediction
        return prediction

    async def decide(self, message):
        loop = asyncio.get_event_loop()
        try:
            # Run the synchronous model inference in an executor
            prediction = await loop.run_in_executor(self.executor, self._predict, message)
            return prediction
        except Exception as e:
            print(f"Error during model prediction: {e}")
            return None  # Or handle the error as needed

    