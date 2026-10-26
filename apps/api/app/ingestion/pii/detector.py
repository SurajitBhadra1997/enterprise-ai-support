from presidio_analyzer import AnalyzerEngine
from app.ingestion.schemas import PIIDetectionResult


class PIIDetector:

    def __init__(self):
        self.analyzer = AnalyzerEngine()

    def detect(self, text: str) -> PIIDetectionResult:
        analysis_results = self.analyzer.analyze(text, language="en")
        pii_lists = []

        for result in analysis_results:
            if result.score > 0.85:
                pii_lists.append(result.entity_type)

        if len(pii_lists) > 0:
            return PIIDetectionResult(
                contains_pii=True, detected_categories=pii_lists, requires_review=True
            )
        return PIIDetectionResult(
              contains_pii=False, detected_categories=[], requires_review=False
        )

