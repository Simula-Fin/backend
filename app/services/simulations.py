from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User, LoanSimulation, ConsortiumSimulation, FinancingSimulation, Bank
from app.schemas.requests import LoanSimulationRequest, ConsortiumSimulationRequest, FinancingSimulationRequest
from sqlalchemy import delete, select
from app.schemas.responses import SimulationDetail, LoanSimulationResponse, ConsortiumSimulationResponse, FinancingSimulationResponse, UserFinancingsResponse, UserConsortiumsResponse, UserLoansResponse
from app.helpers.loan_calculation import TaxCalculation
from sqlalchemy.orm import selectinload

class SimulationCRUD:
    
    @staticmethod
    async def create_loan_simulation(db: AsyncSession, loan_simulation_in: LoanSimulationRequest, user: User):
        try:
            bank = await db.scalar(select(Bank).order_by(Bank.juros_emprestimo).limit(1))

            if not bank:
                raise HTTPException(status_code=404, detail="Nenhum banco encontrado")
        
            amount = loan_simulation_in.amount
            duration_months = loan_simulation_in.duration_months
            juros_rate = loan_simulation_in.tax

            calculation_method = loan_simulation_in.calculation_method

            if calculation_method == "sac":
                calculation_loan_simulation = TaxCalculation.table_calculation_sac(amount, duration_months, juros_rate)
            elif calculation_method == "price":
                calculation_loan_simulation = TaxCalculation.table_calculation_price(amount, duration_months, juros_rate)
            else:
                raise HTTPException(status_code=400, detail="Método de cálculo inválido")
        
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
        
        except Exception as e:
            raise HTTPException(status_code=404, detail="Erro to create loan simulation")

    @staticmethod
    async def create_consortium_simulation(db: AsyncSession, consortium_simulation_in: ConsortiumSimulationRequest, user: User) -> ConsortiumSimulation:
        try:
            bank = await db.scalar(select(Bank).order_by(Bank.juros_consortium).limit(1))

            if not bank:
                raise HTTPException(status_code=404, detail="Nenhum banco encontrado")

            amount = consortium_simulation_in.amount
            duration_months = consortium_simulation_in.duration_months
            juros_rate = consortium_simulation_in.tax
            calculation_method = consortium_simulation_in.calculation_method

            if calculation_method == "sac":
                calculation_consortium_simulation = TaxCalculation.table_calculation_sac(amount, duration_months, juros_rate)
            elif calculation_method == "price":
                calculation_consortium_simulation = TaxCalculation.table_calculation_price(amount, duration_months, juros_rate)
            else:
                raise HTTPException(status_code=400, detail="Método de cálculo inválido")

            consortium_simulation = ConsortiumSimulation(
                user_id=user.user_id,
                duration_months=duration_months,
                monthly_contribution=calculation_consortium_simulation[0]['parcela'],
                total_value=calculation_consortium_simulation[0]['parcela'],
                bank_id=bank.bank_id,
            )

            db.add(consortium_simulation)
            await db.commit()
            
            return ConsortiumSimulationResponse(
                amount=consortium_simulation.total_value,
                duration_months=int(consortium_simulation.monthly_contribution),
                tax=consortium_simulation.monthly_contribution,
                bank_name=bank.name,
                bank_location=bank.location,
                details=[SimulationDetail(**detail) for detail in calculation_consortium_simulation]
            )
        except Exception as e:
            print(e)
            raise HTTPException(status_code=404, detail="Erro to create consortium simulation") 

    @staticmethod
    async def create_financing_simulation(db: AsyncSession, financing_simulation_in: FinancingSimulationRequest, user: User) -> FinancingSimulation:
        try:
            bank = await db.scalar(select(Bank).order_by(Bank.juros_financiamento).limit(1))

            if not bank:
                raise HTTPException(status_code=404, detail="Nenhum banco encontrado")

            amount = financing_simulation_in.amount
            duration_months = financing_simulation_in.duration_months
            juros_rate = financing_simulation_in.tax

            calculation_method = financing_simulation_in.calculation_method

            if calculation_method == "sac":
                calculation_financing_simulation = TaxCalculation.table_calculation_sac(amount, duration_months, juros_rate)
            elif calculation_method == "price":
                calculation_financing_simulation = TaxCalculation.table_calculation_price(amount, duration_months, juros_rate)
            else:
                raise HTTPException(status_code=400, detail="Método de cálculo inválido")

            
            financing_simulation = FinancingSimulation(
                user_id=user.user_id,
                total_value=amount,
                down_payment=calculation_financing_simulation[0]['parcela'],
                interest_rate=juros_rate,
                duration_months=duration_months,
                monthly_payment=calculation_financing_simulation[0]['parcela'],
                bank_id=bank.bank_id,
            )

            db.add(financing_simulation)
            await db.commit()

            return FinancingSimulationResponse(
                amount=financing_simulation.total_value,
                duration_months=financing_simulation.duration_months,
                tax=financing_simulation.interest_rate,
                bank_name=bank.name,
                bank_location=bank.location,
                details=[SimulationDetail(**detail) for detail in calculation_financing_simulation]
            )
        
        except Exception as e:
            raise HTTPException(status_code=404, detail="Erro to create financing simulation")
    
    @staticmethod
    async def get_loan_simulation(db: AsyncSession, user: User):
        loan_simulations = await db.scalars(select(LoanSimulation).where(LoanSimulation.user_id == user.user_id).options(selectinload(LoanSimulation.bank)))
        
        return [
            UserLoansResponse(
                amount=loan.amount,
                interest_rate=loan.interest_rate,
                duration_months=loan.duration_months,
                monthly_payment=loan.monthly_payment,
                bank_name=loan.bank.name,
                created_at=str(loan.created_at)
            ) for loan in loan_simulations
        ]
        
    
    @staticmethod
    async def get_consortium_simulation(db: AsyncSession, user: User):
        consortium_simulation = await db.scalars(select(ConsortiumSimulation).where(ConsortiumSimulation.user_id == user.user_id).options(selectinload(ConsortiumSimulation.bank)))

        return [
            UserConsortiumsResponse(
                amount=consortium.amount,
                interest_rate=consortium.interest_rate,
                duration_months=consortium.duration_months,
                monthly_payment=consortium.monthly_payment,
                bank_name=consortium.bank.name,
                created_at=consortium.created_at
            ) for consortium in consortium_simulation
        ]
    
    @staticmethod
    async def get_financing_simulation(db: AsyncSession, user: User):
        financing_simulation = await db.scalars(select(FinancingSimulation).where(FinancingSimulation.user_id == user.user_id).options(selectinload(FinancingSimulation.bank)))
        
        return [
            UserFinancingsResponse(
                amount=financing.total_value,
                interest_rate=financing.interest_rate,
                duration_months=financing.duration_months,
                monthly_payment=financing.monthly_payment,
                bank_name=financing.bank.name,
                created_at=str(financing.created_at)
            ) for financing in financing_simulation
        ]