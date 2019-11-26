########################################################################################################################
# BIBLIOTECAS UTILIZADAS NO PROGRAMA
########################################################################################################################

import numpy as np
import matplotlib.pyplot as plt
import math as math
import xml.dom.minidom
import time
import sys
import csv

#----------------------------------------------------------------------------------------------------------------------#

########################################################################################################################
# VETORES DE NOMES UTILIZADOS NO PROGRAMA
########################################################################################################################

# NOME DO ARQUIVO XML PARA LER
ARQUIVO_XML = 'ConfigCattleMobility.xml'

# NOMES DAS AREAS
NOMES_DAS_AREAS = ['PASTO ','ÁGUA  ','COCHO ','SOMBRA']

# NOMES DOS COMPORTAMENTOS
NOMES_DOS_COMPORTAMENTOS = ['ANDANDO    ','CORRENDO   ','DEITADO    ','ALIMENTANDO']

# NOMES DOS GRAFICOS
NOMES_DOS_GRAFICOS = ['TRAJETORIA PERCORRIDA PELO GADO 1','TRAJETORIA PERCORRIDA PELO GADO 2',
                     'TRAJETORIA PERCORRIDA PELO GADO 3','TRAJETORIA PERCORRIDA PELO GADO 4',
                     'TRAJETORIA PERCORRIDA PELO GADO 5','TRAJETORIA PERCORRIDA PELO GADO 6',
                     'TRAJETORIA PERCORRIDA PELO GADO 7','TRAJETORIA PERCORRIDA PELO GADO 8',
                     'TRAJETORIA PERCORRIDA PELO GADO 9','TRAJETORIA PERCORRIDA PELO GADO 10']

# NOMES DOS RELEVOS
NOMES_DOS_RELEVOS = ['     0 - 56.25m',' 56.25 - 112.5m','112.5 - 168.75m','  168.75 - 225m']

# NOMES DOS ARQUIVOS .LOG PARA LER
ARQUIVOS = ['trace_position_0.log','trace_position_1.log','trace_position_2.log','trace_position_3.log','trace_position_4.log',
            'trace_position_5.log','trace_position_6.log', 'trace_position_7.log', 'trace_position_8.log', 'trace_position_9.log']

# NOMES DOS ARQUIVOS .CSV PARA ESCREVER
ARQUIVOS_ESCREVER = ['Distribuição_1_Distancia_Total.csv','Distribuição_1_Custo_Energetico_EM.csv','Distribuição_1_Custo_Energetico_ELL.csv']

#----------------------------------------------------------------------------------------------------------------------#

########################################################################################################################
# VETORES UTILIZADOS NO PROGRAMA
########################################################################################################################

# VETORES UTILIZADOS PARA O DESLOCAMENTO HORIZONTAL POR GADO
DESLOCAMENTO_HORIZONTAL_1, DESLOCAMENTO_HORIZONTAL_2, DESLOCAMENTO_HORIZONTAL_3, DESLOCAMENTO_HORIZONTAL_4, DESLOCAMENTO_HORIZONTAL_5 = [], [], [], [], []
DESLOCAMENTO_HORIZONTAL_6, DESLOCAMENTO_HORIZONTAL_7, DESLOCAMENTO_HORIZONTAL_8, DESLOCAMENTO_HORIZONTAL_9, DESLOCAMENTO_HORIZONTAL_10 = [], [], [], [], []


# VETORES UTILIZADOS PARA O DESLOCAMENTO VERTICAL POR GADO
DESLOCAMENTO_VERTICAL_1, DESLOCAMENTO_VERTICAL_2, DESLOCAMENTO_VERTICAL_3, DESLOCAMENTO_VERTICAL_4, DESLOCAMENTO_VERTICAL_5 = [], [], [], [], []
DESLOCAMENTO_VERTICAL_6, DESLOCAMENTO_VERTICAL_7, DESLOCAMENTO_VERTICAL_8, DESLOCAMENTO_VERTICAL_9, DESLOCAMENTO_VERTICAL_10 = [], [], [], [], []

# VETORES UTILIZADOS PARA O CUSTO ENERGETICO 'EM' POR GADO
Custo_Energetico_EM_1, Custo_Energetico_EM_2, Custo_Energetico_EM_3, Custo_Energetico_EM_4, Custo_Energetico_EM_5 = [], [], [], [], []
Custo_Energetico_EM_6, Custo_Energetico_EM_7, Custo_Energetico_EM_8, Custo_Energetico_EM_9, Custo_Energetico_EM_10 = [], [], [], [], []

# VETORES UTILIZADOS PARA O CUSTO ENERGETICO 'ELL' POR GADO

Custo_Energetico_ELL_1, Custo_Energetico_ELL_2, Custo_Energetico_ELL_3, Custo_Energetico_ELL_4, Custo_Energetico_ELL_5 = [], [], [], [], []
Custo_Energetico_ELL_6, Custo_Energetico_ELL_7, Custo_Energetico_ELL_8, Custo_Energetico_ELL_9, Custo_Energetico_ELL_10 = [], [], [], [], []

#----------------------------------------------------------------------------------------------------------------------#

########################################################################################################################
# DECLARAÇÕES DAS MATRIZES DE MARKOV (4X4)
#########################################################################################################################

# MATRIZ DE TRANSIÇÕES DAS AREAS
n = (4,4)
MATRIZ_MARKOV_AREA_0 = np.zeros(n,dtype=np.float)
MATRIZ_MARKOV_AREA_1 = np.zeros(n,dtype=np.float)
MATRIZ_MARKOV_AREA_2 = np.zeros(n,dtype=np.float)

# MATRIZ DE TRANSIÇÕES DOS COMPORTAMENTOS
n = (4,4)
MATRIZ_MARKOV_COMPORTAMENTOS_0 = np.zeros(n,dtype=np.float)
MATRIZ_MARKOV_COMPORTAMENTOS_1 = np.zeros(n,dtype=np.float)
MATRIZ_MARKOV_COMPORTAMENTOS_2 = np.zeros(n,dtype=np.float)
MATRIZ_MARKOV_COMPORTAMENTOS_3 = np.zeros(n,dtype=np.float)

#----------------------------------------------------------------------------------------------------------------------#

########################################################################################################################
# FUNÇÕES UTILIZADAS NO PROGRAMA
########################################################################################################################

# FUNÇÃO PARA DESENHAR AS ÁREAS
def SubArea():
    plt.plot(Px,Py,'k--')
    plt.plot(A_Ax,A_Ay,'b-.')
    plt.plot(Ax,Ay,'b:')
    plt.plot(A_Cx,A_Cy,'g-.')
    plt.plot(Cx,Cy,'g:')
    plt.plot(Sx,Sy,'r-.')
    plt.annotate("PASTO",xy=(225,225),xytext=(214,219))
    plt.annotate("AGUA",xy=(0,105),xytext=(1,116))
    plt.annotate("COCHO",xy=(115,0),xytext=(116,1))
    plt.annotate("SOMBRA",xy=(112.5,112.5),xytext=(113,108))
    plt.xlabel('ÁREA (m)')
    plt.ylabel('ÁREA (m)')
    plt.xlim(-3,228)
    plt.ylim(-3,228)
    plt.xticks(Eixo_X)
    plt.yticks(Eixo_Y)
    plt.grid(True)

########################################################################################################################

