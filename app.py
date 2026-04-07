import streamlit as st
from maze_solver import MAZE, START, END, solve_maze_bfs

st.set_page_config(page_title="Maze Solver", layout="wide")
st.title("Visualizador de Algoritmo de Búsqueda en Laberinto")

def render_maze(maze, path=None):
    if path is None:
        path = []
    
    display_maze = []
    for r_idx, row in enumerate(maze):
        display_row = []
        for c_idx, col in enumerate(row):
            if (r_idx, c_idx) == START:
                display_row.append("🚀") 
            elif (r_idx, c_idx) == END:
                display_row.append("🏁") 
            elif (r_idx, c_idx) in path:
                display_row.append("🟦") 
            elif col == 1:
                display_row.append("⬛") 
            else:
                display_row.append("⬜") 
        display_maze.append("".join(display_row))
    
    st.markdown("<div style='font-family: monospace; line-height: 1.2; letter-spacing: 2px;'>" + "<br>".join(display_maze) + "</div>", unsafe_allow_html=True)

st.sidebar.header("Configuración")
algorithm = st.sidebar.selectbox("Selecciona el algoritmo", ["BFS", "DFS", "A*"])
solve_button = st.sidebar.button("Resolver Laberinto")

# Renderizar estado inicial
if not solve_button:
    render_maze(MAZE)

if solve_button:
    if algorithm == "BFS":
        path = solve_maze_bfs(MAZE, START, END)
        if path:
            # MÉTRICA SOLICITADA: Número de casillas
            num_casillas = len(path)
            st.sidebar.metric("Casillas usadas", num_casillas)
            st.success(f"¡Camino encontrado! El algoritmo {algorithm} utilizó {num_casillas} casillas.")
            render_maze(MAZE, path)
        else:
            st.error("No se encontró un camino.")
    else:
        st.warning(f"El algoritmo {algorithm} aún no está implementado.")