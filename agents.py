class Agent:
    def __init__(self, name):
        self.name = name

    def run(self, task):
        print(f"Agent {self.name} is running task: {task}")
        return {"status": "ok", "task": task}

def run_all_agents():
    # Giả lập chạy tất cả agents
    agents = [Agent("A1"), Agent("A2")]
    results = []
    for agent in agents:
        results.append(agent.run("default task"))
    return results

def get_agent(agent_name):
    return Agent(agent_name)