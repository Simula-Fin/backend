# import pytest
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# #from app.models import User, LoanSimulation, ConsortiumSimulation, FinancingSimulation, Bank
# from ...models import User, LoanSimulation, ConsortiumSimulation, FinancingSimulation, Bank
# from app.schemas.requests import LoanSimulationRequest, ConsortiumSimulationRequest, FinancingSimulationRequest
# from app.schemas.responses import LoanSimulationResponse, ConsortiumSimulationResponse, FinancingSimulationResponse
# from app.helpers.loan_calculation import TaxCalculation
# from app.services.simulations import SimulationCRUD
# from fastapi import HTTPException

# # Configurações do banco de dados para testes
# SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# engine = create_async_engine(SQLALCHEMY_DATABASE_URL, future=True, echo=True)
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)
# Base = declarative_base()

# # Fixtures para configuração e limpeza do banco de dados
# @pytest.fixture(scope="module")
# async def db_session():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     async with TestingSessionLocal() as session:
#         yield session
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)

# @pytest.fixture
# def fake_user():
#     return User(user_id=1, name="Test User", email="testuser@example.com")

# @pytest.fixture
# def fake_bank():
#     return Bank(bank_id=1, name="Test Bank", location="Test Location", juros_emprestimo=5.0, juros_consortium=4.0, juros_financiamento=3.0)

# # Testes de criação
# @pytest.mark.asyncio
# async def test_create_loan_simulation(db_session, fake_user, fake_bank):
#     await db_session.add(fake_bank)
#     await db_session.commit()

#     loan_request = LoanSimulationRequest(amount=10000, duration_months=12, tax=5.0)
#     response = await SimulationCRUD.create_loan_simulation(db_session, loan_request, fake_user)

#     assert isinstance(response, LoanSimulationResponse)
#     assert response.amount == 10000
#     assert response.duration_months == 12
#     assert response.tax == 5.0
#     assert response.bank_name == "Test Bank"

# @pytest.mark.asyncio
# async def test_create_consortium_simulation(db_session, fake_user, fake_bank):
#     await db_session.add(fake_bank)
#     await db_session.commit()

#     consortium_request = ConsortiumSimulationRequest(amount=15000, duration_months=24, tax=4.0)
#     response = await SimulationCRUD.create_consortium_simulation(db_session, consortium_request, fake_user)

#     assert isinstance(response, ConsortiumSimulationResponse)
#     assert response.amount == 15000
#     assert response.duration_months == 24
#     assert response.tax == 4.0
#     assert response.bank_name == "Test Bank"

# @pytest.mark.asyncio
# async def test_create_financing_simulation(db_session, fake_user, fake_bank):
#     await db_session.add(fake_bank)
#     await db_session.commit()

#     financing_request = FinancingSimulationRequest(amount=20000, duration_months=36, tax=3.0)
#     response = await SimulationCRUD.create_financing_simulation(db_session, financing_request, fake_user)

#     assert isinstance(response, FinancingSimulationResponse)
#     assert response.amount == 20000
#     assert response.duration_months == 36
#     assert response.tax == 3.0
#     assert response.bank_name == "Test Bank"

# # Testes de recuperação
# @pytest.mark.asyncio
# async def test_get_loan_simulation(db_session, fake_user):
#     loan_simulations = await SimulationCRUD.get_loan_simulation(db_session, fake_user)
#     assert isinstance(loan_simulations, list)

# @pytest.mark.asyncio
# async def test_get_consortium_simulation(db_session, fake_user):
#     consortium_simulations = await SimulationCRUD.get_consortium_simulation(db_session, fake_user)
#     assert isinstance(consortium_simulations, list)

# @pytest.mark.asyncio
# async def test_get_financing_simulation(db_session, fake_user):
#     financing_simulations = await SimulationCRUD.get_financing_simulation(db_session, fake_user)
#     assert isinstance(financing_simulations, list)
