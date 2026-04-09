import streamlit as st
import numpy as np
from collections import deque
import heapq
import time
import re

# Configuración de página
st.set_page_config(page_title="Visualizador de Laberintos Pro", layout="wide")

# --- ALGORITMOS DE BÚSQUEDA ---

def solve_bfs(maze, start, end):
    start_time = time.time()
    queue = deque([(start, [start])])
    visited = {start}
    while queue:
        (r, c), path = queue.popleft()
        if (r, c) == end:
            return path, (time.time() - start_time)
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < maze.shape[0] and 0 <= nc < maze.shape[1]:
                if maze[nr, nc] != 1 and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    queue.append(((nr, nc), path + [(nr, nc)]))
    return None, 0

def solve_dfs(maze, start, end):
    start_time = time.time()
    stack = [(start, [start])]
    visited = {start}
    while stack:
        (r, c), path = stack.pop() # LIFO para profundidad
        if (r, c) == end:
            return path, (time.time() - start_time)
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < maze.shape[0] and 0 <= nc < maze.shape[1]:
                if maze[nr, nc] != 1 and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    stack.append(((nr, nc), path + [(nr, nc)]))
    return None, 0

def solve_astar(maze, start, end):
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1]) # Distancia Manhattan

    start_time = time.time()
    # Priority Queue: (prioridad, actual, camino)
    pq = [(0 + heuristic(start, end), 0, start, [start])]
    visited = {start: 0}
    
    while pq:
        f, g, (r, c), path = heapq.heappop(pq)
        
        if (r, c) == end:
            return path, (time.time() - start_time)
            
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < maze.shape[0] and 0 <= nc < maze.shape[1] and maze[nr, nc] != 1:
                new_g = g + 1
                if (nr, nc) not in visited or new_g < visited[(nr, nc)]:
                    visited[(nr, nc)] = new_g
                    f = new_g + heuristic((nr, nc), end)
                    heapq.heappush(pq, (f, new_g, (nr, nc), path + [(nr, nc)]))
    return None, 0

# --- INTERFAZ ---

def render_maze(maze, start, end, path=None):
    if path is None: path = []
    path_set = set(path)
    output = ""
    for r in range(maze.shape[0]):
        line = ""
        for c in range(maze.shape[1]):
            pos = (r, c)
            if pos == start: line += "🚀" 
            elif pos == end: line += "🏁"
            elif pos in path_set: line += "🔹" 
            elif maze[r, c] == 1: line += "⬛" 
            else: line += "⬜"
        output += line + "<br>"
    st.markdown(f"<div style='font-family: monospace; line-height: 1.1; font-size: 20px;'>{output}</div>", unsafe_allow_html=True)

st.title("Visualizador de Algoritmo de Búsqueda en Laberinto")

st.sidebar.header("OPCIONES DE LA APP")
archivo = st.sidebar.file_uploader("Carga el laberinto", type=["txt"])
algoritmo = st.sidebar.selectbox("Selecciona algoritmo", ["BFS", "DFS", "A*"])
boton = st.sidebar.button("Resolver Laberinto Cargado")

if archivo:
    content = archivo.read().decode("utf-8")
    maze_data = [[int(d) for d in re.findall(r'\d', line)] for line in content.strip().split('\n') if re.findall(r'\d', line)]
    maze_np = np.array(maze_data)
    
    p2, p3 = np.where(maze_np == 2), np.where(maze_np == 3)
    if p2[0].size > 0 and p3[0].size > 0:
        start, end = (p2[0][0], p2[1][0]), (p3[0][0], p3[1][0])
        
        if boton:
            if algoritmo == "BFS": ruta, t = solve_bfs(maze_np, start, end)
            elif algoritmo == "DFS": ruta, t = solve_dfs(maze_np, start, end)
            else: ruta, t = solve_astar(maze_np, start, end)
            
            if ruta:
                st.success(f"{algoritmo} resuelto en {t:.6f} s | Pasos: {len(ruta)}")
                render_maze(maze_np, start, end, ruta)
            else:
                st.error("No hay solución.")
        else:
            render_maze(maze_np, start, end)
    else:
        st.error("Falta el inicio (2) o el fin (3).")
else:
    st.info("Esperando archivo...")
