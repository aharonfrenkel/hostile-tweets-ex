from app.fetcher import Fetcher
from app.processor import Processor


class Manager:
    def __init__(self):
        self.fetcher = Fetcher()
        raw_data = self.fetcher.get_documents()
        self.processor = Processor(raw_data)
        self.processor.process_all()

    def get_process_data(self):
        response = []

        for _, row in self.processor.data.iterrows():
            record = {
                "id": str(row.get("TweetID", '')),
                "original_text": row.get("Text", ''),
                "rarest_word": row.get("rarest_word", ''),
                "sentiment": row.get("sentiment", "neutral"),
                "weapons_detected": row.get("weapons_detected", '')
            }
            response.append(record)

        return response