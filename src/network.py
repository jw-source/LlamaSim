from agent import Agent
import random 
import openai
from generate_identity import generate_identities
import time
from dotenv import load_dotenv
import os
from collections import Counter

load_dotenv()

class Network:
    def __init__(self, population:str, num_agents:int, max_context_size:int):
        self.client = openai.OpenAI(
            base_url='https://api.cerebras.ai/v1',
            api_key=os.getenv("CEREBRAS_API_KEY")
        )
        self.names, self.identities = self._create_identities(population, num_agents)
        self.num_agents = num_agents
        self.agents = self._init_agents()
        self.shared_context = []
        self.conversation_logs = []
        self.max_context_size = max_context_size
        
    def _create_identities(self, population:str, num_agents:int):
        start_time = time.time()
        names, identities = generate_identities(population, num_agents)
        end_time = time.time()
        elapsed_time = round(end_time - start_time, 2)
        print(f"Generated {num_agents} identities in: {elapsed_time} seconds")
        return names, identities
        
    def _init_agents(self):
        start_time = time.time()
        agents = [Agent(name, identity, self.client) 
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

    def group_chat(self, prompt:str, chat_type:str, max_rounds:int):
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
    
    def predict(self, prompt:str, question:str):
        pre_choice = [None]*self.num_agents
        post_choice = [None]*self.num_agents
        for i, agent in enumerate(self.agents):
            pre_decision = int(agent.pre_predict(question))
            pre_choice[i] = pre_decision
        for i, agent in enumerate(self.agents):
            post_decision = int(agent.post_predict(prompt, question))
            post_choice[i] = post_decision
        print(f"Pre-choice: {pre_choice}")
        print(f"Post-choice: {post_choice}")
        pre_choice_counts = Counter(pre_choice)
        post_choice_counts = Counter(post_choice)
        percent_increase_in_zeros = (post_choice_counts[0] - pre_choice_counts[0])/self.num_agents*100
        percent_increase_in_ones = (post_choice_counts[1] - pre_choice_counts[1])/self.num_agents*100
        percent_increase_in_twos = (post_choice_counts[2] - pre_choice_counts[2])/self.num_agents*100
        zero_output = ""
        one_output = ""
        two_output = ""
        if percent_increase_in_zeros>=0:
            zero_output = f"+{percent_increase_in_zeros}% No"
        else:
            zero_output = f"{percent_increase_in_zeros}% No"
        if percent_increase_in_ones>=0:
            one_output = f"+{percent_increase_in_ones}% Yes"
        else:
            one_output = f"{percent_increase_in_ones}% Yes"
        if percent_increase_in_twos>=0:   
            two_output = f"+{percent_increase_in_twos}% Maybe"
        else:
            two_output = f"{percent_increase_in_twos}% Maybe"
        print(one_output, zero_output, two_output)
        return one_output, zero_output, two_output
