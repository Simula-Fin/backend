from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User, LoanSimulation, ConsortiumSimulation, FinancingSimulation, Bank
from app.schemas.requests import LoanSimulationRequest, ConsortiumSimulationRequest, FinancingSimulationRequest
from sqlalchemy import delete, select
from app.schemas.responses import SimulationDetail, LoanSimulationResponse, ConsortiumSimulationResponse, FinancingSimulationResponse
from app.helpers.loan_calculation import TaxCalculation

class SimulationCRUD:
    
    @staticmethod
    async def create_loan_simulation(db: AsyncSession, loan_simulation_in: LoanSimulationRequest, user: User):
        try:
            bank = await db.scalar(select(Bank).order_by(Bank.juros_emprestimo).limit(1))
        except Exception as e:
            raise HTTPException(status_code=404, detail="Nenhum banco encontrado")

        amount = loan_simulation_in.amount
        duration_months = loan_simulation_in.duration_months
        juros_rate = loan_simulation_in.tax
        calculation_loan_simulation = TaxCalculation.table_calculation(amount, duration_months, juros_rate)

        loan_simulation = LoanSimulation(
            user_id=user.user_id,
            amount=amount,
            interest_rate=juros_rate,
            duration_months=duration_months,
            monthly_payment=calculation_loan_simulation[0]['parcela'],
            bank_id=bank.bank_id,
        )
        db.add(loan_simulation)
        await db.commit()

        return LoanSimulationResponse(
            amount=loan_simulation.amount,
            duration_months=loan_simulation.duration_months,
            tax=loan_simulation.interest_rate,
            bank_name=bank.name,
            bank_location=bank.location,
            details=[SimulationDetail(**detail) for detail in calculation_loan_simulation]
        )

    @staticmethod
    async def create_consortium_simulation(db: AsyncSession, consortium_simulation_in: ConsortiumSimulationRequest, user: User) -> ConsortiumSimulation:
        try:
            bank = await db.scalar(select(Bank).order_by(Bank.juros_consortium).limit(1))
        except Exception as e:
            raise HTTPException(status_code=404, detail="Nenhum banco encontrado")

        amount = consortium_simulation_in.amount
        duration_months = consortium_simulation_in.duration_months
        juros_rate = consortium_simulation_in.tax

        calculation_consortium_simulation = TaxCalculation.table_calculation(amount, duration_months, juros_rate)

        consortium_simulation = ConsortiumSimulation(
            user_id=user.user_id,
            amount=amount,
            interest_rate=juros_rate,
            duration_months=duration_months,
            monthly_payment=calculation_consortium_simulation[0]['parcela'],
            bank_id=bank.bank_id,
        )

        db.add(consortium_simulation)
        await db.commit()
        
        return ConsortiumSimulationResponse(
            amount=consortium_simulation.amount,
            duration_months=consortium_simulation.duration_months,
            tax=consortium_simulation.interest_rate,
            bank_name=bank.name,
            bank_location=bank.location,
            details=[SimulationDetail(**detail) for detail in calculation_consortium_simulation]
        ) 

    @staticmethod
    def create_financing_simulation(db: AsyncSession, financing_simulation_in: FinancingSimulationRequest, user: User) -> FinancingSimulation:
        try:
            bank = db.scalar(select(Bank).order_by(Bank.juros_financiamento).limit(1))
        except Exception as e:
            raise HTTPException(status_code=404, detail="Nenhum banco encontrado")

        amount = financing_simulation_in.amount
        duration_months = financing_simulation_in.duration_months
        juros_rate = financing_simulation_in.tax

        calculation_financing_simulation = TaxCalculation.table_calculation(amount, duration_months, juros_rate)

        financing_simulation = FinancingSimulation(
            user_id=user.user_id,
            amount=amount,
            interest_rate=juros_rate,
            duration_months=duration_months,
            monthly_payment=calculation_financing_simulation[0]['parcela'],
            bank_id=bank.bank_id,
        )

        db.add(financing_simulation)
        db.commit()

        return FinancingSimulationResponse(
            amount=financing_simulation.amount,
            duration_months=financing_simulation.duration_months,
            tax=financing_simulation.interest_rate,
            bank_name=bank.name,
            bank_location=bank.location,
            details=[SimulationDetail(**detail) for detail in calculation_financing_simulation]
        )