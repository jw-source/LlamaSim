from network import Network
prompt = '''Kamala Harris is showing up to the Purnell Center today!'''
population = '''Students at Carnegie Mellon University'''
num_agents = 10
agent_network = Network(prompt, population, num_agents)
agent_network.group_chat("random", 1)
