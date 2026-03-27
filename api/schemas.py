from pydantic import BaseModel, Field, field_validator, computed_field
from typing import Literal, Annotated, Optional

class StudentInput(BaseModel):
    minutes_watched: int = Field(..., ge=0, description='Total minutes watched by student on platform', examples=[1500], strict=True)
    clv: float = Field(..., ge=0, description='Customer Lifetime value of student', examples=[167.5], strict=True)
    # Make region and channel optional with defaults
    region: Annotated[Literal['0','1','2'], Field(default='0', description='region from where student resides (0=US/CA/UK/AU, 1=W. Europe, 2=Rest of World)')]
    channel: Annotated[Literal['1','2','3','4','5','6','7','8'], Field(default='1', description='Acquisition channel from where students enrolls on platform (1=Google, 2=Facebook, etc.)')]

    @field_validator("minutes_watched", "region", "channel")
    @classmethod
    def validate_finite_int(cls, value: int) -> int:
        import math
        if isinstance(value, str):
            value = int(value)
        if math.isnan(value) or math.isinf(value):
            raise ValueError("Value must be a finite number.")
        return value
    
    @field_validator("clv")
    @classmethod
    def validate_finite_float(cls, value: float) -> float:
        import math
        if math.isnan(value) or math.isinf(value):
            raise ValueError("Value must be a finite number.")
        return value
    
    @computed_field
    @property
    def is_free_user(self) -> int:
        return 1 if self.clv == 0 else 0

    @computed_field
    @property
    def is_dormant_user(self) -> int:
        return 1 if self.minutes_watched == 0 else 0

class BatchStudentInput(BaseModel):
    """
    Batch segment prediction request — up to 1,000 students per call.
 
    Example payload:
        {"students": [{"minutes_watched": 500, "clv": 119.0, "region": "0", "channel": "1"}, ...]}
    """
    students: list[StudentInput] = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="List of 1–1000 students to score.",
    )
        
class PredictionResponse(BaseModel):
    """Single-student prediction response."""
    minutes_watched: float = Field(..., description="Echo of input minutes_watched")
    clv: float = Field(..., description="Echo of input CLV")
    cluster: int = Field(..., description="Cluster index (0, 1, or 2)")
    persona: str = Field(..., description="Human-readable persona name")
    region: str = Field(..., description="Region name")
    channel: str = Field(..., description="Channel name")

class BatchPredictionResponse(BaseModel):
    """Batch prediction response."""
    predictions: list[PredictionResponse]
    total: int = Field(..., description="Total students scored")