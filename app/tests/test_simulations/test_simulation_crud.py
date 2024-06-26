import pytest
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User, Bank, LoanSimulation, ConsortiumSimulation, FinancingSimulation
from app.services.simulations import SimulationCRUD
from app.schemas.requests import LoanSimulationRequest, ConsortiumSimulationRequest, FinancingSimulationRequest
from app.schemas.responses import LoanSimulationResponse, ConsortiumSimulationResponse, FinancingSimulationResponse, UserConsortiumsResponse
from fastapi import status
from httpx import AsyncClient
from sqlalchemy import func, select

@pytest.mark.asyncio
async def test_create_loan_simulation(session: AsyncSession, default_user: User, default_bank: Bank):
    # Dados de entrada para a simulação de empréstimo
    loan_simulation_in = LoanSimulationRequest(
        amount=10000.0,
        duration_months=12,
        tax=5.0,
        calculation_method="sac"
    )
    
    # Criando a simulação de empréstimo
    loan_simulation_response = await SimulationCRUD.create_loan_simulation(
        db=session,
        loan_simulation_in=loan_simulation_in,
        user=default_user
    )

    assert loan_simulation_response.amount == loan_simulation_in.amount
    assert loan_simulation_response.duration_months == loan_simulation_in.duration_months
    assert loan_simulation_response.tax == loan_simulation_in.tax

    # Verificando se a simulação foi criada no banco de dados
    db_simulation = await session.execute(
        select(LoanSimulation).where(LoanSimulation.user_id == default_user.user_id)
    )
    db_loan_simulation = db_simulation.scalars().first()

    assert db_loan_simulation is not None
    assert db_loan_simulation.amount == loan_simulation_in.amount
    assert db_loan_simulation.duration_months == loan_simulation_in.duration_months
    assert db_loan_simulation.interest_rate == loan_simulation_in.tax
    assert db_loan_simulation.bank_id is not None

@pytest.mark.asyncio
async def test_create_consortium_simulation(session: AsyncSession, default_user: User, default_bank: Bank ):
    # Dados de entrada para a simulação de consórcio
    consortium_simulation_in = ConsortiumSimulationRequest(
        amount=20000.0,
        duration_months=24,
        tax=6.0,
        calculation_method="price"
    )

    # Criando a simulação de consórcio
    consortium_simulation_response = await SimulationCRUD.create_consortium_simulation(
        db=session,
        consortium_simulation_in=consortium_simulation_in,
        user=default_user
    )

    # Verificando se a simulação foi criada no banco de dados
    db_simulation = await session.execute(
        select(ConsortiumSimulation).where(ConsortiumSimulation.user_id == default_user.user_id)
    )
    db_consortium_simulation = db_simulation.scalars().first()

    assert db_consortium_simulation is not None
    assert db_consortium_simulation.bank_id is not None

@pytest.mark.asyncio
async def test_create_financing_simulation(session: AsyncSession, default_user: User, default_bank: Bank):
    # Dados de entrada para a simulação de financiamento
    financing_simulation_in = FinancingSimulationRequest(
        amount=30000.0,
        duration_months=36,
        tax=7.5,
        calculation_method="sac"
    )

    # Criando a simulação de financiamento
    financing_simulation_response = await SimulationCRUD.create_financing_simulation(
        db=session,
        financing_simulation_in=financing_simulation_in,
        user=default_user
    )

    assert financing_simulation_response.amount == financing_simulation_in.amount
    assert financing_simulation_response.duration_months == financing_simulation_in.duration_months

    # Verificando se a simulação foi criada no banco de dados
    db_simulation = await session.execute(
        select(FinancingSimulation).where(FinancingSimulation.user_id == default_user.user_id)
    )
    db_financing_simulation = db_simulation.scalars().first()

    assert db_financing_simulation is not None
    assert db_financing_simulation.total_value == financing_simulation_response.amount
    assert db_financing_simulation.duration_months == financing_simulation_response.duration_months
    assert db_financing_simulation.bank_id is not None


# @pytest.mark.asyncio
# async def test_get_loan_simulation(session: AsyncSession, default_user: User, default_bank: Bank, default_loan_simulation: LoanSimulation):
  
#     user_loans = await SimulationCRUD.get_loan_simulation(db=session, user=default_user)

#     assert isinstance(user_loans, list)
#     assert len(user_loans) == 1
#     assert user_loans[0].amount == default_loan_simulation.amount
#     assert user_loans[0].interest_rate == default_loan_simulation.interest_rate
#     assert user_loans[0].duration_months == default_loan_simulation.duration_months
#     assert user_loans[0].monthly_payment == default_loan_simulation.monthly_payment

#     session.delete(default_loan_simulation)
#     await session.commit()

# @pytest.mark.asyncio
# async def test_get_consortium_simulation(session: AsyncSession, default_user: User):
#     # Criando uma simulação de consórcio para o usuário padrão
#     consortium_simulation = ConsortiumSimulation(
#         user_id=default_user.user_id,
#         duration_months=36,
#         monthly_payment=500.0,
#         total_value=18000.0,
#         bank_id=1
#     )
#     session.add(consortium_simulation)
#     await session.commit()

#     # Recuperando as simulações de consórcio para o usuário padrão
#     user_consortiums = await SimulationCRUD.get_consortium_simulation(db=session, user=default_user)

#     assert isinstance(user_consortiums, list)
#     assert len(user_consortiums) == 1
#     assert isinstance(user_consortiums[0], UserConsortiumsResponse)
#     assert user_consortiums[0].amount == consortium_simulation.total_value
#     assert user_consortiums[0].interest_rate == consortium_simulation.monthly_payment
#     assert user_consortiums[0].duration_months == consortium_simulation.duration_months

#     session.delete(consortium_simulation)
#     await session.commit()

# @pytest.mark.asyncio
# async def test_get_financing_simulation(session: AsyncSession, default_user: User):
#     # Criando uma simulação de financiamento para o usuário padrão
#     financing_simulation = FinancingSimulation(
#         user_id=default_user.user_id,
#         total_value=25000.0,
#         duration_months=48,
#         interest_rate=8.0,
#         monthly_payment=550.0,
#         bank_id=1 
#     )
#     session.add(financing_simulation)
#     await session.commit()

#     # Recuperando as simulações de financiamento para o usuário padrão
#     user_financings = await SimulationCRUD.get_financing_simulation(db=session, user=default_user)

#     assert isinstance(user_financings, list)    