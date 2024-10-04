from agent import Agent
import random 
import openai
from generate_identity import generate_identities
import time
from dotenv import load_dotenv
import os

load_dotenv()

class Network:
    def __init__(self, data:str, num_agents:int, max_context_size:int):
        self.names, self.identities = self._create_identities(data, num_agents)
        self.client = openai.OpenAI(
            base_url='https://api.cerebras.ai/v1',
            api_key=os.getenv("CEREBRAS_API_KEY")
        )
        self.shared_context = []
        self.conversation_logs = []
        self.max_context_size = max_context_size
        self.num_agents = num_agents
        self.agents = self._init_agents()
        
    def _create_identities(self, data:str, num_agents:int):
        start_time = time.time()
        names, identities = generate_identities(data, num_agents)
        end_time = time.time()
        elapsed_time = round(end_time - start_time, 2)
        print(f"Generated {num_agents} identities in: {elapsed_time} seconds")
        return names, identities
        
    def _init_agents(self):
        start_time = time.time()
        agents = [Agent(name=name, identity=identity, client=self.client) 
                  for name, identity in zip(self.names, self.identities)]
        end_time = time.time()
        elapsed_time = round(end_time - start_time, 2)
        print(f"Generated {self.num_agents} backstories in: {elapsed_time} seconds")
        return agents
    
    def _manage_context_size(self):
        total_length = sum(len(msg) for msg in self.shared_context)
        while total_length > self.max_context_size:
            removed_msg = self.shared_context.pop(0)
            total_length -= len(removed_msg)

    def group_chat(self, prompt, chat_type, max_rounds):
        round_count = 0
        while round_count < max_rounds: 
            if chat_type == "round_robin":
                for _, agent in enumerate(self.agents):
                    agent.prompt = prompt
                    agent_response = agent.chat(self.shared_context)
                    self.shared_context.append(agent.name + ": " + agent_response)
                    self.conversation_logs.append(agent.name + ": " + agent_response)
                    self._manage_context_size()
                    print(f"\n{agent.name}: {agent_response}")
            elif chat_type == "random":
                for _ in range(len(self.agents)):
                    agent = random.choice(self.agents)
                    agent.prompt = prompt
                    agent_response = agent.chat(self.shared_context)
                    self.shared_context.append(agent.name + ": " + agent_response)
                    self.conversation_logs.append(agent.name + ": " + agent_response)
                    self._manage_context_size()
                    print(f"\n{agent.name}: {agent_response}")
            round_count += 1
        return self.conversation_logs
