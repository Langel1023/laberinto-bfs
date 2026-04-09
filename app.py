import streamlit as st
import numpy as np
from collections import deque
import time
import re

# Configuración visual de la página
st.set_page_config(page_title="Visualizador de Laberintos", layout="wide")

def solve_maze_bfs(maze, start, end):
    """Algoritmo de Búsqueda en Amplitud (BFS)"""
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

def render_maze_styled(maze, start, end, path=None):
    """Renderiza el laberinto siguiendo la estética de las capturas del profe"""
    if path is None: path = []
    path_set = set(path)
    
    output = ""
    for r in range(maze.shape[0]):
        line = ""
        for c in range(maze.shape[1]):
            pos = (r, c)
            if pos == start: line += "🚀" 
            elif pos == end: line += "🏁"
            elif pos in path_set: line += "🔹" # Emoji de punto azul para el camino
            elif maze[r, c] == 1: line += "⬛" 
            else: line += "⬜"
        output += line + "<br>"
    
    st.markdown(f"<div style='font-family: monospace; line-height: 1.1; font-size: 20px;'>{output}</div>", unsafe_allow_html=True)

# --- INTERFAZ (SIDEBAR) ---
st.title("Visualizador de Algoritmo de Búsqueda en Laberinto")

st.sidebar.header("OPCIONES DE LA APP")
st.sidebar.write("1=pared, 0=camino, 2=inicio, 3=final")

archivo = st.sidebar.file_uploader("Carga el laberinto", type=["txt"])
algoritmo = st.sidebar.selectbox("Selecciona algoritmo", ["BFS", "DFS en proceso", "A* en proceso"])
boton_resolver = st.sidebar.button("Resolver Laberinto Cargado")

# --- LÓGICA PRINCIPAL ---
if archivo:
    # Procesamiento del archivo .txt
    content = archivo.read().decode("utf-8")
    lines = content.strip().split('\n')
    maze_data = []
    for line in lines:
        row = [int(d) for d in re.findall(r'\d', line)]
        if row: maze_data.append(row)
    
    maze_np = np.array(maze_data)
    
    # Localizar puntos 2 y 3
    p2 = np.where(maze_np == 2)
    p3 = np.where(maze_np == 3)

    if p2[0].size > 0 and p3[0].size > 0:
        start = (p2[0][0], p2[1][0])
        end = (p3[0][0], p3[1][0])
        
        if boton_resolver:
            if algoritmo == "BFS":
                ruta, tiempo = solve_maze_bfs(maze_np, start, end)
                if ruta:
                    # Banner de éxito verde como en la imagen
                    st.success(f"BFS resuelto en {tiempo:.6f} s | Pasos: {len(ruta)}")
                    render_maze_styled(maze_np, start, end, ruta)
                else:
                    st.error("No se encontró ruta.")
            else:
                st.warning("Este algoritmo aún no está habilitado.")
        else:
            # Vista previa sin resolver
            st.info("Esperando resolución...")
            render_maze_styled(maze_np, start, end)
    else:
        st.error("El archivo debe tener un 2 (inicio) y un 3 (meta).")
else:
    # Estado inicial: Cuadro azul de "Esperando archivo..."
    st.info("Esperando archivo...")
