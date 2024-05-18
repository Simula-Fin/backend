from fastapi import APIRouter, Depends, status
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.core.security.password import get_password_hash
from app.models import User, LoanSimulation, ConsortiumSimulation, FinancingSimulation
from app.schemas.requests import UserUpdatePasswordRequest, LoanSimulationRequest, ConsortiumSimulationRequest, FinancingSimulationRequest
from app.schemas.responses import LoanSimulationResponse
from app.services.simulations import SimulationCRUD

router = APIRouter()

@router.post("/loan-simulation/", response_model=LoanSimulationResponse, description="Create a new loan simulation", status_code=status.HTTP_201_CREATED)
async def create_loan_simulation(
    loan_simulation_in: LoanSimulationRequest,
    current_user: User = Depends(deps.get_current_user),
    db: AsyncSession = Depends(deps.get_session)
)-> LoanSimulationResponse:

    return await SimulationCRUD.create_loan_simulation(db, loan_simulation_in, current_user)
