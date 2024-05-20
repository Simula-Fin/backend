from fastapi import APIRouter, Depends, status
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.api import deps
from app.models import User
from app.schemas.requests import LoanSimulationRequest, ConsortiumSimulationRequest, FinancingSimulationRequest
from app.schemas.responses import LoanSimulationResponse, ConsortiumSimulationResponse, FinancingSimulationResponse
from app.schemas.responses import UserLoansResponse, UserConsortiumsResponse, UserFinancingsResponse
from app.services.simulations import SimulationCRUD

router = APIRouter()

@router.post("/loan-simulation/", response_model=LoanSimulationResponse, description="Create a new loan simulation", status_code=status.HTTP_201_CREATED)
async def create_loan_simulation(
    loan_simulation_in: LoanSimulationRequest,
    current_user: User = Depends(deps.get_current_user),
    db: AsyncSession = Depends(deps.get_session)
)-> LoanSimulationResponse:
    return await SimulationCRUD.create_loan_simulation(db, loan_simulation_in, current_user)

@router.post("/consortium-simulation/", response_model=ConsortiumSimulationResponse, description="Create a new consortium simulation", status_code=status.HTTP_201_CREATED)
async def create_consortium_simulation(
    consortium_simulation_in: ConsortiumSimulationRequest,
    current_user: User = Depends(deps.get_current_user),
    db: AsyncSession = Depends(deps.get_session)
) -> ConsortiumSimulationResponse:
    return await SimulationCRUD.create_consortium_simulation(db, consortium_simulation_in, current_user)

@router.post("/financing-simulation/", response_model=FinancingSimulationResponse, description="Create a new financing simulation", status_code=status.HTTP_201_CREATED)
async def create_financing_simulation(
    financing_simulation_in: FinancingSimulationRequest,
    current_user: User = Depends(deps.get_current_user),
    db: AsyncSession = Depends(deps.get_session)
) -> FinancingSimulationResponse:
    return await SimulationCRUD.create_financing_simulation(db, financing_simulation_in, current_user)

@router.get("/loan-simulation/", response_model=List[UserLoansResponse], description="Get all loan simulations")
async def get_loan_simulations(
    current_user: User = Depends(deps.get_current_user),
    db: AsyncSession = Depends(deps.get_session)
) -> List[UserLoansResponse]:
    return await SimulationCRUD.get_loan_simulation(db, current_user)

@router.get("/consortium-simulation/", response_model=List[UserConsortiumsResponse], description="Get all consortium simulations")
async def get_consortium_simulations(
    current_user: User = Depends(deps.get_current_user),
    db: AsyncSession = Depends(deps.get_session)
) -> List[UserConsortiumsResponse]:
    return await SimulationCRUD.get_consortium_simulation(db, current_user)

@router.get("/financing-simulation/", response_model=List[UserFinancingsResponse], description="Get all financing simulations")
async def get_financing_simulations(
    current_user: User = Depends(deps.get_current_user),
    db: AsyncSession = Depends(deps.get_session)
) -> List[UserFinancingsResponse]:
    return await SimulationCRUD.get_financing_simulation(db, current_user)
