from app.features.pipeline import process_features, calculate_features


class Pipeline:
    def __init__(self, storage):
        self.storage = storage

    def run(self, symbols):
        # Minimal implementation to satisfy test requirements
        pass
