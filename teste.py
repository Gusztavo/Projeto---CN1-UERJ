import yfinance as yf
import streamlit as st
import numpy as np

def melhores_acoes(capital, qtd_acoes):
    stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NFLX', 'NVDA', 'JPM', 'V', 'MA', 'BA', 'DIS', 'JNJ', 'WMT']
    indiceSharpe = []

    for stock in stocks:
        indiceSharpe.append((stock, calculate_sharpe_ratio(stock)))

    sortedIndiceSharp = sorted(indiceSharpe, key=lambda x: x[1], reverse=True)
    # Armazenar as melhores ações juntamente com as quantidades selecionadas pelo usuário
    carteira = []
    for stock, indice in sortedIndiceSharp[:qtd_acoes]:
        #baixando info do stock
        stock_info = yf.Ticker(stock)
        #consulta preço atual
        preco_atual = stock_info.history(period="1d")['Close'][0]
        n_acoes = capital / preco_atual
        carteira.append((stock, n_acoes))

    return carteira

def calculate_sharpe_ratio(ticker_symbol):
    # Obtendo os dados históricos da ação
    #taxa livre de risco representa o nível mínimo de rentabilidade que pode ser considerado seguro
    taxa_de_risco = 0.04
    stock_data = yf.download(ticker_symbol, start="2023-01-01", end="2024-01-01")
    # Calculando o retorno diário da ação
    stock_data['Daily_Return'] = stock_data['Adj Close'].pct_change()
    # Calculando o retorno médio diário e o desvio padrão dos retornos diários
    retorno_diario = stock_data['Daily_Return'].mean()
    desvio_diario = stock_data['Daily_Return'].std()
    # Calculando o retorno anualizado
    retorno_anual= retorno_diario * 252  # 252 dias úteis em um ano
    # Calculando o desvio padrão anualizado
    desvio_padrao_anual = desvio_diario * np.sqrt(252)
    # Calculando o índice de Sharpe
    indice_sharpe = (retorno_anual - taxa_de_risco) / desvio_padrao_anual

    return indice_sharpe

def main():
    # Title and instructions
    st.title("Carteira de Ações Otimizada")
    st.markdown("Insira o valor a investir e o número de ações desejadas para obter a carteira ideal.")
    # Inputs
    capital = st.number_input("Valor a Investir (R$)", min_value=1, step=100)
    qtd_acoes = st.number_input("Número de Ações na Carteira", min_value=1)
    # Generate carteira
    if st.button("Gerar Carteira"):
        carteira = melhores_acoes(capital, qtd_acoes)
        st.header("Sua Carteira Otimizada:")

        for i, (stock, num_of_shares) in enumerate(carteira, 1):
            st.markdown(f"{i}. {stock}: {num_of_shares:.2f} ações")

if __name__ == "__main__":
    main()