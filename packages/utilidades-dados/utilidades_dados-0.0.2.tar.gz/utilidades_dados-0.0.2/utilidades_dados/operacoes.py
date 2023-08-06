def metade(num, form=False):
    divisao = num / 2
    formato = ''
    if form == True:
        formato = f'R${divisao:.2f}'
    else:
        formato = divisao
    return formato


def dobro(num, form=False):
    multiplica = num * 2
    formato = ''
    if form == True:
        formato = f'R${multiplica:.2f}'
    else:
        formato = multiplica
    return formato


def aumento(num, valorau, form=False):
    aumen = ((num * valorau) / 100) + num
    formato = ''
    if form == True:
        formato = f'R${aumen:.2f}'
    else:
        formato = aumen
    return formato


def diminui(num, valordi, form=False):
    dimin = num - ((num * valordi) / 100)
    formato = ''
    if form == True:
        formato = f'R${dimin:.2f}'
    else:
        formato = dimin
    return formato


def moeda(preco=0, moeda='R$'):
    formato = f'{moeda}{preco:.2f}'.replace(',', '.')
    return formato


def tabelaform(msg, num, largura):
    print(f'{msg:<{largura-10}}', end='')
    print(num)


def resumo(num, aument, reducao, largura):
    print('~' * largura)
    print(f'RESUMO DO VALOR'.center(largura))
    print('~' * largura)
    tabelaform('Preço analisado:', moeda(num), largura)
    tabelaform('Dobro do preço:', dobro(num, True), largura)
    tabelaform('Metade do preço:', metade(num, True), largura)
    tabelaform(f'{aument}% de aumento:', aumento(num, aument, True), largura)
    tabelaform(f'{reducao}% de redução:', diminui(num, reducao, True), largura)
    print('~' * largura)