# FUNÇÃO PARA LER UM ARQUIVO
def LER_ARQUIVO(Arquivo):
    X, Y = [], []
    f = open(Arquivo,'r')
    for linha in f:
        linha = linha.strip()
        x,y = linha.split(';')
        X.append(float(x))
        Y.append(float(y))
    f.close()
    return X,Y

########################################################################################################################

# FUNÇÃO PARA GUARDAR EM UM ARQUIVO
def CARGAR_ARQUIVO (Arquivo,Vetor):
    f = open(Arquivo,'w')
    try:
       writer = csv.writer(f)
       for i in range(len(Vetor)):
           writer.writerow((i+1,Vetor[i]))
    finally:
       f.close()

########################################################################################################################

# FUNÇÃO PARA MOSTRAR POSIÇÕES X;Y
def MOSTRAR_POSIÇÕES(X,Y,gado):
    print("")
    print("POSIÇÕES DO PERCORRIDO DO GADO LEITEIRO :", gado + 1)
    for i in range(len(X)):
        print(" ",i+1,"--> X :", X[i], " Y :", Y[i])
########################################################################################################################

# FUNÇÃO PARA CALCULAR A EQUAÇÃO DA RETA
def CALCULO_EQUAÇÃO_RETA(x1,y1,x2,y2):
    if (x2 - x1) !=0:
        m = (y2 - y1) / (x2 - x1)
    else:
        m = 0
    b = y1 - (m * x1)
    return m,b
########################################################################################################################

# FUNÇÃO PARA CALCULAR TODOS OS PONTOS DA TRAJETORIA
def TRAJETORIA(m,b,x1,y1,x2,y2,Eixo_X,Eixo_Y):
    x = []
    y = []
    x.append(x1)
    y.append(y1)
    if m != 0 or (y2 - y1) == 0:
        for i in range(len(Eixo_X)):
            if x1 >= Eixo_X[i] and x1 < Eixo_X[i + 1]:
                j = i + 1
                while x2 > Eixo_X[j]:
                    valor = (m * Eixo_X[j]) + b
                    y.append(valor)
                    x.append(Eixo_X[j])
                    j = j + 1
                break
    if y2 >= y1:
        for i in range(len(Eixo_Y)):
            if y1 >= Eixo_Y[i] and y1 < Eixo_Y[i + 1]:
                j = i + 1
                while y2 > Eixo_Y[j]:
                    if m != 0:
                        valor = (Eixo_Y[j] - b)/m
                    else:
                        valor = x1
                    x.append(valor)
                    y.append(Eixo_Y[j])
                    j = j + 1
                break
    else:
        for i in range(len(Eixo_Y)):
            if y2 >= Eixo_Y[i] and y2 < Eixo_Y[i + 1]:
                j = i + 1
                while y1 > Eixo_Y[j]:
                    if m != 0:
                        valor = (Eixo_Y[j] - b)/m
                    else:
                        valor = x1
                    x.append(valor)
                    y.append(Eixo_Y[j])
                    j = j + 1
                break
    x.append(x2)
    y.append(y2)
    return x,y
########################################################################################################################

# FUNÇÃO PARA REMOVER PONTOS REPETIDOS
def REMOVER_REPETIDOS(Lista):
    l = []
    for i in Lista:
        if i not in l:
            l.append(i)
    return l
########################################################################################################################

# FUNÇÃO PARA ORDENAR
def BUBBLE_SORT(lista,y):
    elementos = len(lista)-1
    ordenado = False
    while not ordenado:
        ordenado = True
        for i in range(elementos):
            if lista[i] > lista[i+1]:
                lista[i], lista[i+1] = lista[i+1],lista[i]
                y[i], y[i+1] = y[i+1],y[i]
                ordenado = False
    return lista,y
########################################################################################################################

# FUNÇÃO PARA PROCURAR AREA DE RELEVO
def PROCURAR_AREA_DE_RELEVO(x,y,Eixo_X,Eixo_Y,flag):
    if flag == 0:
        for i in range(len(Eixo_X)):
            if x >= Eixo_X[i] and x <= Eixo_X[i+1]:
                coluna = i
                break
        for i in range(len(Eixo_Y)):
            if y >= Eixo_Y[i] and y <= Eixo_Y[i+1]:
                fila = i
                break
    else:
        i = len(Eixo_X) - 1
        while i > 0:
            if x <= Eixo_X[i] and x > Eixo_X[i-1]:
                coluna = i - 1
                break
            i = i - 1
        i = len(Eixo_Y) - 1
        while i > 0:
            if y <= Eixo_Y[i] and y >= Eixo_Y[i-1]:
                fila = i - 1
                break
            i = i - 1
    return fila,coluna
########################################################################################################################

# FUNÇÃO PARA CALCULAR A DISTANCIA
def CALCULO_DISTANCIA(X,Y):
    DISTANCIA = [0]*(len(X)-1)
    for i in range(len(X)-1):
        x1 = X[i]
        x2 = X[i+1]
        y1 = Y[i]
        y2 = Y[i+1]
        DISTANCIA[i] = (math.sqrt(pow((x2-x1),2) + pow((y2-y1),2)))
        DISTANCIA[i] = DISTANCIA[i]/1000
    return DISTANCIA
########################################################################################################################

# FUNÇÃO PARA MOSTRAR POSIÇÕES X;Y
def MOSTRAR_DISTANCIA(D,gado):
    print("")
    print("DISTANCIA DO PERCORRIDO DO GADO LEITEIRO :", gado + 1)
    for i in range(len(D)):
        print(" ",i+1,"--> Distancia :",D[i],"Km")
########################################################################################################################

# FUNÇÃO PARA CALCULAR O CUSTO ENERGETICO EM
def CALCULO_CUSTO_ENERGETICO_EM(Peso,D_Horizontal,D_Vertical,C_Horizontal,C_Vertical):
    CUSTO = [0] * len(D_Horizontal)
    for i in range(len(D_Horizontal)):
        if D_Vertical[i] != 0:
            if D_Vertical[i] > 0:
                D_Vertical[i] = D_Horizontal[i]*(D_Vertical[i]/100)
            else:
                D_Vertical[i] = D_Horizontal[i] * ((-1 * D_Vertical[i]) / 100)
        CUSTO[i] = (Peso * ((C_Horizontal * D_Horizontal[i])+(C_Vertical * D_Vertical[i])))
    return CUSTO
########################################################################################################################

# FUNÇÃO PARA MOSTRAR O CUSTO ENERGETICO EM
def MOSTRAR_CUSTO_ENERGETICO_EM(C,gado):
    print("")
    print("CUSTO ENERGETICO 'EM' DO GADO LEITEIRO :", gado + 1)
    for i in range(len(C)):
        print(" ",i+1,"--> Custo Energetico :",C[i],"Mcal")
########################################################################################################################

# FUNÇÃO PARA CALCULAR O CUSTO ENERGETICO ELL
def CALCULO_CUSTO_ENERGETICO_ELL(Custo_Enegetico_EM):
    Constante = 0.644
    CUSTO = [0] * len(Custo_Enegetico_EM)
    for i in range(len(Custo_Enegetico_EM)):
        CUSTO[i] = Custo_Enegetico_EM[i] * Constante
    return CUSTO
########################################################################################################################

# FUNÇÃO PARA MOSTRAR O CUSTO ENERGETICO ELL
def MOSTRAR_CUSTO_ENERGETICO_ELL(C,gado):
    print("")
    print("CUSTO ENERGETICO 'ELL' DO GADO LEITEIRO :", gado + 1)
    for i in range(len(C)):
        print(" ",i+1,"--> Custo Energetico :",C[i],"Mcal")
