import pandas as pd

def encontrar_numero_maior_proximo(df, coluna, numero_desejado):
    for index, row in df.iterrows():
        if row[coluna] == numero_desejado:
            return numero_desejado
        elif row[coluna] > numero_desejado:
            return row[coluna]
    return df.iloc[-1][coluna]


#Passo 1: Determinar a corrente de projeto do projeto
corrente_de_projeto = 0
while not corrente_de_projeto:
    try:
        potencia = float(input("\nInsira a potência em watt [W]: "))
        tensao = float(input("Insira a tensão em volts [V]: "))
        corrente_de_projeto = potencia / tensao
        break
    except ValueError:
        print("Valor inválido\n")
    except ZeroDivisionError:
        print("A tensão não pode ser nula.\n")

print(f"\nCorrente de projeto: {corrente_de_projeto:.2f} A\n")


#Passo 2: Determinar os fatores de correção:
tabela_fatores_correcao_sub = {
    "Temperatura": [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80],
    "PVC": [1.10, 1.05, 1, 0.95, 0.89, 0.84, 0.77, 0.71, 0.63, 0.55, 0.45, 0.45, 0.45, 0.45, 0.45],
    "EPRorXLPE": [1.07, 1.04, 1, 0.96, 0.93, 0.89, 0.85, 0.80, 0.76, 0.71, 0.65, 0.60, 0.53, 0.46, 0.38]
}
tabela_fatores_correcao_Nsub = {
    "Temperatura": [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80],
    "PVC": [1.22, 1.17, 1.12, 1.06, 1, 0.94, 0.87, 0.79, 0.71, 0.61, 0.50, 0.50, 0.50, 0.50, 0.50],
    "EPRorXLPE": [1.15, 1.12, 1.08, 1.04, 1, 0.96, 0.91, 0.87, 0.82, 0.76, 0.71, 0.65, 0.58, 0.50, 0.41]
}
tabela_fca = {
    "N_Circ_CabosMulti": ["1", "2", "3", "4", "5", "6", "7", "8", "9 a 11", "12 a 15", "16 a 19", ">=20"],
    "FCA": [1.00, 0.80, 0.70, 0.65, 0.60, 0.57, 0.54, 0.52, 0.50, 0.45, 0.41, 0.38]
}

df_sub = pd.DataFrame(tabela_fatores_correcao_sub)
df_nsub = pd.DataFrame(tabela_fatores_correcao_Nsub)
df_fca = pd.DataFrame(tabela_fca)

temperatura = float(input('Defina a temperatura ambiente em °C: '))
subterraneo = False if input('O ambiente é subterrâneo[S] ou não-subterraneo[NS]?: ').upper()=='NS' else True
qtd_circuitos_cabmult = int(input("Insira a quantidade de circuitos ou cabos multipolares: "))

if subterraneo:
    temp = temperatura if temperatura == 20 else encontrar_numero_maior_proximo(df_sub, 'Temperatura', temperatura)
    tipo_condutor = input('Insira o tipo de condutor(PVC, EPR ou XLPE): ').upper()
    if tipo_condutor == 'PVC':
        linha = df_sub[df_sub['Temperatura'] == temp]
        FCT = linha.iloc[0, 1]
        print(f'\nO FCT é: {FCT}')
    else:
        linha = df_sub[df_sub['Temperatura'] == temp]
        FCT = linha.iloc[0, 2]
        print(f'\nO FCT é: {FCT}')
else:
    temp = temperatura if temperatura == 30 else encontrar_numero_maior_proximo(df_nsub, 'Temperatura', temperatura)
    tipo_condutor = input('Insira o tipo de condutor(PVC, EPR ou XLPE): ').upper()
    if tipo_condutor == 'PVC':
        linha = df_nsub[df_nsub['Temperatura'] == temp]
        FCT = linha.iloc[0, 1]
        print(f'\nO FCT é: {FCT}')
    else:
        linha = df_nsub[df_nsub['Temperatura'] == temp]
        FCT = linha.iloc[0, 2]
        print(f'\nO FCT é: {FCT}')
if 1 <= qtd_circuitos_cabmult <= 8:
    FCA = df_fca.loc[df_fca["N_Circ_CabosMulti"] == str(qtd_circuitos_cabmult), "FCA"].values[0]
elif 9 <= qtd_circuitos_cabmult <= 11:
    FCA = df_fca.loc[df_fca["N_Circ_CabosMulti"] == "9 a 11", "FCA"].values[0]
