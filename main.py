# 1. MST / Prim y Kruskal
# 2. Necesitamos TSP
# 3. Ford Fulkerson
from itertools import permutations


def prim(grafo):
    n = len(grafo)
    visitados = [False] * n
    clave = [float("inf")] * n
    padre = [-1] * n

    clave[0] = 0

    for _ in range(n):
        u = -1
        min_val = float("inf")
        for i in range(n):
            if not visitados[i] and clave[i] < min_val:
                min_val = clave[i]
                u = i

        visitados[u] = True

        for v in range(n):
            peso = grafo[u][v]
            if peso != 0 and not visitados[v] and peso < clave[v]:
                clave[v] = peso
                padre[v] = u
    mst = []
    for v in range(1, n):
        mst.append((chr(65 + padre[v]), chr(65 + v), grafo[padre[v]][v]))

    return mst


def tsp(grafo):
    numero_de_nodos = len(grafo)
    nodos = list(range(1, numero_de_nodos))

    mejor_costo = float("inf")
    mejor_camino = None

    for perm in permutations(nodos):
        costo_actual = 0
        nodo_actual = 0

        for nodo in perm:
            costo_actual += grafo[nodo_actual][nodo]
            nodo_actual = nodo

        costo_actual += grafo[nodo_actual][0]

        if costo_actual < mejor_costo:
            mejor_costo = costo_actual
            mejor_camino = perm

    res = ["A"]

    for colonia in mejor_camino:
        res.append(chr(65 + colonia))

    res.append("A")

    return res, mejor_costo


def BFS(grafo, s, t, parent):
    row = len(grafo)
    visited = [False] * (row)
    queue = []

    queue.append(s)
    visited[s] = True

    while queue:

        u = queue.pop(0)

        for ind, val in enumerate(grafo[u]):
            if visited[ind] == False and val > 0:
                queue.append(ind)
                visited[ind] = True
                parent[ind] = u
                if ind == t:
                    return True
    return False


def FordFulkerson(grafo, source, sink):
    row = len(grafo)
    parent = [-1] * (row)

    max_flow = 0
    while BFS(grafo, source, sink, parent):
        path_flow = float("Inf")
        s = sink
        while s != source:
            path_flow = min(path_flow, grafo[parent[s]][s])
            s = parent[s]

        max_flow += path_flow
        v = sink
        while v != source:
            u = parent[v]
            grafo[u][v] -= path_flow
            grafo[v][u] += path_flow
            v = parent[v]

    return max_flow


def leer_archivo(ruta):
    with open(ruta, "r") as f:
        lineas = [line.strip() for line in f if line.strip() != ""]

    indice = 0

    n = int(lineas[indice])
    indice += 1

    source, sink = map(int, lineas[indice].split())
    indice += 1

    distancias = []
    for _ in range(n):
        fila = list(map(int, lineas[indice].split()))
        distancias.append(fila)
        indice += 1

    capacidades = []
    for _ in range(n):
        fila = list(map(int, lineas[indice].split()))
        capacidades.append(fila)
        indice += 1

    return n, distancias, capacidades, source, sink


def main():
    n, distancias, capacidades, source, sink = leer_archivo("input.txt")
    print(f"Forma optima de cablear la fibra optica: {prim(distancias)}")
    print(
        f"Camino optimo para visitar todas las colonias: {tsp(distancias)[0]} con costo {tsp(distancias)[1]}"
    )
    print(
        f"Flujo maximo de datos con source: {source} y sink: {sink} es {FordFulkerson(capacidades,source,sink)}"
    )


main()
