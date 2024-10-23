from alt_network import Network
from mem0_utils import config
from mem0 import Memory

memory = Memory.from_config(config)
agent_network = Network(memory, population="Pennsylvania Voters", num_agents=2, max_context_size=4000)
prompt = "Gas prices are an all-time high."
question = "Are you voting for Kamala Harris?"
agent_network.group_chat(prompt, "random", max_rounds=1)
agent_network.predict(prompt, question)
