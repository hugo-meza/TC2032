import json
import random
from mesa import Agent, Model
from mesa.space import MultiGrid


class WalleReactivo(Agent):
    """
    Agente reactivo que se mueve en la cuadrícula.
    La idea es que el alumno complete la lógica de movimiento.
    """

    def __init__(self, model, x, y, goal_x, goal_y, max_steps=30):
        super().__init__(model)

        # Posición actual del agente
        self.x = x
        self.y = y

        # Posición inicial (spawn)
        self.spawn_x = x
        self.spawn_y = y

        # Meta
        self.goal_x = goal_x
        self.goal_y = goal_y

        # Control de pasos
        self.steps_taken = 0
        self.max_steps = max_steps

        # Historial de movimiento (ya inicializado correctamente)
        self.path = [{"x": self.x, "y": self.y}]

    def reached_goal(self):
        """
        Regresa True si el agente ya llegó a la meta.
        """
        # TODO: aquí el alumno debe comparar la posición actual con la meta
        return (self.x, self.y) == (self.goal_x, self.goal_y)

    def get_possible_moves(self):
        """
        Obtiene los movimientos válidos dentro de la cuadrícula.
        """
        moves = []
        grid_width = self.model.grid.width
        grid_height = self.model.grid.height

        # TODO: completar lógica de movimientos (ya hay ejemplos)

        if self.x < grid_width - 1:
            moves.append((self.x + 1, self.y))

        if self.x > 0:
            moves.append((self.x - 1, self.y))

        if self.y < grid_height - 1:
            moves.append((self.x, self.y + 1))

        if self.y > 0:
            moves.append((self.x, self.y - 1))

        return moves

    def choose_action(self, moves):
        """
        Selecciona una acción de manera reactiva.
        """
        # TODO: aquí el alumno puede modificar la estrategia
        if moves:
            return random.choice(moves)
        return None

    def move(self, new_position):
        """
        Mueve al agente a la nueva posición.
        """
        new_x, new_y = new_position

        # Movimiento en el grid
        self.model.grid.move_agent(self, (new_x, new_y))

        # Actualizar atributos
        self.x = new_x
        self.y = new_y

        # Guardar historial (esto ya funciona para el JSON)
        self.path.append({"x": self.x, "y": self.y})

    def step(self):
        """
        Ejecuta un paso de simulación para el agente.
        """

        # TODO: lógica general del agente

        if self.reached_goal():
            print(f"WalleReactivo llegó a la meta en ({self.x}, {self.y}) en {self.steps_taken} pasos.")
            return

        if self.steps_taken >= self.max_steps:
            print(f"WalleReactivo FALLÓ al llegar a la meta en {self.max_steps} pasos.")
            return

        possible_moves = self.get_possible_moves()
        selected_move = self.choose_action(possible_moves)

        if selected_move is not None:
            self.move(selected_move)
            self.steps_taken += 1
            print(f"WalleReactivo se movió a ({self.x}, {self.y})")


class GridModel(Model):
    """
    Modelo que contiene la cuadrícula y al agente reactivo.
    """

    def __init__(self, width, height, goal_x, goal_y):
        super().__init__()

        self.grid = MultiGrid(width, height, torus=False)

        # Crear y colocar agente
        self.agent1 = WalleReactivo(self, 0, 0, goal_x, goal_y, max_steps=25)
        self.grid.place_agent(self.agent1, (0, 0))

    def step(self):
        """
        Avanza un paso en la simulación.
        """
        self.agent1.step()

    def save_log(self, filename="walle_log.json"):
        """
        Guarda el historial en JSON (YA FUNCIONAL).
        """

        log_data = {
            "robots": [
                {
                    "spawnPosition": {
                        "x": self.agent1.spawn_x,
                        "y": self.agent1.spawn_y
                    },
                    "path": self.agent1.path
                }
            ]
        }

        with open(filename, "w") as file:
            json.dump(log_data, file, indent=4)

        print(f"Log guardado en {filename}")


# -------------------------
# EJECUCIÓN DE LA SIMULACIÓN
# -------------------------

GRID_WIDTH = 5
GRID_HEIGHT = 5

# IMPORTANTE: dentro del grid válido (0–4)
GOAL_X = 4
GOAL_Y = 4

model = GridModel(GRID_WIDTH, GRID_HEIGHT, GOAL_X, GOAL_Y)

# Ejecutar simulación
for _ in range(30):
    model.step()

# Guardar resultados (esto ya funciona automáticamente)
model.save_log()