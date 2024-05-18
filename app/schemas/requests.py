from pydantic import BaseModel, EmailStr


class BaseRequest(BaseModel):
    # may define additional fields or config shared across requests
    pass


class RefreshTokenRequest(BaseRequest):
    refresh_token: str


class UserUpdatePasswordRequest(BaseRequest):
    password: str


class UserCreateRequest(BaseRequest):
    email: EmailStr
    password: str
    name: str
    telephone: str
    monthly_income: float
    cpf: str
    birth_date: str
    pix_key: str
    
class LoanSimulationRequest(BaseRequest):
    amount: float
    duration_months: int
    tax: float


