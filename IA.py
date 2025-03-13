import random
import math
import matplotlib.pyplot as plt

NUM_CIDADES = 50
TAMANHO_POPULACAO = 100
NUM_GERACOES = 500
TAXA_CROSSOVER = 0.8
TAXA_MUTACAO = 0.02
ELITE_SIZE = 5

def gerar_cidades(num_cidades):
    return [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(num_cidades)]

cidades = gerar_cidades(NUM_CIDADES)

def calcular_distancia(cidade1, cidade2):
    return math.sqrt((cidade1[0] - cidade2[0])**2 + (cidade1[1] - cidade2[1])**2)

def distancia_total(percurso):
    distancia = 0
    for i in range(len(percurso)):
        cidade_atual = percurso[i]
        proxima_cidade = percurso[(i + 1) % len(percurso)] 
        distancia += calcular_distancia(cidade_atual, proxima_cidade)
    return distancia

def criar_populacao(tamanho, cidades):
    populacao = []
    for _ in range(tamanho):
        individuo = cidades[:]
        random.shuffle(individuo)
        populacao.append(individuo)
    return populacao

def avaliar_populacao(populacao):
    pontuacoes = []
    for individuo in populacao:
        pontuacoes.append((distancia_total(individuo), individuo))
    return sorted(pontuacoes, key=lambda x: x[0])

def selecao(pontuacoes, elite_size):
    selecionados = [individuo for _, individuo in pontuacoes[:elite_size]]
    while len(selecionados) < TAMANHO_POPULACAO:
        participante1 = random.choice(pontuacoes)[1]
        participante2 = random.choice(pontuacoes)[1]
        melhor = participante1 if distancia_total(participante1) < distancia_total(participante2) else participante2
        selecionados.append(melhor)
    return selecionados

def crossover(pai1, pai2):
    start = random.randint(0, len(pai1) - 1)
    end = random.randint(start, len(pai1) - 1)
    
    filho_temp = pai1[start:end]
    filho = filho_temp + [cidade for cidade in pai2 if cidade not in filho_temp]
    
    return filho

def gerar_filhos(selecionados):
    filhos = []
    for i in range(len(selecionados)):
        if random.random() < TAXA_CROSSOVER:
            pai1 = selecionados[i]
            pai2 = random.choice(selecionados)
            filho = crossover(pai1, pai2)
            filhos.append(filho)
        else:
            filhos.append(selecionados[i])
    return filhos

def mutacao(individuo):
    for trocas in range(len(individuo)):
        if random.random() < TAXA_MUTACAO:
            i = random.randint(0, len(individuo) - 1)
            j = random.randint(0, len(individuo) - 1)
            individuo[i], individuo[j] = individuo[j], individuo[i]
    return individuo

def mutar_populacao(populacao):
    return [mutacao(individuo) for individuo in populacao]

def algoritmo_genetico():
    populacao = criar_populacao(TAMANHO_POPULACAO, cidades)
    
    melhor_distancia = float('inf')
    melhor_rota = None

    for geracao in range(NUM_GERACOES):
        pontuacoes = avaliar_populacao(populacao)
        
        if pontuacoes[0][0] < melhor_distancia:
            melhor_distancia = pontuacoes[0][0]
            melhor_rota = pontuacoes[0][1]
        
        selecionados = selecao(pontuacoes, ELITE_SIZE)
        filhos = gerar_filhos(selecionados)
        populacao = mutar_populacao(filhos)
        
        if geracao % 50 == 0 or geracao == NUM_GERACOES - 1:
            print(f"Geração {geracao}: Melhor distância = {melhor_distancia:.2f}")

    return melhor_rota, melhor_distancia

def plotar_rota(cidades, rota):
    x = [cidade[0] for cidade in rota]
    y = [cidade[1] for cidade in rota]
    
    plt.figure(figsize=(10, 8))
    plt.plot(x, y, marker='o', linestyle='-', color='b')
    
    # Conectar a última cidade com a primeira
    plt.plot([x[-1], x[0]], [y[-1], y[0]], marker='o', linestyle='-', color='b')
    
    for i, cidade in enumerate(rota):
        plt.text(cidade[0], cidade[1], f'{i+1}', fontsize=12, ha='right')
    
    plt.title("Melhor Rota Encontrada (Caixeiro Viajante)")
    plt.xlabel("Coordenada X")
    plt.ylabel("Coordenada Y")
    plt.show()


rota_final, distancia_final = algoritmo_genetico()

print(f"\nMelhor distância encontrada: {distancia_final:.2f}")

print("Testando Jeff")
