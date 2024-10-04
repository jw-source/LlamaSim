<p align="center">
  <img src="https://github.com/user-attachments/assets/99dbbe95-a2df-48ff-bd48-124cc1e51c6a" width="300">
</p>

<p align="center">
  <em>Simulate human behavior with LLM agents</em>
</p>
<p align="center">
<a href="website_placeholder">🔗 <b>Website</b></a>
<span>&nbsp;&nbsp;•&nbsp;&nbsp;</span>
<a href="https://x.com/CerebrasSystems/status/1838684550282559545">🐦 <b>Twitter</b></a>

# LlamaPoll: 

LlamaPoll is a baby (still developing!) multi-agent framework that aims to simulate human behavior at scale. Given a specific environment (voters in Pennsylvania, students at CMU, focus group participants etc.), we use demographic data to replicate target groups, and aim to provide actionable insights for important questions/events. 

More to come...

## Usage: 
```python 
from network import Network
prompt = '''Kamala Harris is showing up to the Purnell Center today!'''
population = '''Carnegie Mellon University students'''
agent_network = Network(population, num_agents=5, max_context_size=4000)
agent_network.group_chat(prompt, "random", 1)
```
