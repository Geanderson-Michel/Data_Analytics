# IMPORTA AS BIBLIOTECAS
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
from unidecode import unidecode
from collections import Counter

###############################################################################################################
################################### CONFIGURAÇÃO DO USUÁRIO ###################################################
###############################################################################################################

# EXIBE AS n DEZENAS MAIS SORTEADAS DA MEGA-SENA
n = 10

# NOME DA PLANILHA COM OS DADOS DOS SORTEIOS DA MEGA-SENA
mega_sena_plan = 'Mega-Sena.xlsx'

# CAMINHO PARA SALVAR AS FIGURAS
save_figs_and_plan = os.getcwd()

###############################################################################################################
###### ACESSA OS DADOS SOBRE A MEGA-SENA, ARMAZENA AS COLUNAS DE INTERESSE E CRIA UMA FIGURA ##################
###############################################################################################################

# CRIA UM CAMINHO ATÉ A PLANILHA DA MEGA-SENA
mega_sena_plan_path = os.path.join(os.getcwd(), mega_sena_plan)

# CRIA UM DATAFRAME COM OS DADOS DOS SORTEIOS DA MEGA-SENA
df = pd.read_excel(mega_sena_plan_path)

# SEPARA AS COLUNAS COM AS DEZENAS SORTEADAS
bolas_sorteadas = df[['Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5', 'Bola6']]

# NÚMERO DE SORTEIOS PARA A MEGA-SENA JÁ REALIZADOS PELA CAIXA
num_sorteios = len(bolas_sorteadas.index)

# CRIA UMA FIGURA E OS SUBPLOTS
fig, axs = plt.subplots(1, 2, figsize=(12, 5))

###############################################################################################################
###### ENCONTRA AS n DEZENAS MAIS SORTEADAS E CRIA UM GRÁFICO DE BARRA COM ESSA INFORMAÇÃO ####################
###############################################################################################################

# CRIA UMA SÉRIE A PARTIR DO DATAFRAME bolas_sorteadas QUE CONTÉM A CONTAGEM DOS VALORES EM TODAS AS COLUNAS
contagem_dezenas = bolas_sorteadas.stack().value_counts()

# EXIBE AS n DEZENAS MAIS SORTEADAS DA MEGA-SENA
print(f"{n} Dezenas mais sorteadas da Mega-Sena")
print(contagem_dezenas.head(n))

# CRIA UM GRÁFICO DE COLUNAS USANDO SEABORN
bar_plot0 = sns.barplot(x = contagem_dezenas.head(n).index.astype(str), y = contagem_dezenas.head(n).values, ax = axs[0])

# ADICIONA UM TÍTULO AO SUBPLOT DE ÍNDICE 0
#axs[0].set_title(f'{n} dezenas mais sorteadas da Mega-Sena desde 03/1996')

# ADICIONA RÓTULOS AOS EIXOS X E Y
axs[0].set(xlabel = "Dezenas sortedas", ylabel = "Frequência")

# CALCULA OS PERCENTUAIS DE VEZES QUE AS n DEZENAS FORAM SORTEADAS
percentual_dezenas = [round(contagem / num_sorteios, 4) * 100 for contagem in contagem_dezenas.head(n).values.tolist()]

# ADICIONA OS PERCENTUAIS SOBRE AS BARRAS
for index, value in enumerate(contagem_dezenas.head(n).values):

    bar_plot0.text(index, value + 5, s = f"{percentual_dezenas[index]:.2f}%", fontsize = 7, color='black', ha='center')

###############################################################################################################
###### ENCONTRA OS n LOCAIS MAIS PREMIADOS E CRIA UM GRÁFICO DE BARRA COM ESSA INFORMAÇÃO #####################
###############################################################################################################

# SALVA TODAS AS CIDADES PREMIADAS PELA MEGA-SENA
cidades_vencedoras = []

# FAZ UM TRATAMENTO DAS STRINGS NA COLUNA 'Cidade / UF'
for cidade in df['Cidade / UF'].dropna():

    if ('/' not in cidade) and (';' in cidade):

        lista_cidades = cidade.split('; ')

        cidades_vencedoras += lista_cidades

    elif ('/' in cidade) and (';' not in cidade):

        cidades_vencedoras += [cidade.split('/')[1]]

    elif ('/' in cidade) and (';' in cidade):

        for cid in cidade.split('; '):

            if ('canal eletronico' == unidecode(cid).lower()):

                cidades_vencedoras += ['internet']

            else:

                cidades_vencedoras += [cid.split('/')[1]]

    elif ('canal eletronico' == unidecode(cidade).lower()):

        cidades_vencedoras += ['internet']

    else:

        cidades_vencedoras += [cidade]

# TRANSFORMA A LISTA cidades_vencedoras EM SÉRIE
cidades_vencedoras = pd.Series(cidades_vencedoras)

# EXIBE OS n LOCAIS MAIS PREMIADOS
print()
print(f"{n} locais mais premiados da Mega-Sena")
print(cidades_vencedoras.value_counts().head(n))