elif 12 <= qtd_circuitos_cabmult <= 15:
    FCA = df_fca.loc[df_fca["N_Circ_CabosMulti"] == "12 a 15", "FCA"].values[0]
elif 16 <= qtd_circuitos_cabmult <= 19:
    FCA = df_fca.loc[df_fca["N_Circ_CabosMulti"] == "16 a 19", "FCA"].values[0]
elif qtd_circuitos_cabmult >= 20:
    FCA = df_fca.loc[df_fca["N_Circ_CabosMulti"] == ">=20", "FCA"].values[0]
else:
    FCA = None
print(f"O FCA é: {FCA:.2f}.\n")


#Passo 3: Determinar a corrente de projeto corrigida:
corrente_de_projeto_corrigida = corrente_de_projeto/(FCA*FCT)

print(f"A corrente de projeto corrigida é: {corrente_de_projeto_corrigida:.2f} A.\n")


#Passo 4: Selecionar o condutor:
secoes_nominais = [0.5, 0.75, 1, 1.5, 2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95]
tabela_a1 = {
    "Seções nominais": secoes_nominais,
    "2 Condutores": [7, 9, 11, 14.5, 19.5, 26, 34, 46, 61, 80, 99, 119, 151, 182],
    "3 Condutores": [7, 9, 10, 13.5, 18, 24, 31, 42, 56, 73, 89, 108, 136, 164]
}

tabela_a2 = {
    "Seções nominais": secoes_nominais,
    "2 Condutores": [7, 9, 11, 14, 18.5, 25, 32, 43, 57, 75, 92, 110, 139, 167],
    "3 Condutores": [7, 9, 10, 13, 17.5, 23, 29, 39, 52, 68, 83, 99, 125, 150]
}

tabela_b1 = {
    "Seções nominais": secoes_nominais,
    "2 Condutores": [9, 11, 14, 17.5, 24, 32, 41, 57, 76, 101, 125, 151, 192, 232],
    "3 Condutores": [8, 10, 12, 15.5, 21, 28, 36, 50, 68, 89, 110, 134, 171, 207]
}

tabela_b2 = {
    "Seções nominais": secoes_nominais,
    "2 Condutores": [9, 11, 13, 16.5, 23, 30, 38, 52, 69, 90, 111, 133, 168, 201],
    "3 Condutores": [8, 10, 12, 15, 20, 27, 34, 46, 62, 80, 99, 118, 149, 179]
}

tabela_c = {
    "Seções nominais": secoes_nominais,
    "2 Condutores": [10, 13, 15, 19.5, 27, 36, 46, 63, 85, 112, 138, 168, 213, 258],
    "3 Condutores": [9, 11, 14, 17.5, 24, 32, 41, 57, 76, 96, 119, 144, 184, 223]
}

tabela_d = {
    "Seções nominais": secoes_nominais,
    "2 Condutores": [12, 15, 18, 22, 29, 38, 47, 63, 85, 104, 125, 148, 183, 216],
    "3 Condutores": [10, 12, 15, 18, 24, 31, 39, 52, 67, 86, 103, 122, 151, 179]
}

df_a1 = pd.DataFrame(tabela_a1)
df_a2 = pd.DataFrame(tabela_a2)
df_b1 = pd.DataFrame(tabela_b1)
df_b2 = pd.DataFrame(tabela_b2)
df_c = pd.DataFrame(tabela_c)
df_d = pd.DataFrame(tabela_d)

metodo_de_referencia = input('Defina o método de referência(A1, A2, B1, B2, C, D): ').upper()
qtd_condutores_carregados = int(input("Escolha o número de condutores carregados. 2 ou 3: "))