########################################################################################################################

# FUNÇÃO PARA MOSTRAR A MATRIZ DE MARKOV DE ÁREAS
def MOSTRAR_MATRIZ_MARKOV_AREAS(M):
    tamanho = np.shape(M)
    print("      ",NOMES_DAS_AREAS[0]," ",NOMES_DAS_AREAS[1]," ",NOMES_DAS_AREAS[2]," ",NOMES_DAS_AREAS[3])
    for i in range(tamanho[0]):
        print(NOMES_DAS_AREAS[i], end="  ")
        for j in range(tamanho[1]):
            print(M[i][j],end="      ")
        print('\n')
########################################################################################################################

# FUNÇÃO PARA MOSTRAR AS MATRIZES DE MARKOV DOS COMPORTAMENTOS
def MOSTRAR_MATRIZ_MARKOV_COMPORTAMENTOS(M):
    tamanho = np.shape(M)
    print("            ",NOMES_DOS_COMPORTAMENTOS[0],NOMES_DOS_COMPORTAMENTOS[1],NOMES_DOS_COMPORTAMENTOS[2],NOMES_DOS_COMPORTAMENTOS[3])
    for i in range(tamanho[0]):
        print(NOMES_DOS_COMPORTAMENTOS[i], end="   ")
        for j in range(tamanho[1]):
            print(M[i][j],end="          ")
        print('\n')
########################################################################################################################

# FUNÇÃO PARA MOSTRAR AS MATRIZES DE RELEVOS
def MOSTRAR_MATRIZ_RELEVO(M):
    tamanho = np.shape(M)
    print("            ",NOMES_DOS_RELEVOS[0]," ",NOMES_DOS_RELEVOS[1]," ",NOMES_DOS_RELEVOS[2]," ",NOMES_DOS_RELEVOS[3])
    for i in range(tamanho[0]):
        print(NOMES_DOS_RELEVOS[i], end="        ")
        for j in range(tamanho[1]):
            print(M[i][j],end="             ")
        print('\n')

########################################################################################################################

# FUNÇÃO PARA MOSTRAR AS MATRIZES DE TEMPERATURA
def MOSTRAR_MATRIZ_TEMPERATURA(M,Inicio,Fim):
    tamanho = np.shape(M)
    horas = np.arange(Inicio, Fim+1, 1)
    print(end="Horas --> ")
    for i in range(tamanho[1]):
        print(horas[i],"-",horas[i+1], end="         ")
    print('\n')
    for i in range(tamanho[0]):
        if i == 0:
            print("Tmin --> ",end=" ")
        else:
            print("Tmax --> ",end=" ")
        for j in range(tamanho[1]):
            print(M[i][j],end="           ")
        print('\n')
########################################################################################################################

# FUNÇÃO PARA TROCAR DOIS ELEMENTOS
def TROCA(x,y):
    aux = x
    x = y
    y = aux
    return x,y
########################################################################################################################
#----------------------------------------------------------------------------------------------------------------------#

########################################################################################################################
# PROGRAMA PRINCIPAL
########################################################################################################################

