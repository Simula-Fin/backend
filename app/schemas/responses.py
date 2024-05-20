from datetime import date
from pydantic import BaseModel, ConfigDict, EmailStr, field_validator
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
    telephone: str
    monthly_income: float
    cpf: str
    birth_date: date 
    pix_key: str

    class Config:
        orm_mode = True


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


class UserLoansResponse(BaseResponse):
    amount: float
    interest_rate: float
    duration_months: int
    monthly_payment: float
    bank_name: str
    created_at: str

class UserConsortiumsResponse(BaseResponse):
    amount: float
    interest_rate: float
    duration_months: int
    monthly_payment: float
    bank_name: str
    created_at: str

class UserFinancingsResponse(BaseResponse):
    amount: float
    interest_rate: float
    duration_months: int
    monthly_payment: float
    bank_name: str
    created_at: str

     