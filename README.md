# LlamaPoll - Simulate Focus Groups With LLM Agents

__TLDR: We built a multi-agent framework from scratch and used it to simulate focus groups__ 

Leaner than CrewAI & meaner than Autogen, we easily beat prompting & fine-tuning by using our conversational framework to spawn groupchats of collaborative agents to solve all your problems __(in just 4 lines of code)__.

We adapted this framework to simulate focus groups in real-time: by using data to replicate diversity, generating detailed backstories for AI agents, and programming them to think exactly like the people they are acting out. 
```python
from Network import Network
breaking_news = '''Breaking News! Donald Trump will launch his own cryptocurrency.'''
agent_network = Network(breaking_news, state = "Pennsylvania", num_agents = 15)
agent_network.simulate("round_robin", num_rounds = 1)