# LER ARQUIVO DE CONFIGURAÇÃO XML
print("***************************************************************************************************************")
print("INICIO DA LEITURA DO ARQUIVO DE CONFIGURAÇÃO XML")
Tempo_Inicio_Leitura = time.time()
if __name__=="__main__":
    x = xml.dom.minidom.parse(ARQUIVO_XML)
    root = x.documentElement
    print("|-> %s" % root.nodeName)
    filhos1 = [no for no in root.childNodes if no.nodeType == x.ELEMENT_NODE]
    for pai in filhos1:
        print("")
        print("|--> %s" % pai.nodeName)
        if pai.nodeName == 'initialParams':
            print("|---> areaTypeID : %s" % pai.getAttribute('areaTypeID'))
            print("|---> behaviorID : %s" % pai.getAttribute('behaviorID'))

        if pai.nodeName == 'leaderGroup':
            print("|---> percentValue : %s" % pai.getAttribute('percentValue'))

        if pai.nodeName == 'matrixTemperature':
            print("|---> temperatureMatrixID : %s" % pai.getAttribute('temperatureMatrixID'))
            n_temperatura = int(pai.getAttribute('temperatureMatrixID'))

        if pai.nodeName == 'matrixRelief':
            print("|---> reliefMatrixID : %s" % pai.getAttribute('reliefMatrixID'))
            n_relevo = int(pai.getAttribute('reliefMatrixID'))

        if pai.nodeName == 'nodesNumber':
            print("|---> number : %s" % pai.getAttribute('number'))
            QUANTIDADE_DE_GADOS = int(pai.getAttribute('number'))

        if pai.nodeName == 'horizontalConstant':
            print("|---> constant : %s" % pai.getAttribute('constant'))
            Constante_Horizontal = float(pai.getAttribute('constant'))

        if pai.nodeName == 'verticalConstant':
            print("|---> constant : %s" % pai.getAttribute('constant'))
            Constante_Vertical = float(pai.getAttribute('constant'))

        if pai.nodeName == 'divisionsX':
            print("|---> axisX : %s" % pai.getAttribute('axisX'))
            n_x = int(pai.getAttribute('axisX'))

        if pai.nodeName == 'divisionsY':
            print("|---> axisY : %s" % pai.getAttribute('axisY'))
            n_y = int(pai.getAttribute('axisY'))

        if pai.nodeName == 'initialTime':
            print("|---> initial : %s" % pai.getAttribute('initial'))
            Hora_Inicio = int(pai.getAttribute('initial'))

        if pai.nodeName == 'finalTime':
            print("|---> final : %s" % pai.getAttribute('final'))
            Hora_Final = int(pai.getAttribute('final'))

        if pai.nodeName == "DairyCattleWeights":
            PESO_DO_GADO = [0] * QUANTIDADE_DE_GADOS
            filhos2 = [no for no in pai.childNodes if no.nodeType == x.ELEMENT_NODE]
            for filho in filhos2:
                print("|---> %s" % filho.nodeName)
                print("|-----> weightID : %s" % filho.getAttribute('weightID'))
                print("|-----> weight : %s" % filho.getAttribute('weight'))
                PESO_DO_GADO[int(filho.getAttribute('weightID'))]=float(filho.getAttribute('weight'))

        if pai.nodeName == "behaviors":
            filhos2 = [no for no in pai.childNodes if no.nodeType == x.ELEMENT_NODE]
            for filho in filhos2:
                print("|---> %s" % filho.nodeName)
                print("|-----> behaviorID : %s" % filho.getAttribute('behaviorID'))
                print("|-----> name : %s" % filho.getAttribute('name'))
                print("|-----> minSpeed : %s" % filho.getAttribute('minSpeed'))
                print("|-----> maxSpeed : %s" % filho.getAttribute('maxSpeed'))

        if pai.nodeName == "areaTypes":
            filhos2 = [no for no in pai.childNodes if no.nodeType == x.ELEMENT_NODE]
            for filho in filhos2:
                print("|---> %s" % filho.nodeName)
                print("|-----> areaTypeID : %s" % filho.getAttribute('areaTypeID'))
                areaTypeID = int(filho.getAttribute('areaTypeID'))
                print("|-----> name : %s" % filho.getAttribute('name'))
                print("|-----> xMin : %s" % filho.getAttribute('xMin'))
                print("|-----> yMin : %s" % filho.getAttribute('yMin'))
                print("|-----> zMin : %s" % filho.getAttribute('zMin'))
                print("|-----> xMax : %s" % filho.getAttribute('xMax'))
                print("|-----> yMax : %s" % filho.getAttribute('yMax'))
                print("|-----> zMax : %s" % filho.getAttribute('zMax'))
                print("|-----> behaviorsMatrixID : %s" % filho.getAttribute('behaviorsMatrixID'))
                if areaTypeID == 0:
                    xMin = int(filho.getAttribute('xMin'))
                    yMin = int(filho.getAttribute('yMin'))
                    zMin = int(filho.getAttribute('zMin'))
                    xMax = int(filho.getAttribute('xMax'))
                    yMax = int(filho.getAttribute('yMax'))
                    zMax = int(filho.getAttribute('zMax'))

        if pai.nodeName == "temperatureMatrices":
            filhos2 = [no for no in pai.childNodes if no.nodeType == x.ELEMENT_NODE]
            Quantidade_Matriz_Temperatura = len(filhos2)
            for filho in filhos2:
                print("|---> %s" % filho.nodeName)
                print("|-----> temperatureMatrixID : %s" % filho.getAttribute('temperatureMatrixID'))
                print("|-----> type : %s" % filho.getAttribute('type'))
                filhos3 = [no for no in filho.childNodes if no.nodeType == x.ELEMENT_NODE]
                print("Fila = ", len(filhos3))
                i = 0
                for x in filhos3:
                    print("|---> %s" % x.nodeName)
                    filhos4 = [no for no in x.childNodes if no.nodeType == x.ELEMENT_NODE]
                    print("Coluna = ", len(filhos4))
                    j = 0
                    for y in filhos4:
                        print("|----> %s" % y.nodeName)
                        print("|-----> value: %s" % y.getAttribute('value'))
                        # Preencher as Matrizes de Temperatura
                        if filho.getAttribute('temperatureMatrixID') == '0':
                            if i == 0 and j == 0:
                                MATRIZ_TEMPERATURA_0 = np.zeros((len(filhos3), len(filhos4)), dtype=np.float)
                            MATRIZ_TEMPERATURA_0[i][j] = float(y.getAttribute('value'))
                        elif filho.getAttribute('temperatureMatrixID') == '1':
                            if i == 0 and j == 0:
                                MATRIZ_TEMPERATURA_1 = np.zeros((len(filhos3), len(filhos4)), dtype=np.float)
                            MATRIZ_TEMPERATURA_1[i][j] = float(y.getAttribute('value'))
                        else:
                            if i == 0 and j == 0:
                                MATRIZ_TEMPERATURA_2 = np.zeros((len(filhos3), len(filhos4)), dtype=np.float)
                            MATRIZ_TEMPERATURA_2[i][j] = float(y.getAttribute('value'))
                        j = j + 1
                    i = i + 1

        if pai.nodeName == "reliefMatrices":
            filhos2 = [no for no in pai.childNodes if no.nodeType == x.ELEMENT_NODE]
            Quantidade_Matriz_Relevo = len(filhos2)
            for filho in filhos2:
                print("|---> %s" % filho.nodeName)
                print("|-----> reliefMatrixID : %s" % filho.getAttribute('reliefMatrixID'))
                print("|-----> type : %s" % filho.getAttribute('type'))
                filhos3 = [no for no in filho.childNodes if no.nodeType == x.ELEMENT_NODE]
                print("Fila = ", len(filhos3))
                i = 0
                for x in filhos3:
                    print("|---> %s" % x.nodeName)
                    filhos4 = [no for no in x.childNodes if no.nodeType == x.ELEMENT_NODE]
                    print("Coluna = ", len(filhos4))
                    j = 0
                    for y in filhos4:
                        print("|----> %s" % y.nodeName)
                        print("|-----> value: %s" % y.getAttribute('value'))
                        # Preencher as Matrizes de Relevo
                        if filho.getAttribute('reliefMatrixID') == '0':
                            if i == 0 and j == 0:
                                MATRIZ_RELEVO_0 = np.zeros((len(filhos3),len(filhos4)), dtype=np.float)
                            MATRIZ_RELEVO_0[i][j] = float(y.getAttribute('value'))
                        elif filho.getAttribute('reliefMatrixID') == '1':
                            if i == 0 and j == 0:
                                MATRIZ_RELEVO_1 = np.zeros((len(filhos3),len(filhos4)), dtype=np.float)
                            MATRIZ_RELEVO_1[i][j] = float(y.getAttribute('value'))
                        elif filho.getAttribute('reliefMatrixID') == '2':
                            if i == 0 and j == 0:
                                MATRIZ_RELEVO_2 = np.zeros((len(filhos3),len(filhos4)), dtype=np.float)
                            MATRIZ_RELEVO_2[i][j] = float(y.getAttribute('value'))
                        j = j + 1
                    i = i + 1

        if pai.nodeName == "markovAreaMatrices":
            filhos2 = [no for no in pai.childNodes if no.nodeType == x.ELEMENT_NODE]
            Quantidade_Matriz_Markov_Area = len(filhos2)
            for filho in filhos2:
                print("|---> %s" % filho.nodeName)
                print("|-----> areaMatrixID : %s" % filho.getAttribute('areaMatrixID'))
                print("|-----> type : %s" % filho.getAttribute('type'))
                filhos3 = [no for no in filho.childNodes if no.nodeType == x.ELEMENT_NODE]
                i = 0
                for x in filhos3:
                    print("|---> %s" % x.nodeName)
                    filhos4 = [no for no in x.childNodes if no.nodeType == x.ELEMENT_NODE]
                    j = 0
                    for y in filhos4:
                        print("|----> %s" % y.nodeName)
                        print("|-----> value: %s" % y.getAttribute('value'))
                        # Preencher as Matrizes de Markov das Áreas
                        if filho.getAttribute('areaMatrixID') == '0':
                            MATRIZ_MARKOV_AREA_0[i][j] = float(y.getAttribute('value'))
                        elif filho.getAttribute('areaMatrixID') == '1':
                            MATRIZ_MARKOV_AREA_1[i][j] = float(y.getAttribute('value'))
                        else:
                            MATRIZ_MARKOV_AREA_2[i][j] = float(y.getAttribute('value'))
                        j = j + 1
                    i = i + 1

        if pai.nodeName == "markovBehaviorMatrices":
            filhos2 = [no for no in pai.childNodes if no.nodeType == x.ELEMENT_NODE]
            Quantidade_Matriz_Markov_Comportamento = len(filhos2)
            for filho in filhos2:
                print("|---> %s" % filho.nodeName)
                print("|-----> behaviorMatrixID : %s" % filho.getAttribute('behaviorMatrixID'))
                print("|-----> type : %s" % filho.getAttribute('type'))
                filhos3 = [no for no in filho.childNodes if no.nodeType == x.ELEMENT_NODE]
                i = 0
                for x in filhos3:
                    print("|---> %s" % x.nodeName)
                    filhos4 = [no for no in x.childNodes if no.nodeType == x.ELEMENT_NODE]
                    j = 0
                    for y in filhos4:
                        print("|----> %s" % y.nodeName)
                        print("|-----> value: %s" % y.getAttribute('value'))
                        # Preencher as Matrizes de Markov dos Comportamentos
                        if filho.getAttribute('behaviorMatrixID') == '0':
                            MATRIZ_MARKOV_COMPORTAMENTOS_0[i][j] = float(y.getAttribute('value'))
                        elif filho.getAttribute('behaviorMatrixID') == '1':
                            MATRIZ_MARKOV_COMPORTAMENTOS_1[i][j] = float(y.getAttribute('value'))
                        elif filho.getAttribute('behaviorMatrixID') == '2':
                            MATRIZ_MARKOV_COMPORTAMENTOS_2[i][j] = float(y.getAttribute('value'))
                        else:
                            MATRIZ_MARKOV_COMPORTAMENTOS_3[i][j] = float(y.getAttribute('value'))
                        j = j + 1
                    i = i + 1

