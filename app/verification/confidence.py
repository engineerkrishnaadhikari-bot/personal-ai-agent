class ConfidenceEngine:
    """Calculate a simple confidence score from verification signals."""

    def calculate(
        self,
        verification_score: float,
        memory_confidence: float = 0.0,
        tool_verified: bool = False,
    ) -> float:
        values = [verification_score]

        if memory_confidence > 0:
            values.append(memory_confidence)

        score = sum(values) / len(values)

        if tool_verified:
            score = min(1.0, score + 0.1)

        return round(max(0.0, min(1.0, score)), 4)
