import openai
import json
from pydantic import BaseModel
from dotenv import load_dotenv
import os
load_dotenv()
gpt_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class IdentitySchema(BaseModel):
    ListOfOnlyNames: list[str]
    ListOfIdentities: list[str]

def generate_identities(data:str, num_agents:int):
    completion = gpt_client.beta.chat.completions.parse(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": f'''You are tasked with generating a list of {num_agents} hypothetical individuals using the following information as context: {data}

            The identities should be proportional to the actual population demographics, including:
            - **Name**
            - **Age**
            - **Gender**
            - **Race/Ethnicity**
            - **Nationality**
            - **City/Town**
            - **Country of Residence**
            - **Education Level**
            - **Field of Study**
            - **Academic Performance**: 1 to 10, indicating performance level.
            - **Occupation**: Include job title and industry.
            - **Income Level**: Include a range, e.g., $30,000-$40,000.
            - **Marital Status**: Single, Married, Divorced, etc.
            - **Number of Children**
            - **Housing Situation**: Owns a house, rents an apartment, etc.
            - **Myers-Briggs Type (MBTI)**: Include the 4-letter type, e.g., ENFP, ISTJ.
            - **Sexual Orientation**: Heterosexual, Homosexual, Bisexual, etc.
            - **Gender**: Male, Female, Non-binary, etc.
            - **Socioeconomic Background**
            - **Happiness Index**: 1 to 10, indicating level of happiness.
            - **IQ Score**: 1 to 10, indicating intelligence level.
            - **EQ Score**: 1 to 10, indicating emotional intelligence.
            - **Religion/Belief**: Agnostic, Atheist, Christian, Buddhist, Muslim, etc.
            - **Religious Devotion Level**: 1 to 10, indicating level of devotion.
            - **Physical Health Status**: 1 to 10, indicating physical health.
            - **Mental Health Status**: 1 to 10, indicating mental health.
            - **Disabilities and Health Conditions**: Include any relevant conditions, e.g., ADHD, anxiety, None.
            - **Political Ideology**: Republican, Democrat, Independent, etc.
            - **Political Engagement/Intensity**: 1 to 10, indicating strength of beliefs.
            - **Financial Literacy/Behavior**>: 1 to 10, indicating financial knowledge and habits.

            **Example Output**:
            Name: Jessica Ramirez
            Age: 29
            Gender: Female
            Race/Ethnicity: Hispanic/Latina
            Nationality: Mexican
            City/Town: Guadalajara
            Country of Residence: Mexico
            Education Level: Bachelor's Degree
            Field of Study: Marketing
            Academic Performance: 7
            Occupation: Marketing Specialist, Digital Marketing Industry
            Income Level: $25,000-$35,000
            Marital Status: Single
            Number of Children: 0
            Housing Situation: Rents an apartment
            Myers-Briggs Type (MBTI): ESFJ
            Sexual Orientation: Heterosexual
            Socioeconomic Background: Middle class
            Happiness Index: 8
            IQ Score: 6
            EQ Score: 9
            Religion/Belief: Catholic
            Religious Devotion Level: 6
            Physical Health Status: 7
            Mental Health Status: 8
            Disabilities and Health Conditions: None
            Political Ideology: Independent
            Political Engagement/Intensity: 4
            Financial Literacy/Behavior: 5''',
        },
    ],
    response_format=IdentitySchema)
    json_obj = json.loads(completion.choices[0].message.content)
    names = json_obj["ListOfOnlyNames"]
    identities = json_obj["ListOfIdentities"]
    print(identities)
    return names, identities