Tempo_Fim_Leitura = time.time()
print("")
print("FIN DA LEITURA DO ARQUIVO DE CONFIGURAÇÃO XML")

########################################################################################################################

# VERIFICAR OS NUMEROS DAS DIVISÕES DA ÁREA COM AS AREAS MAXIMAS NO ARQUIVO DE CONFIGURAÇÃO
print("")
if n_x <= xMax and n_y <= yMax:
    print("* VALIDAÇÃO DOS NÚMEROS DAS DIVISÕES DA ÁREA COM OS TAMANHOS DAS ÁREAS MÁXIMAS")
else:
    print("* NÚMEROS DAS DIVISÕES DAS ÁREAS É MAIOR QUE O TAMANHO DAS ÁREAS MÁXIMAS")
    sys.exit()

########################################################################################################################

# VERIFICAR QUE A QUANTIDADE DAS MATRIZES DE RELEVO SEJA COMO MÁXIMO = 3
print("")
if Quantidade_Matriz_Relevo >= 0 and Quantidade_Matriz_Relevo <= 3:
    print("* A QUANTIDADE DE MATRIZES DE RELEVO <= 3")
else:
    print("* A QUANTIDADE DE MATRIZES DE RELEVO > 3")
    sys.exit()

########################################################################################################################

# VERIFICAR QUE O NÚMERO DA MATRIZ DE RELEVO ESTEJA DENTRO DA QUANTIDADE DE MATRIZES DE RELEVO NO ARQUIVO DE CONFIGURAÇÃO
print("")
if n_relevo >= 0 and n_relevo <  Quantidade_Matriz_Relevo:
    print("* O ID DA MATRIZ DE RELEVO ESTÁ DENTRO DAS MATRIZES DE RELEVO ESPECIFICADA NO ARQUIVO DE CONFIGURAÇÃO")
else:
    print("* O ID DA MATRIZ DE RELEVO NÃO ESTÁ DENTRO DAS MATRIZES DE RELEVO ESPECIFICADA NO ARQUIVO DE CONFIGURAÇÃO")
    sys.exit()

########################################################################################################################

# VERIFICAR QUE O NÚMERO DA MATRIZ DE TEMPERATURA ESTEJA DENTRO DA QUANTIDADE DE MATRIZES DE TEMPERATURA NO ARQUIVO DE CONFIGURAÇÃO
print("")
if n_temperatura >= 0 and n_temperatura < Quantidade_Matriz_Temperatura:
    print("* O ID DA MATRIZ DE TEMPERATURA ESTÁ DENTRO DAS MATRIZES DE TEMPERATURA ESPECIFICADA NO ARQUIVO DE CONFIGURAÇÃO")
else:
    print("* O ID DA MATRIZ DE TEMPERATURA NÃO ESTÁ DENTRO DAS MATRIZES DE TEMPERATURA ESPECIFICADA NO ARQUIVO DE CONFIGURAÇÃO")
    sys.exit()

########################################################################################################################

# MOSTRAR A MATRIZ DAS AREAS DE MARKOV LIDA DO ARQUIVO DE CONFIGURAÇÃO
print("***************************************************************************************************************")
print("MATRIZ DE MARKOV PARA AS TRANSIÇÕES DAS ÁREAS")
for i in range(Quantidade_Matriz_Markov_Area):
    print("ID : ",i)
    if i == 0:
        MOSTRAR_MATRIZ_MARKOV_AREAS(MATRIZ_MARKOV_AREA_0)
        filas = MATRIZ_MARKOV_AREA_0.shape[0]
        colunas = MATRIZ_MARKOV_AREA_0.shape[1]
    elif i == 1:
        MOSTRAR_MATRIZ_MARKOV_AREAS(MATRIZ_MARKOV_AREA_1)
        filas = MATRIZ_MARKOV_AREA_1.shape[0]
        colunas = MATRIZ_MARKOV_AREA_1.shape[1]
    else:
        MOSTRAR_MATRIZ_MARKOV_AREAS(MATRIZ_MARKOV_AREA_2)
        filas = MATRIZ_MARKOV_AREA_2.shape[0]
        colunas = MATRIZ_MARKOV_AREA_2.shape[1]

    print("Número de Fila =", filas)
    print("Número de Coluna =", colunas)
    print("------------------------------------------------------------------------------------------------------------")

########################################################################################################################

# MOSTRAR AS MATRIZES DOS COMPORTAMENTOS LIDA DO ARQUIVO DE CONFIGURAÇÃO
print("***************************************************************************************************************")
print("MATRIZ DE MARKOV PARA AS TRANSIÇÕES DOS COMPORTAMENTOS")
for i in range(Quantidade_Matriz_Markov_Comportamento):
    print("ID : ",i)
    print("ÁREA :",NOMES_DAS_AREAS[i])
    if i == 0:
        MOSTRAR_MATRIZ_MARKOV_COMPORTAMENTOS(MATRIZ_MARKOV_COMPORTAMENTOS_0)
        filas = MATRIZ_MARKOV_COMPORTAMENTOS_0.shape[0]
        colunas = MATRIZ_MARKOV_COMPORTAMENTOS_0.shape[1]
    elif i == 1:
        MOSTRAR_MATRIZ_MARKOV_COMPORTAMENTOS(MATRIZ_MARKOV_COMPORTAMENTOS_1)
        filas = MATRIZ_MARKOV_COMPORTAMENTOS_1.shape[0]
        colunas = MATRIZ_MARKOV_COMPORTAMENTOS_1.shape[1]
    elif i == 2:
        MOSTRAR_MATRIZ_MARKOV_COMPORTAMENTOS(MATRIZ_MARKOV_COMPORTAMENTOS_2)
        filas = MATRIZ_MARKOV_COMPORTAMENTOS_2.shape[0]
        colunas = MATRIZ_MARKOV_COMPORTAMENTOS_2.shape[1]
    else:
        MOSTRAR_MATRIZ_MARKOV_COMPORTAMENTOS(MATRIZ_MARKOV_COMPORTAMENTOS_3)
        filas = MATRIZ_MARKOV_COMPORTAMENTOS_3.shape[0]
        colunas = MATRIZ_MARKOV_COMPORTAMENTOS_3.shape[1]

    print("Número de Fila =", filas)
    print("Número de Coluna =", colunas)
    print("------------------------------------------------------------------------------------------------------------")

########################################################################################################################

