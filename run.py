from Network import Network
task = '''Breaking News! Donald Trump will launch his own cryptocurrency.'''
agent_network = Network(task, "Pennsylvania", 15)
#agent_network.group_chat("round_robin", 1)
agent_network.simulate("round_robin", 1)
