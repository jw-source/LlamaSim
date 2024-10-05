from network import Network
agent_network = Network(population="Pennsylvania Voters", num_agents=5, max_context_size=4000)
prompt = "Gas prices are an all-time high."
question = "Are you voting for Kamala Harris?"
agent_network.group_chat(prompt, "random", max_rounds=1)
agent_network.predict(prompt, question)
