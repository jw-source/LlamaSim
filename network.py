from Agent import Agent
import random 
import os
import openai
from generate_identity import generate_identities

class Network:
    def __init__(self, prompt : str, state: str, num_agents:int, state_data=None):
        self.prompt = prompt
        self.state_data = state_data
        self.identities = self._create_identities(state, num_agents, state_data)
        self.client = openai.OpenAI(
            base_url='https://api.cerebras.ai/v1',
            api_key=os.environ.get('DHRUVI_API_KEY')
        )
        self.shared_context = []
        self.agents = self._init_agents()
        
    def _create_identities(self, state:str, num_agents:int, state_data):
        identities = generate_identities(state, num_agents, state_data)
        return identities
        
    def _init_agents(self):
        agents = [Agent(prompt=self.prompt, identity=identity, client=self.client) for identity in self.identities]
        return agents
    
    def group_chat(self, chat_type, max_rounds):
        round_count = 0
        while round_count < max_rounds: 
            if chat_type == "round_robin":
                for i, agent in enumerate(self.agents):
                    print('in loop')
                    agent_response = agent.chat(self.shared_context)
                    self.shared_context.append({'role': 'assistant', 'content':  agent_response, 'identity': agent.identity})
                    if len(self.shared_context) > 14000:
                        self.shared_context = self.shared_context[-14000:]
                    # print(f"\n{agent.identity}: {agent_response}")
            elif chat_type == "random":
                for i in range(len(self.agents)):
                    agent = random.choice(self.agents)
                    agent_response = agent.chat(self.shared_context)
                    self.shared_context.append({'role': 'assistant', 'content':  agent_response, 'identity': agent.identity})
                    if len(self.shared_context) > 14000:
                        self.shared_context = self.shared_context[-14000:]
                    print(f"\n{agent.identity}: {agent_response}")
            round_count += 1
        return self.shared_context
    
    def simulate(self, chat_type, max_rounds):
        pre_vote = [2]*len(self.agents)
        post_vote = [2]*len(self.agents)
        for i, agent in enumerate(self.agents):
            pre_decision = int(agent.pre_predict())
            pre_vote[i] = pre_decision
        self.group_chat(chat_type, max_rounds)
        for i, agent in enumerate(self.agents):
            pred = agent.post_predict()
            if str.isdigit(pred):
                post_decision = int(pred)
            else:
                weight = self.approximate_weight()
                print(weight)
                post_decision = round(weight)
            post_vote[i] = post_decision
        print(f"Pre-vote: {pre_vote}")
        print(f"Post-vote: {post_vote}")
        return pre_vote, post_vote, self.shared_context
    
    def approximate_weight(self):
        vote_data = self.state_data.get('2020_election_vote_data', [])
        if vote_data == []: return random.randint(0,1)
        
        pct_dem = vote_data[0].get('percent_democrat', [])
        if pct_dem == []: return random.randint(0,1)
        
        return 1 - pct_dem * 0.01
