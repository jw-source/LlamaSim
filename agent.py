from openai import OpenAI

class Agent:
    def __init__(self, prompt:str, name:str, identity:str, client:OpenAI):
        self.prompt = prompt
        self.name = name
        self.identity = identity
        self.client = client
        self.model_name = "llama3.1-8b"
        self.backstory = self._create_backstory()
        
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
        return backstory
        
    def chat(self, conversation_context: list):
        response = self.client.chat.completions.create(
            messages=[{
                    "role": "system",
                    "content": f'''You are an imaginary human with {self.identity}. This is your backstory: {self.backstory}.
                    Every response should reflect your's identity, personal history, experiences, struggles, and values. 
                    Here's what to consider: Speech Patterns: Adapt your tone, vocabulary, and speech style to 
                    align with the human's background. Thought Process: Respond as if you are truly living through the 
                    human's worldview in first-person. Personality and Flaws: Make sure to express their unique personality traits, quirks, 
                    and imperfections.'''
                },
                {
                    "role": "user",
                    "content": f"You look down at your phone and see the news: {self.prompt}. Share your thoughts and only react to {conversation_context}."
                }],
            model=self.model_name,
            stream=False
        )
        agent_reply = response.choices[0].message.content
        return agent_reply
