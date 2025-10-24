"""
Request data models/schemas
"""
from dataclasses import dataclass
from typing import Optional

@dataclass
class QueryRequest:
    """Query request model"""
    query: str
    top_k: Optional[int] = 5
    
    def validate(self):
        """Validate query request"""
        if not self.query or len(self.query.strip()) < 3:
            raise ValueError("Query must be at least 3 characters")
        if self.top_k < 1 or self.top_k > 10:
            raise ValueError("top_k must be between 1 and 10")