if qtd_condutores_carregados == 2:
    if metodo_de_referencia == 'A1':
        corrente_de_referencia = encontrar_numero_maior_proximo(df_a1, '2 Condutores', corrente_de_projeto_corrigida)
        linha = df_a1[df_a1['2 Condutores'] == corrente_de_referencia]
        secao_nominal_cabo = linha.iloc[0,0]
    elif metodo_de_referencia == 'A2':
        corrente_de_referencia = encontrar_numero_maior_proximo(df_a2, '2 Condutores', corrente_de_projeto_corrigida)
        linha = df_a2[df_a2['2 Condutores'] == corrente_de_referencia]
        secao_nominal_cabo = linha.iloc[0,0]
    elif metodo_de_referencia == 'B1':
        corrente_de_referencia = encontrar_numero_maior_proximo(df_b1, '2 Condutores', corrente_de_projeto_corrigida)
        linha = df_b1[df_b1['2 Condutores'] == corrente_de_referencia]
        secao_nominal_cabo = linha.iloc[0,0]
    elif metodo_de_referencia == 'B2':
        corrente_de_referencia = encontrar_numero_maior_proximo(df_b2, '2 Condutores', corrente_de_projeto_corrigida)
        linha = df_b2[df_b2['2 Condutores'] == corrente_de_referencia]
        secao_nominal_cabo = linha.iloc[0,0]
    elif metodo_de_referencia == 'C':
        corrente_de_referencia = encontrar_numero_maior_proximo(df_c, '2 Condutores', corrente_de_projeto_corrigida)
        linha = df_c[df_c['2 Condutores'] == corrente_de_referencia]
        secao_nominal_cabo = linha.iloc[0,0]
    elif metodo_de_referencia == 'D':
        corrente_de_referencia = encontrar_numero_maior_proximo(df_d, '2 Condutores', corrente_de_projeto_corrigida)
        linha = df_d[df_d['2 Condutores'] == corrente_de_referencia]
        secao_nominal_cabo = linha.iloc[0,0]

elif  qtd_condutores_carregados == 3:
    if metodo_de_referencia == 'A1':
        corrente_de_referencia = encontrar_numero_maior_proximo(df_a1, '3 Condutores', corrente_de_projeto_corrigida)
        linha = df_a1[df_a1['3 Condutores'] == corrente_de_referencia]
        secao_nominal_cabo = linha.iloc[0,0]
    elif metodo_de_referencia == 'A2':
        corrente_de_referencia = encontrar_numero_maior_proximo(df_a2, '3 Condutores', corrente_de_projeto_corrigida)
        linha = df_a2[df_a2['3 Condutores'] == corrente_de_referencia]
        secao_nominal_cabo = linha.iloc[0,0]
    elif metodo_de_referencia == 'B1':
        corrente_de_referencia = encontrar_numero_maior_proximo(df_b1, '3 Condutores', corrente_de_projeto_corrigida)
        linha = df_b1[df_b1['3 Condutores'] == corrente_de_referencia]
        secao_nominal_cabo = linha.iloc[0,0]
    elif metodo_de_referencia == 'B2':
        corrente_de_referencia = encontrar_numero_maior_proximo(df_b2, '3 Condutores', corrente_de_projeto_corrigida)
        linha = df_b2[df_b2['3 Condutores'] == corrente_de_referencia]
        secao_nominal_cabo = linha.iloc[0,0]
    elif metodo_de_referencia == 'C':
        corrente_de_referencia = encontrar_numero_maior_proximo(df_c, '3 Condutores', corrente_de_projeto_corrigida)
        linha = df_c[df_c['3 Condutores'] == corrente_de_referencia]
        secao_nominal_cabo = linha.iloc[0,0]
    elif metodo_de_referencia == 'D':
        corrente_de_referencia = encontrar_numero_maior_proximo(df_d, '3 Condutores', corrente_de_projeto_corrigida)
        linha = df_d[df_d['3 Condutores'] == corrente_de_referencia]
        secao_nominal_cabo = linha.iloc[0,0]

print(f'Corrente de referência: {corrente_de_referencia:.2f}A.\nSeção nominal do cabo: {secao_nominal_cabo}mm².')


#Passo 5: Cálculo da capacidade de condução real do cabo
corrente_z = corrente_de_referencia * FCA * FCT
print(f'Condução real do cabo: {corrente_z:.2f}\n')


#Resumo
resumo = {
    'Corrente de Projeto': f'{corrente_de_projeto:.2f} A',
    'Corrente de Projeto Corrigida': f'{corrente_de_projeto_corrigida:.2f} A',
    'Temperatura do ambiente': str(temperatura)+' °C',
    'Quantidade de circuitos': qtd_circuitos_cabmult,
    'FCT': FCT,
    'FCA': FCA,
    'Tipo de condutor': tipo_condutor.upper(),
    'Corrente de referência': f'{corrente_de_referencia:.2f} A',
    'Corrente real do cabo': f'{corrente_z:.2f} A',
    'Seção Nominal do cabo': f'{secao_nominal_cabo:.2f} mm²'
}
df_resumo = pd.DataFrame([resumo]).T

print('######## Resumo de Cálculo ########')
print(df_resumo)
print("\n")