# CRIA UM GRÁFICO DE COLUNAS USANDO SEABORN
bar_plot1 = sns.barplot(x = cidades_vencedoras.value_counts().head(n).index.astype(str), y = cidades_vencedoras.value_counts().head(n).values, ax = axs[1])

# ADICIONA UM TÍTULO AO SUBPLOT DE ÍNDICE 1
#axs[1].set_title(f'{n} locais mais premiados da Mega-Sena desde 03/1996')

# ADICIONA RÓTULOS AOS EIXOS X E Y
axs[1].set(xlabel = "Locais premiados", ylabel = "Frequência")

# CALCULA OS PERCENTUAIS DE VEZES QUE OS n LOCAIS FORAM PREMIADOS
percentual_dezenas = [round(contagem / num_sorteios, 4) * 100 for contagem in cidades_vencedoras.value_counts().head(n).values.tolist()]

# ADICIONA OS PERCENTUAIS SOBRE AS BARRAS
for index, value in enumerate(cidades_vencedoras.value_counts().head(n).values):

    bar_plot1.text(index, value + 5, f"{percentual_dezenas[index]:.2f}%", fontsize = 7, color='black', ha='center')

# CRIA UM TÍTULO PARA A FIGURA
plt.suptitle(f"As {n} dezenas mais sorteadas e os {n} locais mais premiados da Mega-Sena desde 03/1996",
             fontsize = 14)

# SALVA A FIGURA
plt.savefig(os.path.join(save_figs_and_plan, f'{n} dezenas mais sorteadas.png'), dpi = 300, bbox_inches = 'tight')  # dpi é a resolução da imagem, bbox_inches='tight' ajusta o espaçamento


###############################################################################################################
######################## AVALIAÇÃO DAS DEZENAS SORTEADAS POR QUADRANTES #######################################
###############################################################################################################

# CONSTRUÇÃO DOS 4 QUADRANTES
quadrante_1 = list(range(1, 6)) + list(range(11, 16)) + list(range(21, 26))
quadrante_2 = list(range(6, 11)) + list(range(16, 21)) + list(range(26, 31))
quadrante_3 = list(range(31, 36)) + list(range(41, 46)) + list(range(51, 56))
quadrante_4 = list(range(36, 41)) + list(range(46, 51)) + list(range(56, 61))

# SALVA DICIONÁRIOS COM A QUANTIDADE DE DEZENAS SORTEADAS POR QUADRANTE PARA CADA SORTEIO DA MEGA-SENA
bolas_por_quadrantes = []

# NÚMERO INCIAL DE DEZENAS POR QUADRANTE
q1 = 0
q2 = 0
q3 = 0
q4 = 0

# VERIFICA, PARA CADA SORTEIO, QUANTAS DEZENAS ESTÃO INDERIDAS NOS QUADRANTES 1, 2, 3 E 4
for index, row in bolas_sorteadas.iterrows():

    # SELECIONA CADA UMA DAS 6 DEZENAS NA VARIÁVEL row
    for dezena in row:

        if dezena in quadrante_1:

            q1 += 1

        elif dezena in quadrante_2:

            q2 += 1

        elif dezena in quadrante_3:

            q3 += 1

        elif dezena in quadrante_4:

            q4 += 1

    # SALVA, PARA CADA SORTEIO, A QNTD DE DEZENAS POR QUADRANTE
    bolas_por_quadrantes += [{'q1': q1, 'q2': q2, 'q3': q3, 'q4': q4}]

    # ZERA OS VALORES DOS QUADRANTES PARA UMA NOVA ITERAÇÃO
    q1 = 0
    q2 = 0
    q3 = 0
    q4 = 0

# USA A CLASSE Counter PARA CONTAR A OCORRÊNCIA DE CADA DICIONÁRIO COM A QNTD DE DEZENAS POR QUADRANTE
contagem_dicionarios = Counter(map(str, bolas_por_quadrantes))

data = []

# EXTRAI OS DICIONÁRIOS NAS TUPLAS DO OBJETO dict_items E OS ARMAZENA EM data
for dicionario, quantidade in contagem_dicionarios.items():

    # TRANSFORMA O DICIONÁRIO NO FORMATO STRING EM UM OBJETO DICIONÁRIO
    dicionario = eval(dicionario)

    data.append({'Q1': dicionario['q1'],
                 'Q2': dicionario['q2'],
                 'Q3': dicionario['q3'],
                 'Q4': dicionario['q4'],
                 'frequencia': quantidade})

# CONVERTE AS INFORMAÇÕES EM data EM UM DATAFRAME
df = pd.DataFrame(data = data)

# ORGANIZA O DATAFRAME PELA COLUNA frequencia
df = df.sort_values(by = 'frequencia', ascending = False)

# SALVA O DATAFRAME
df.to_excel('Avaliacao_quadrantes.xlsx', index = False)
