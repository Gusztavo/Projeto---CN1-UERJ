import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
from itertools import combinations

def get_best_portfolio(amount, stocks, qtd_acoes):
    # Calcula o índice de Sharpe para cada combinação de até qtd_acoes ações
    melhor_portfolio = None
    melhor_sharpe = -float('inf')

    for combination in combinations(stocks, qtd_acoes):
        sharpe = calculate_portfolio_sharpe(list(combination))
        if sharpe > melhor_sharpe:
            melhor_sharpe = sharpe
            melhor_portfolio = combination

    # Calcula o número de ações de cada empresa no portfólio
    portfolio = []
    for stock in melhor_portfolio:
        stock_info = yf.Ticker(stock)
        current_price = stock_info.history(period="1d")['Close'][0]
        num_of_shares = amount / current_price
        portfolio.append((stock, num_of_shares))

    return portfolio


def calculate_portfolio_sharpe(portfolio):
    # Obtendo os dados históricos das ações no portfólio
    risk_free_rate = 0.04
    sharpe_ratios = []

    for ticker in portfolio:
        stock_data = yf.download(ticker, start="2023-01-01", end="2024-01-01")['Adj Close']

        # Calculando os retornos diários da ação
        daily_returns = stock_data.pct_change().dropna()

        # Calculando o retorno médio diário e o desvio padrão dos retornos diários
        average_daily_return = daily_returns.mean()
        standard_deviation = daily_returns.std()

        # Calculando o retorno anualizado
        annualized_return = average_daily_return * 252  # 252 dias úteis em um ano

        # Calculando o desvio padrão anualizado
        annualized_std_dev = standard_deviation * np.sqrt(252)

        # Calculando o índice de Sharpe
        sharpe_ratio = (annualized_return - risk_free_rate) / annualized_std_dev

        sharpe_ratios.append(sharpe_ratio)

    # Retorna o menor índice de Sharpe do portfólio
    return min(sharpe_ratios)


def main():
    st.title("Seleção Automática de Portfólio")

    # Lista de ações disponíveis
    stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NFLX', 'NVDA', 'JPM', 'V', 'MA', 'BA', 'DIS', 'JNJ', 'WMT']

    # Campos de entrada para o valor a ser investido e a quantidade de ações desejada
    amount = st.number_input("Digite o valor em reais que deseja investir:", min_value=0.01, step=0.01)
    qtd_acoes = st.number_input("Quantas ações deseja ter em seu melhor portfólio? (Recomendado acima de 3):", min_value=1, step=1, value=3)

    # Botão para calcular o melhor portfólio
    if st.button("Calcular Melhor Portfólio"):
        portfolio = get_best_portfolio(amount, stocks, int(qtd_acoes))
        st.subheader("Melhor Portfólio:")
        for i, (stock, num_of_shares) in enumerate(portfolio, 1):
            st.write(f"{i}. {stock}: {num_of_shares:.2f} ações")


if __name__ == "__main__":
    main()
