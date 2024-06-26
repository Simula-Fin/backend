import pytest
from app.helpers.loan_calculation import TaxCalculation

def test_table_calculation_sac():
    amount = 1000.0
    duration_months = 12
    taxa_juros = 1.0

    expected_result = [
        {
            "parcela":93.33,
            "amortizacao":83.33,
            "juros":10.0,
            "saldo_devedor":916.67
        },
        {
            "parcela":92.5,
            "amortizacao":83.33,
            "juros":9.17,
            "saldo_devedor":833.34
        },
        {
            "parcela":91.66,
            "amortizacao":83.33,
            "juros":8.33,
            "saldo_devedor":750.01
        },
        {
            "parcela":90.83,
            "amortizacao":83.33,
            "juros":7.5,
            "saldo_devedor":666.68
        },
        {
            "parcela":90.0,
            "amortizacao":83.33,
            "juros":6.67,
            "saldo_devedor":583.35
        },
        {
            "parcela":89.16,
            "amortizacao":83.33,
            "juros":5.83,
            "saldo_devedor":500.02
        },
        {
            "parcela":88.33,
            "amortizacao":83.33,
            "juros":5.0,
            "saldo_devedor":416.69
        },
        {
            "parcela":87.5,
            "amortizacao":83.33,
            "juros":4.17,
            "saldo_devedor":333.36
        },
        {
            "parcela":86.66,
            "amortizacao":83.33,
            "juros":3.33,
            "saldo_devedor":250.03
        },
        {
            "parcela":85.83,
            "amortizacao":83.33,
            "juros":2.5,
            "saldo_devedor":166.7
        },
        {
            "parcela":85.0,
            "amortizacao":83.33,
            "juros":1.67,
            "saldo_devedor":83.37
        },
        {
            "parcela":84.16,
            "amortizacao":83.33,
            "juros":0.83,
            "saldo_devedor":0.04
        }
    ]

    result = TaxCalculation.table_calculation_sac(amount, duration_months, taxa_juros)
    assert result == expected_result

def test_table_calculation_price():
    amount = 1000.0
    duration_months = 1
    taxa_juros = 1.0

    expected_result = [{'parcela': 1010.0, 'amortizacao': 1000.0, 'juros': 10.0, 'saldo_devedor': 0.0}]
    result = TaxCalculation.table_calculation_price(amount, duration_months, taxa_juros)

    assert result == expected_result

