from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User, LoanSimulation, ConsortiumSimulation, FinancingSimulation, Bank
from app.schemas.requests import LoanSimulationRequest, ConsortiumSimulationRequest, FinancingSimulationRequest
from sqlalchemy import delete, select
from datetime import datetime
from app.schemas.responses import LoanSimulationDetail, LoanSimulationResponse
from app.helpers.loan_calculation import LoanCalculation

class SimulationCRUD:
    
    @staticmethod
    async def create_loan_simulation(db: AsyncSession, loan_simulation_in: LoanSimulationRequest, user: User):
        try:

            bank = await db.scalar(select(Bank).order_by(Bank.taxa_juros).limit(1))
        except Exception as e:
            raise HTTPException(status_code=404, detail="Nenhum banco encontrado")

        # Calcular os detalhes das parcelas
        amount = loan_simulation_in.amount
        duration_months = loan_simulation_in.duration_months
        juros_rate = loan_simulation_in.tax
        calculation_loan_simulation = LoanCalculation.calcular_simulacao_emprestimo(amount, duration_months, juros_rate)

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
            details=[LoanSimulationDetail(**detail) for detail in calculation_loan_simulation]
        )