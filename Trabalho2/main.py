import networkx as nx
import pandas as pd


def criar_grafo_arquivo(nome_arquivo):
    extensao = nome_arquivo.split('.')[-1]
    if extensao == 'csv':
        df = pd.read_csv(nome_arquivo)
    elif extensao in ['xlsx', 'xls']:
        df = pd.read_excel(nome_arquivo)
    else:
        raise Exception("Extensão de arquivo inválida")

    G = nx.DiGraph()

    for i in range(len(df)):
        etapa = df.loc[i, 'Código']
        nome = df.loc[i, 'Nome']
        duracao = df.loc[i, 'Duração']
        G.add_node(etapa, nome=nome, duracao=duracao)

    for i in range(len(df)):
        etapa = df.loc[i, 'Código']
        dependencias = df.loc[i, 'Dependências']
        if pd.notna(dependencias):
            dependencias = dependencias.split(';')
            for d in dependencias:
                G.add_edge(d.strip(), etapa)

    return G


def encontrar_caminho_critico(G):
    caminho_critico = nx.algorithms.dag.dag_longest_path(G, weight='duracao')
    return caminho_critico


if __name__ == '__main__':
    while True:
        nome_arquivo = input("Informe o arquivo (0 para sair): ")
        if nome_arquivo == '0':
            break
        try:
            G = criar_grafo_arquivo(nome_arquivo)
            caminho_critico = encontrar_caminho_critico(G)
            print("Caminho Crítico:")
            for etapa in caminho_critico:
                nome = G.nodes[etapa]['nome']
                print("- {} ({})".format(nome, etapa))
            duracao_minima = nx.algorithms.dag.dag_longest_path_length(G, weight='duracao')
            print("Tempo Mínimo: {}".format(duracao_minima))
        except Exception as e:
            print("Erro: {}".format(str(e)))
