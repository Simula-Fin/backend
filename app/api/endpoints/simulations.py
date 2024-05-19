from fastapi import APIRouter, Depends, status
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.core.security.password import get_password_hash
from app.models import User
from app.schemas.requests import LoanSimulationRequest, ConsortiumSimulationRequest, FinancingSimulationRequest
from app.schemas.responses import LoanSimulationResponse, ConsortiumSimulationResponse, FinancingSimulationResponse
from app.services.simulations import SimulationCRUD

router = APIRouter()

@router.post("/loan-simulation/", response_model=LoanSimulationResponse, description="Create a new loan simulation", status_code=status.HTTP_201_CREATED)
async def create_loan_simulation(
    loan_simulation_in: LoanSimulationRequest,
    current_user: User = Depends(deps.get_current_user),
    db: AsyncSession = Depends(deps.get_session)
)-> LoanSimulationResponse:
    return await SimulationCRUD.create_loan_simulation(db, loan_simulation_in, current_user)

@router.post("/consortium-simulation/", response_model=ConsortiumSimulationResponse, description="Create a new consortium simulation")
async def create_consortium_simulation(
    consortium_simulation_in: ConsortiumSimulationRequest,
    current_user: User = Depends(deps.get_current_user),
    db: AsyncSession = Depends(deps.get_db)
) -> ConsortiumSimulationResponse:
    return await SimulationCRUD.create_consortium_simulation(db, consortium_simulation_in, current_user)

@router.post("/financing-simulation/", response_model=FinancingSimulationResponse, description="Create a new financing simulation")
async def create_financing_simulation(
    financing_simulation_in: FinancingSimulationRequest,
    current_user: User = Depends(deps.get_current_user),
    db: AsyncSession = Depends(deps.get_db)
) -> FinancingSimulationResponse:
    return await SimulationCRUD.create_financing_simulation(db, financing_simulation_in, current_user)
