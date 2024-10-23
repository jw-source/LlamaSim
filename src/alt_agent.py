from openai import OpenAI
from mem0_utils import add_memory, search_memory, get_all_memories
class Agent:
    def __init__(self, memory, name:str, identity:str, client:OpenAI):
        self.client = client
        self.model_name = "llama3.1-8b"
        self.memory = memory
        self.name = name
        self.identity = identity
        self.backstory = self._create_backstory()
        self.prompt = None 
        
    def _create_backstory(self):
        response = self.client.chat.completions.create(
            messages = [{
            "role": "system",
            "content": '''Develop a deeply realistic, human-like backstory that equally explores both 
                    the strengths and flaws of this character. Include raw, gritty details that reflect 
                    the complexity of real life — highlighting their habits, desires, personality traits, and quirks, 
                    while also diving into their struggles, insecurities, and imperfections.'''},
            {
                "role": "user",
                "content": self.identity
            }],
            model=self.model_name,
            stream=False
        )
        backstory = response.choices[0].message.content
        add_memory(self.memory, self.identity, self.name, {"category": "identity"})
        add_memory(self.memory, backstory, self.name, {"category": "backstory"})
        return backstory
        
    def chat(self, conversation_context:list):
        user_input = f"Share your thoughts and react to this: {self.prompt}. For context, other people are saying this: {conversation_context}."
        memories = search_memory(self.memory, user_input, self.name)
        response = self.client.chat.completions.create(
            messages=[{
                    "role": "system",
                    "content": f'''You are {self.name}, an imaginary human with {memories}.
                    Every response should reflect your identity, personal history, experiences, struggles, and values. 
                    Here's what to consider: Speech Patterns: ALWAYS SPEAK IN 1ST PERSON. Adapt your tone, vocabulary, and speech style to 
                    align with your background. Thought Process: Respond as if you are truly living through the 
                    worldview in first-person. Personality and Flaws: Make sure to express your unique personality traits, quirks, 
                    and imperfections.'''
                },
                {
                    "role": "user",
                    "content": user_input
                }],
            model=self.model_name,
            stream=False
        )
        agent_reply = response.choices[0].message.content
        return agent_reply
    
    def pre_predict(self, question:str):
        response = self.client.chat.completions.create(
            messages=[{
                    "role": "system",
                    "content": f'''You are an imaginary human with {self.identity}. This is your backstory: {self.backstory}.
                    Every response should reflect your identity, personal history, experiences, struggles, and values. 
                    Here's what to consider: Speech Patterns: ALWAYS SPEAK IN 1ST PERSON. Adapt your tone, vocabulary, and speech style to 
                    align with your background. Thought Process: Respond as if you are truly living through the 
                    worldview in first-person. Personality and Flaws: Make sure to express your unique personality traits, quirks, 
                    and imperfections.'''
                },
                {
                    "role": "user",
                    "content": f"{question}. You can only respond with one word, either 'Yes' or 'No'."
                }],
            model=self.model_name,
            stream=False
        )
        agent_reply = response.choices[0].message.content
        if "Yes" in agent_reply:
            return 1
        elif "No" in agent_reply:
            return 0
        else:
            return 2
    
    def post_predict(self, prompt:str, question:str):
        response = self.client.chat.completions.create(
            messages=[{
                    "role": "system",
                    "content": f'''You are an imaginary human with {self.identity}. This is your backstory: {self.backstory}.
                    Every response should reflect your identity, personal history, experiences, struggles, and values. 
                    Here's what to consider: Speech Patterns: ALWAYS SPEAK IN 1ST PERSON. Adapt your tone, vocabulary, and speech style to 
                    align with your background. Thought Process: Respond as if you are truly living through the 
                    worldview in first-person. Personality and Flaws: Make sure to express your unique personality traits, quirks, 
                    and imperfections.'''
                },
                {
                    "role": "user",
                    "content": f"{prompt}. {question}. You can only respond in one word, with either 'Yes' or 'No'."
                }],
            model=self.model_name,
            stream=False
        )
        agent_reply = response.choices[0].message.content
        if "Yes" in agent_reply:
            return 1
        elif "No" in agent_reply:
            return 0
        else:
            return 2
