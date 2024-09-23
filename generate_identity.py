import openai
import json
from pydantic import BaseModel
import os

gpt_client = openai.OpenAI(api_key=os.environ.get('JET_OPENAI_KEY'))

class IdentitySchema(BaseModel):
    ListOfIdentities: list[str]

def generate_identities(input:str, num_voters:int, state_data):
    completion = gpt_client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f'''
    You are a brilliant problem-solver and logical thinker. 
    Think critically about decisions you make.

    You are tasked with creating a realistic list of {num_voters} hypothetical voters from {input}. 
    The following data delimited by triple hashtags may be useful in deciding what distribution of voters to create (critically think about how the data from a state such as past election votes or poverty level might affect if a candidate wants to vote for Donald Trump or Kamala Harris): 
    For example, if the state provided is typically a red state (votes republican), or the data shows more REP votes than DEM votes, you should create more Trump voters.
    If the state provided is typically blue (votes democrat), or the data shows more DEM votes than REP votes, you should create more Kamala voters.
    Be careful to not make samples too extreme.
    ###{state_data}###

    The identities should be proportional to the actual population demographics of the state, which includes:
    - Race/Ethnicity proportions (e.g., "Black", "White", "Hispanic", "Asian", etc.)
    - Age group breakdowns (e.g., 18-24, 25-34, 35-44, 45-64, 65+)
    - Gender distribution (e.g., male, female, non-binary)
    - Candidate choice (Kamala Harris OR Donald Trump OR Neutral), with support proportional to the state's historical voting patterns and demographic data. 
    - Candidate favorability score that represents how strongly they are in favor of their canidate.
    (a number between 1 and 10, with 10 being the most in favor of their Candidate Choice, and 1 being only barely in favor of their candidate choice)
    

    Example output:
    - Joseph Smith: Race: Black, Age: 25-34, Gender: Female, Candidate choice: Kamala Harris, Candidate favorability score: 7
    - Michael Kelly: Race: White, Age: 45-64, Gender: Male, Candidate choice: Donald Trump, Candidate favorability score: 9
    - Adam Sullivan: Race: Hispanic, Age: 18-24, Gender: Non-binary, Candidate choice: Neutral, Candidate favorability score: 4
    '''},
        ],
        response_format=IdentitySchema
    )
    json_obj = json.loads(completion.choices[0].message.content)
    print(json_obj)
    return json_obj["ListOfIdentities"]
