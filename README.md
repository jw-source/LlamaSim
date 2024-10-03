# LlamaPoll 🦙: - Simulate The World With LLM Agents

__TLDR: We built a multi-agent framework from scratch and used it to simulate focus groups__ 

Use our conversational framework to spawn groupchats of collaborative agents to solve all your problems __(in just 4 lines of code)__.

We adapted this framework to simulate focus groups in real-time: by using data to replicate diversity, generating detailed backstories for AI agents, and programming them to think exactly like the people they are acting out. 
```python
from Network import Network
prompt = '''Kamala Harris is showing up to the Purnell Center today!'''
population = '''Students at Carnegie Mellon University'''
num_agents = 10
agent_network = Network(prompt, population, num_agents)
agent_network.group_chat("random", 1)
