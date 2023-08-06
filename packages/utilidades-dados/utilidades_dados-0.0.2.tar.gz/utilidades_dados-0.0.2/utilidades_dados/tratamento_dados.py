def filtrodados(lista, dados, coluna):
    import pandas as pd
    filtro = list()
    for c, v in enumerate(lista):
        for d in dados[coluna]:
            if v == d:
                c = dados.loc[
                    (dados[coluna] == v)
                ]
                filtro.append(c)
    dadosconcat = pd.concat(filtro)
    return dadosconcat


def adicionar_coluna_dados(dados, coluna, operacao, nome_nova_coluna=None):
    import numpy as np
    if operacao == 'novos_casos':
        dados[nome_nova_coluna] = list(map(
            lambda x: 0 if (x == 0) else dados[coluna].iloc[x] - dados[coluna].iloc[x - 1],
            np.arange(dados.shape[0])
        ))

    elif operacao == 'acumulado':
        dados[nome_nova_coluna] = list(map(
            lambda x: dados[coluna].iloc[0] if (x == 0) else dados[coluna].iloc[x] + dados[coluna].iloc[x - 1],
            np.arange(dados.shape[0])
        ))


def taxa_evolucao(dados, coluna, data_inicio=None, coluna_data=None):
    import pandas as pd
    import numpy as np
    if data_inicio == None:
        data_inicio = dados[coluna_data].loc[dados[coluna] > 0].min()
    else:
        data_inicio = pd.to_datetime(data_inicio)

    datafim = dados[coluna_data].max()

    n = (datafim - data_inicio).days

    taxas = list(map(
        lambda x: (dados[coluna].iloc[x] - dados[coluna].iloc[x - 1]) / dados[coluna].iloc[x - 1],
        range(1, n + 1)
    ))
    return np.array(taxas) * 100