from network import Network
prompt = '''Kamala Harris is showing up to the Purnell Center today!'''
population = '''Students at Carnegie Mellon University'''
agent_network = Network(population, num_agents=5, max_context_size=4000)
agent_network.group_chat(prompt, "random", 1)

