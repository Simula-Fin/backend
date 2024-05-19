from pydantic import BaseModel, ConfigDict, EmailStr
from typing import List


class BaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class AccessTokenResponse(BaseResponse):
    token_type: str = "Bearer"
    access_token: str
    expires_at: int
    refresh_token: str
    refresh_token_expires_at: int


class UserResponse(BaseResponse):
    user_id: str
    email: EmailStr

class SimulationDetail(BaseResponse):
    parcela: float
    amortizacao: float
    juros: float
    saldo_devedor: float

class LoanSimulationResponse(BaseResponse):
    amount: float
    duration_months: int
    tax: float
    bank_name: str
    bank_location: str
    details: List[SimulationDetail]    

class ConsortiumSimulationResponse(BaseResponse):
    amount: float
    duration_months: int
    tax: float
    bank_name: str
    bank_location: str
    details: List[SimulationDetail]

class FinancingSimulationResponse(BaseResponse):
    amount: float
    duration_months: int
    tax: float
    bank_name: str
    bank_location: str
    details: List[SimulationDetail]    