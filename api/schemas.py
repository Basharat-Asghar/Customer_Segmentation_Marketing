from pydantic import BaseModel, Field, field_validator, computed_field
from typing import Literal, Annotated

class StudentInput(BaseModel):
    minutes_watched: int = Field(..., ge=0, description='Total minutes watched by student on platform', examples=[1500], strict=True)
    clv: float = Field(..., ge=0, description='Customer Lifetime value of student', examples=[167.5], strict=True)
    region: Annotated[Literal['0','1','2'], Field(..., description='region from where student resides')]
    channel: Annotated[Literal['1','2','3','4','5','6','7','8'], Field(..., description='Acquisition chaneel from where students enrolls on platform')]

    @field_validator("minutes_watched", "region", "channel")
    @classmethod
    def minutes_watched_must_be_finite(cls, value: int) -> int:
        import math
        if math.isnan(value) or math.isinf(value):
            raise ValueError("Value must be a finite number.")
        
        return value
    
    @field_validator("clv")
    @classmethod
    def minutes_watched_must_be_finite(cls, value: float) -> float:
        import math
        if math.isnan(value) or math.isinf(value):
            raise ValueError("Value must be a finite number.")
        
        return value
    
    @computed_field
    @property
    def is_free_user(self) -> int:
        if self.clv == 0:
            return 1
        else:
            return 0

    @computed_field
    @property
    def is_dormant_user(self) -> int:
        if self.minutes_watched == 0:
            return 1
        else:
            return 0
        
class PredictionResponse(BaseModel):
    """Single-student prediction response."""
    minutes_watched: float = Field(..., description="Echo of input minutes_watched")
    clv: float = Field(..., description="Echo of input CLV")
    cluster: int = Field(..., description="Cluster index (0, 1, or 2)")
    persona: str = Field(..., description="Human-readable persona name")
    