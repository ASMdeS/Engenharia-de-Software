import pandas as pd
import numpy as np

def gerar_dados_mock():
    datas = pd.date_range(start="2022-01-01", periods=100, freq='D')
    precos = np.linspace(100, 200, num=100) + np.random.normal(0, 5, 100)
    return pd.DataFrame({
        'Date': datas,
        'Close': precos
    })