# MOSTRAR AS MATRIZES DE TEMPERATURA LIDA DO ARQUIVO DE CONFIGURAÇÃO
print("***************************************************************************************************************")
print("MATRIZ DE TEMPERATURA")
for i in range(Quantidade_Matriz_Temperatura):
    print("ID : ",i)
    if i == 0:
        MOSTRAR_MATRIZ_TEMPERATURA(MATRIZ_TEMPERATURA_0,Hora_Inicio,Hora_Final)
        filas = MATRIZ_TEMPERATURA_0.shape[0]
        colunas = MATRIZ_TEMPERATURA_0.shape[1]
    elif i == 1:
        MOSTRAR_MATRIZ_TEMPERATURA(MATRIZ_TEMPERATURA_1,Hora_Inicio,Hora_Fina)
        filas = MATRIZ_TEMPERATURA_1.shape[0]
        colunas = MATRIZ_TEMPERATURA_1.shape[1]
    else:
        MOSTRAR_MATRIZ_TEMPERATURA(MATRIZ_TEMPERATURA_2,Hora_Inicio,Hora_Fina)
        filas = MATRIZ_TEMPERATURA_2.shape[0]
        colunas = MATRIZ_TEMPERATURA_2.shape[1]

    print("Número de Fila =", filas)
    print("Número de Coluna =", colunas)
    print("------------------------------------------------------------------------------------------------------------")

########################################################################################################################

# MOSTRAR AS MATRIZES DE RELEVO LIDA DO ARQUIVO DE CONFIGURAÇÃO
filas_Relevo = [0] * Quantidade_Matriz_Relevo
colunas_Relevo = [0] * Quantidade_Matriz_Relevo
print("***************************************************************************************************************")
print("MATRIZES DE RELEVO")
for i in range(Quantidade_Matriz_Relevo):
    print("ID : ", i)
    if i == 0:
        MOSTRAR_MATRIZ_RELEVO(MATRIZ_RELEVO_0)
        filas_Relevo[i] = MATRIZ_RELEVO_0.shape[0]
        colunas_Relevo[i] = MATRIZ_RELEVO_0.shape[1]
    elif i == 1:
        MOSTRAR_MATRIZ_RELEVO(MATRIZ_RELEVO_1)
        filas_Relevo[i] = MATRIZ_RELEVO_1.shape[0]
        colunas_Relevo[i] = MATRIZ_RELEVO_1.shape[1]
    else:
        MOSTRAR_MATRIZ_RELEVO(MATRIZ_RELEVO_2)
        filas_Relevo[i] = MATRIZ_RELEVO_2.shape[0]
        colunas_Relevo[i] = MATRIZ_RELEVO_2.shape[1]

    print("Número de Fila =", filas_Relevo[i])
    print("Número de Coluna =", colunas_Relevo[i])
    print("------------------------------------------------------------------------------------------------------------")

########################################################################################################################

# SELECCIONAR A MATRIZ DE RELEVO SEGUNDO O ARQUIVO DE CONFIGURAÇÃO
ff = filas_Relevo[n_relevo]
cc = colunas_Relevo[n_relevo]
MATRIZ_RELEVO = np.zeros((ff, cc), dtype=np.float)
if n_relevo == 0:
    MATRIZ_RELEVO = MATRIZ_RELEVO_0
elif n_relevo == 1:
    MATRIZ_RELEVO = MATRIZ_RELEVO_1
else:
    MATRIZ_RELEVO = MATRIZ_RELEVO_2

########################################################################################################################

# VERIFICAR TAMANHO DA MATRIZ DE RELEVO COM OS NUMEROS DAS DIVISÕES DA ÁREA
print("")
if filas_Relevo[n_relevo] == n_x and colunas_Relevo[n_relevo] == n_y:
    print("* VALIDAÇÃO DO TAMANHO DA MATRIZ DE RELEVO COM OS NÚMEROS DAS DIVISÕES DA ÁREA")
else:
    print("* TAMANHO DA MATRIZ DE RELEVO É DIFERENTE DOS NÚMEROS DAS DIVISÕES DA ÁREA")
    sys.exit()

########################################################################################################################

# CONFIGURAÇÕES DAS DIVISÕES DOS EIXOS
paso_x = (xMax - xMin) / n_x
print("")
print("CONFIGURAÇÃO DAS DIVISÕES DO EIXO X")
print("Paso X -->", paso_x)
Eixo_X = np.arange(xMin, xMax + paso_x, paso_x)
print("Eixo X --> ", Eixo_X)
Tamanho_Eixo_X = len(Eixo_X)
print("Quantidade de Divisões no Eixo X -->", Tamanho_Eixo_X)
paso_y = (yMax - yMin) / n_y
print("------------------------------------------------------------------------------------------------------------")
print("")
print("CONFIGURAÇÃO DAS DIVISÕES DO EIXO Y")
print("Paso Y -->", paso_y)
Eixo_Y = np.arange(yMin, yMax + paso_y, paso_y)
print("Eixo Y --> ", Eixo_Y)
Tamanho_Eixo_Y = len(Eixo_Y)
print("Quantidade de Divisões no Eixo Y -->", Tamanho_Eixo_Y)

########################################################################################################################

# LER ARQUIVOS DAS ÁREAS PARA CARREGAR OS VETORES E DESENHAR
Px, Py, Ax, Ay, A_Ax, A_Ay, Cx, Cy, A_Cx, A_Cy, Sx, Sy = [],[],[],[],[],[],[],[],[],[],[],[]

Px, Py = LER_ARQUIVO('Pasto.txt')
Ax, Ay = LER_ARQUIVO('Agua.txt')
A_Ax, A_Ay = LER_ARQUIVO('Area_Agua.txt')
Cx, Cy = LER_ARQUIVO('Cocho.txt')
A_Cx, A_Cy = LER_ARQUIVO('Area_Cocho.txt')
Sx, Sy = LER_ARQUIVO('Sombra.txt')

