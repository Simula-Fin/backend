from typing import List
from app.schemas.responses import LoanSimulationDetail

class LoanCalculation:
    @staticmethod
    def calcular_simulacao_emprestimo(amount: float, duration_months: int, taxa_juros: float) -> List[LoanSimulationDetail]:
        detalhes_simulacao = []
        
        parcela_fixa = (amount * (taxa_juros / 100)) / (1 - (1 + taxa_juros / 100) ** -duration_months)
        
        saldo_devedor = amount
        for parcela in range(1, duration_months + 1):
            juros = saldo_devedor * (taxa_juros / 100)
            amortizacao = parcela_fixa - juros
            saldo_devedor -= amortizacao
            
            amortizacao = round(amortizacao, 2)
            juros = round(juros, 2)
            saldo_devedor = round(saldo_devedor, 2)
            valor_parcela = round(parcela_fixa, 2)
            
            detalhes_simulacao.append({
                "parcela": valor_parcela,
                "amortizacao": amortizacao,
                "juros": juros,
                "saldo_devedor": saldo_devedor
            })
        
        return detalhes_simulacao