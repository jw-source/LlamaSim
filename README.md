<p align="center">
  <img src="https://github.com/user-attachments/assets/99dbbe95-a2df-48ff-bd48-124cc1e51c6a" width="300">
</p>

<p align="center">
  <em>Simulate human behavior with mass LLMs</em>
</p>
<p align="center">
<a href="https://www.loom.com/share/e7a6bf9cf44448ed99e7b29cd790d918?sid=c36b767b-ad39-4006-939b-1c623a36d263">🔗 <b>Demo Video</b></a>
<span>&nbsp;&nbsp;•&nbsp;&nbsp;</span>
<a href="https://x.com/CerebrasSystems/status/1838684550282559545">🐦 <b>Twitter</b></a>

# LlamaSim: 

LlamaSim is a multi-LLM framework that aims to simulate human behavior at scale. Given a specific environment (e.g., voters in Pennsylvania, students at CMU), we replicate target groups, and aim to provide actionable insights for important questions/events. 

More to come...

## Roadmap
- [x] Gradio Frontend (Local Demo)
- [ ] Rewrite Agent Generatation using Cerebras instead of OpenAI
- [ ] Improve Memory using mem0.ai
- [ ] Demographically Aligned Agents on-the-fly
- [ ] Live Data Feeds for Agents
- [ ] Async Communication for Agents
- [ ] Live Demo

## Usage: 
```bash
# Clone the repository
git clone https://github.com/jw-source/LlamaSim
```
```bash
# Add API keys to .env
mv env.txt .env

# Create venv
python3 -m venv .venv

# Set the venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run
cd src
python run.py
```

### Real Example
```python
from network import Network
agent_network = Network(population="Pennsylvania Voters", num_agents=5, max_context_size=4000)
prompt = "Gas prices are an all-time high."
question = "Are you voting for Kamala Harris?"
agent_network.group_chat(prompt, "random", max_rounds=1)
agent_network.predict(prompt, question)
```