########################################################################################################################
Tempo_Inicio = time.time()
# CALCULOS DAS DISTANCIAS E DOS CUSTOS ENERGETICOS POR GADO
for i in range(len(PESO_DO_GADO)):
    X, Y = [], []
    '''
    print("")
    print("***************************************************************************************************************")
    print("INFORMAÇÕES DO GADO :",i+1)
    print("")
    print(" Peso =", PESO_DO_GADO[i])
    '''
    X, Y = LER_ARQUIVO(ARQUIVOS[i])
    #MOSTRAR_POSIÇÕES(X, Y, i)
    #print("------------------------------------------------------------------------------------------------------------")
    ########################################################################################################################
    # CALCULO DOS CUSTOS ENERGETICOS NOS GADOS LEITEIROS
    SubArea()
    for j in range(len(X)-1):
        x1 = X[j]
        y1 = Y[j]
        x2 = X[j+1]
        y2 = Y[j+1]
        # TRATAMENTO DA RETA ENTRE DOIS PONTOS
        if x1 <= x2 and y1 <= y2:
            flag = 0
        elif x1 > x2 and y1 > y2:
            flag = 0
            x1, x2 = TROCA(x1, x2)
            y1, y2 = TROCA(y1, y2)
        elif x1 > x2 and y1 < y2:
            flag = 1
            x1, x2 = TROCA(x1, x2)
            y1, y2 = TROCA(y1, y2)
        elif x1 < x2 and y1 > y2:
            flag = 1
        # CALCULO DAS EQUAÇÕES DAS RETAS
        m, b = CALCULO_EQUAÇÃO_RETA(x1, y1, x2, y2)
        '''
        print("")
        if m == 0:
            print("Equação da Reta: Y =",b)
        else:
            if b > 0:
                print("Equação da Reta: Y =", m, "X +",b)
            elif b == 0:
                print("Equação da Reta: Y =", m,"X")
            else:
                print("Equação da Reta: Y =", m, "X", b)
        '''
        ########################################################################################################################
        # GRAFICO DOS PONTOS
        PX = [x1, x2]
        PY = [y1, y2]
        plt.plot(PX, PY, color='blue')
        plt.plot(PX, PY, 'o', color='blue')
        plt.title(NOMES_DOS_GRAFICOS[i])
        ########################################################################################################################
        # CALCULO DA TRAJETORIA
        x = []
        y = []
        x, y = TRAJETORIA(m, b, x1, y1, x2, y2, Eixo_X, Eixo_Y)
        if flag == 0:
            x.sort()
            y.sort()
        else:
            x, y = BUBBLE_SORT(x, y)
        if m != 0:
            x = REMOVER_REPETIDOS(x)
            y = REMOVER_REPETIDOS(y)
        #print("PONTOS EM X -->", x)
        #print("PONTOS EM Y -->", y)
        plt.plot(x, y, '.', color='black')
        ########################################################################################################################
        # PROCURAR AREA DE RELEVO E DESLOCAMENTO VERTICAL
        DESLOCAMENTO_VERTICAL = [0] * (len(x) - 1)
        for k in range(len(x)):
            ii, jj = PROCURAR_AREA_DE_RELEVO(x[k], y[k], Eixo_X, Eixo_Y,flag)
            '''
            print("-----------------------------------------------------------------------------------------------------------")
            print("PONTO -> (", x[k], ";", y[k], ")")
            print("AREA DE RELEVO --> i =", ii, ",j =", jj)
            print("RELEVO =", MATRIZ_RELEVO[ii][jj],"%")
            '''
            if k != 0:
                DESLOCAMENTO_VERTICAL[k - 1] = MATRIZ_RELEVO[ii][jj]
        ########################################################################################################################
        # DESLOCAMENTO HORIZONTAL
        DESLOCAMENTO_HORIZONTAL = CALCULO_DISTANCIA(x, y)
        '''
        print("")
        print("DESLOCAMENTO HORIZONTAL -->",DESLOCAMENTO_HORIZONTAL)
        print("")
        print("RELEVO -->", DESLOCAMENTO_VERTICAL)
        '''
        ########################################################################################################################
        # CUSTO ENERGETICO EM
        CUSTO_ENERGETICO_EM = np.zeros(len(DESLOCAMENTO_HORIZONTAL))
        CUSTO_ENERGETICO_EM = CALCULO_CUSTO_ENERGETICO_EM(PESO_DO_GADO[i], DESLOCAMENTO_HORIZONTAL, DESLOCAMENTO_VERTICAL, Constante_Horizontal, Constante_Vertical)
        '''
        print("")
        print("CUSTO ENERGETICO 'EM' -->",CUSTO_ENERGETICO_EM)
        '''
        ########################################################################################################################
        # CUSTO ENERGETICO ELL
        CUSTO_ENERGETICO_ELL = np.zeros(len(DESLOCAMENTO_HORIZONTAL))
        CUSTO_ENERGETICO_ELL = CALCULO_CUSTO_ENERGETICO_ELL(CUSTO_ENERGETICO_EM)
        '''
        print("")
        print("CUSTO ENERGETICO 'ELL' -->",CUSTO_ENERGETICO_ELL)
        '''
        soma_horizontal = np.sum(DESLOCAMENTO_HORIZONTAL)
        soma_vertical = np.sum(DESLOCAMENTO_VERTICAL)
        soma_em = np.sum(CUSTO_ENERGETICO_EM)
        soma_ell = np.sum(CUSTO_ENERGETICO_ELL)
        if i == 0:
            DESLOCAMENTO_HORIZONTAL_1.append(soma_horizontal)
            DESLOCAMENTO_VERTICAL_1.append(soma_vertical)
            Custo_Energetico_EM_1.append(soma_em)
            Custo_Energetico_ELL_1.append(soma_ell)
        elif i == 1:
            DESLOCAMENTO_HORIZONTAL_2.append(soma_horizontal)
            DESLOCAMENTO_VERTICAL_2.append(soma_vertical)
            Custo_Energetico_EM_2.append(soma_em)
            Custo_Energetico_ELL_2.append(soma_ell)
        elif i==2:
            DESLOCAMENTO_HORIZONTAL_3.append(soma_horizontal)
            DESLOCAMENTO_VERTICAL_3.append(soma_vertical)
            Custo_Energetico_EM_3.append(soma_em)
            Custo_Energetico_ELL_3.append(soma_ell)
        elif i==3:
            DESLOCAMENTO_HORIZONTAL_4.append(soma_horizontal)
            DESLOCAMENTO_VERTICAL_4.append(soma_vertical)
            Custo_Energetico_EM_4.append(soma_em)
            Custo_Energetico_ELL_4.append(soma_ell)
        elif i==4:
            DESLOCAMENTO_HORIZONTAL_5.append(soma_horizontal)
            DESLOCAMENTO_VERTICAL_5.append(soma_vertical)
            Custo_Energetico_EM_5.append(soma_em)
            Custo_Energetico_ELL_5.append(soma_ell)
        elif i==5:
            DESLOCAMENTO_HORIZONTAL_6.append(soma_horizontal)
            DESLOCAMENTO_VERTICAL_6.append(soma_vertical)
            Custo_Energetico_EM_6.append(soma_em)
            Custo_Energetico_ELL_6.append(soma_ell)
        elif i==6:
            DESLOCAMENTO_HORIZONTAL_7.append(soma_horizontal)
            DESLOCAMENTO_VERTICAL_7.append(soma_vertical)
            Custo_Energetico_EM_7.append(soma_em)
            Custo_Energetico_ELL_7.append(soma_ell)
        elif i==7:
            DESLOCAMENTO_HORIZONTAL_8.append(soma_horizontal)
            DESLOCAMENTO_VERTICAL_8.append(soma_vertical)
            Custo_Energetico_EM_8.append(soma_em)
            Custo_Energetico_ELL_8.append(soma_ell)
        elif i==8:
            DESLOCAMENTO_HORIZONTAL_9.append(soma_horizontal)
            DESLOCAMENTO_VERTICAL_9.append(soma_vertical)
            Custo_Energetico_EM_9.append(soma_em)
            Custo_Energetico_ELL_9.append(soma_ell)
        else:
            DESLOCAMENTO_HORIZONTAL_10.append(soma_horizontal)
            DESLOCAMENTO_VERTICAL_10.append(soma_vertical)
            Custo_Energetico_EM_10.append(soma_em)
            Custo_Energetico_ELL_10.append(soma_ell)
    plt.savefig(NOMES_DOS_GRAFICOS[i])
    plt.cla()
plt.close()
print("***************************************************************************************************************")
Tempo_Fim = time.time()

########################################################################################################################

# CALCULO DA DISTANCIA TOTAL POR GADO LEITEIRO
DISTANCIA_TOTAL = [0] * len(PESO_DO_GADO)
for i in range(len(DISTANCIA_TOTAL)):
    if i==0:
        soma = np.sum(DESLOCAMENTO_HORIZONTAL_1)
    elif i==1:
        soma = np.sum(DESLOCAMENTO_HORIZONTAL_2)
    elif i==2:
        soma = np.sum(DESLOCAMENTO_HORIZONTAL_3)
    elif i==3:
        soma = np.sum(DESLOCAMENTO_HORIZONTAL_4)
    elif i==4:
        soma = np.sum(DESLOCAMENTO_HORIZONTAL_5)
    elif i==5:
        soma = np.sum(DESLOCAMENTO_HORIZONTAL_6)
    elif i==6:
        soma = np.sum(DESLOCAMENTO_HORIZONTAL_7)
    elif i==7:
        soma = np.sum(DESLOCAMENTO_HORIZONTAL_8)
    elif i==8:
        soma = np.sum(DESLOCAMENTO_HORIZONTAL_9)
    else:
        soma = np.sum(DESLOCAMENTO_HORIZONTAL_10)
    DISTANCIA_TOTAL[i] = soma

