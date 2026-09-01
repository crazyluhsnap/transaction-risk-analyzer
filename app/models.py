from pydantic import BaseModel
from typing import List


class RiskAnalysisResponse(BaseModel):
    transaction_id:str
    risk_score:int
    risk_level:str
    reasons: List[str]

class TransactionResponse(BaseModel):
    transaction_id: str
    sender: str
    receiver: str
    amount: float
    country: str
    timestamp: str

class HealthResponse(BaseModel):
    status: str

class SummaryResponse(BaseModel):
    total_transactions: int
    high_risk: int
    medium_risk: int
    low_risk: int
