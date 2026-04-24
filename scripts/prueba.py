import mesa
import matplotlib.pyplot as plt

class MoneyAgent(mesa.Agent):
    """An agent with fixed initial wealth."""

    # 1. Ya no necesitas pasar 'unique_id' manualmente
    def __init__(self, model):
        super().__init__(model) 
        self.wealth = 1

    def step(self):
        # 2. El agente sigue teniendo un unique_id, pero ahora Mesa lo genera solo
        print(f"Hi, I am agent {self.unique_id}")
        if self.wealth == 0:
            return
        other_agent = self.random.choice(self.model.agents)
        other_agent.wealth += 1
        self.wealth -= 1
        print("I donated 1 coin to " + str(other_agent.unique_id) + ".")


class MoneyModel(mesa.Model):
    """A model with some number of agents."""

    def __init__(self, N):
        # 3. Inicializar la clase padre es obligatorio en Mesa 3+
        super().__init__() 
        self.num_agents = N
        
        # 4. Creamos los agentes. Ya no usamos 'schedule'
        for _ in range(self.num_agents):
            # Solo le pasamos el modelo. Mesa lo registra automáticamente en self.agents
            MoneyAgent(self) 

    def step(self):
        """Advance the model by one step."""
        # 5. Reemplazamos self.schedule.step() por el nuevo sistema de AgentSet
        self.agents.shuffle_do("step")

'''
empty_model = MoneyModel(10)
empty_model.step()

agent_wealths = [agent.wealth for agent in empty_model.agents]
plt.hist(agent_wealths)
plt.xlabel("Wealth")
plt.ylabel("Number of Agents")
plt.title("Wealth Distribution")
plt.show()'''

all_wealths = []
# This runs the model 100 times and collects the wealth of all agents at the end of each run
for j in range(100):
    # Run the model
    model = MoneyModel(10)
    for i in range(100):
        model.step()
    
    # Store the results
    for agent in model.agents:
        all_wealths.append(agent.wealth)

plt.hist(all_wealths, bins=range(max(all_wealths) + 1), align='left')
plt.show()