########################################################################################################################

# CALCULO DO CUSTO ENERGETICO "EM" TOTAL POR GADO LEITEIRO
CUSTO_ENERGETICO_EM_TOTAL = [0] * len(PESO_DO_GADO)
CUSTO_ENERGETICO_ELL_TOTAL = [0] * len(PESO_DO_GADO)
for i in range(len(CUSTO_ENERGETICO_EM_TOTAL)):
    if i==0:
        soma_em = np.sum(Custo_Energetico_EM_1)
        soma_ell = np.sum(Custo_Energetico_ELL_1)
    elif i==1:
        soma_em = np.sum(Custo_Energetico_EM_2)
        soma_ell = np.sum(Custo_Energetico_ELL_2)
    elif i==2:
        soma_em = np.sum(Custo_Energetico_EM_3)
        soma_ell = np.sum(Custo_Energetico_ELL_3)
    elif i==3:
        soma_em = np.sum(Custo_Energetico_EM_4)
        soma_ell = np.sum(Custo_Energetico_ELL_4)
    elif i==4:
        soma_em = np.sum(Custo_Energetico_EM_5)
        soma_ell = np.sum(Custo_Energetico_ELL_5)
    elif i==5:
        soma_em = np.sum(Custo_Energetico_EM_6)
        soma_ell = np.sum(Custo_Energetico_ELL_6)
    elif i==6:
        soma_em = np.sum(Custo_Energetico_EM_7)
        soma_ell = np.sum(Custo_Energetico_ELL_7)
    elif i==7:
        soma_em = np.sum(Custo_Energetico_EM_8)
        soma_ell = np.sum(Custo_Energetico_ELL_8)
    elif i==8:
        soma_em = np.sum(Custo_Energetico_EM_9)
        soma_ell = np.sum(Custo_Energetico_ELL_9)
    else:
        soma_em = np.sum(Custo_Energetico_EM_10)
        soma_ell = np.sum(Custo_Energetico_ELL_10)
    CUSTO_ENERGETICO_EM_TOTAL[i] = soma_em
    CUSTO_ENERGETICO_ELL_TOTAL[i] = soma_ell

########################################################################################################################

# MOSTRAR AS DISTANCIAS E DOS CUSTOS ENERGETICOS POR GADO
for i in range(len(PESO_DO_GADO)):
    print("")
    print("***************************************************************************************************************")
    MOSTRAR_DISTANCIA(DISTANCIA_TOTAL,i)
    print("-----------------------------------------------------------------------------------------------------------")
    MOSTRAR_CUSTO_ENERGETICO_EM(CUSTO_ENERGETICO_EM_TOTAL,i)
    print("-----------------------------------------------------------------------------------------------------------")
    MOSTRAR_CUSTO_ENERGETICO_ELL(CUSTO_ENERGETICO_ELL_TOTAL,i)

########################################################################################################################

# MOSTRAR AS DISTANCIAS E OS CUSTOS ENERGETICOS TOTAIS

print("")
print("DISTANCIA TOTAL :",np.sum(DISTANCIA_TOTAL),"Km")
print("")
print("CUSTO ENERGETICO 'EM' TOTAL :",np.sum(CUSTO_ENERGETICO_EM_TOTAL),"MCal")
print("")
print("CUSTO ENERGETICO 'ELL' TOTAL :",np.sum(CUSTO_ENERGETICO_ELL_TOTAL),"MCal")

########################################################################################################################

# MOSTRAR OS TEMPOS DE PROCESSAMENTOS

Tempo_Leitura_do_Arquivo = Tempo_Fim_Leitura - Tempo_Inicio_Leitura
print("")
print("TEMPO DE LEITURA DO ARQUIVO DE CONFIGURAÇÃO:",Tempo_Leitura_do_Arquivo,"Seg")
Tempo_do_Processamento = Tempo_Fim - Tempo_Inicio
print("")
print("TEMPO DE PROCESSAMENTO TOTAL :",Tempo_do_Processamento,"Seg")

########################################################################################################################

# GUARDAR OS RESULTADOS EM ARQUIVOS CSV
for i in range(len(ARQUIVOS_ESCREVER)):
    if i == 0:
        CARGAR_ARQUIVO(ARQUIVOS_ESCREVER[i],DISTANCIA_TOTAL)
    elif i == 1:
        CARGAR_ARQUIVO(ARQUIVOS_ESCREVER[i], CUSTO_ENERGETICO_EM_TOTAL)
    else:
        CARGAR_ARQUIVO(ARQUIVOS_ESCREVER[i], CUSTO_ENERGETICO_ELL_TOTAL)

########################################################################################################################

# GRAFICO DA DISTANCIA TOTAL POR GADO
width = 0.5
x_axis = ['1','2','3','4','5','6','7','8','9','10']
plt.bar(x_axis, DISTANCIA_TOTAL, width, color='black')
plt.title('DISTÂNCIA TOTAL PERCORRIDA POR BOVINO', SIZE=18)
plt.xlabel('Bovino', size=18)
plt.ylabel('Distância Total (Km)', size=18)
plt.axis([-0.5, 10, 0, 20])
plt.xticks(fontsize='x-large')
plt.yticks(fontsize='x-large')
plt.savefig('Distancia Total Percorrida por bovino.png')
plt.cla
plt.show()

########################################################################################################################

# GRAFICO DO CUSTO ENERGETICO EM TOTAL POR GADO
width = 0.5
x_axis = ['1','2','3','4','5','6','7','8','9','10']
plt.bar(x_axis, CUSTO_ENERGETICO_EM_TOTAL, width, color='red')
plt.title('CUSTO ENERGÉTICO "EM" TOTAL POR BOVINO', SIZE=18)
plt.xlabel('Bovino', SIZE=18)
plt.ylabel('Custo Energético EM (Mcal)', SIZE=18)
plt.axis([-0.5, 10, 0, 6])
plt.xticks(fontsize='x-large')
plt.yticks(fontsize='x-large')
plt.savefig('Consumo Energetico EM Total por bovino.png')
plt.cla()
plt.show()

########################################################################################################################

# GRAFICO DO CUSTO ENERGETICO ELL TOTAL POR GADO
width = 0.5
x_axis = ['1','2','3','4','5','6','7','8','9','10']
plt.bar(x_axis, CUSTO_ENERGETICO_ELL_TOTAL, width, color='blue')
plt.title('CUSTO ENERGÉTICO "ELL" TOTAL POR BOVINO', SIZE=18)
plt.xlabel('Bovino', SIZE=18)
plt.ylabel('Custo Energético ELL (Mcal)', SIZE=18)
plt.axis([-0.5, 10, 0, 5])
plt.xticks(fontsize='x-large')
plt.yticks(fontsize='x-large')
plt.savefig('Consumo Enegertico ELL Total por bovino.png')
plt.show()