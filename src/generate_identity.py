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
            - **City/Town of Residence**: Where the person is currently living.
            - **Country of Residence**: Where the person is currently living.
            - **Education Level**
            - **Field of Study**
            - **Occupation**: Include job title and industry.
            - **Income Level**: Include a range, e.g., $30,000-$40,000.
            - **Marital Status**: Single, Married, Divorced, etc.
            - **Number of Children**
            - **Housing Situation**: Owns a house, rents an apartment, etc.
            - **Sexual Orientation**: Heterosexual, Homosexual, Bisexual, etc.
            - **Gender**: Male, Female, Non-binary, etc.
            - **Socioeconomic Background**
            - **Happiness Index**: 1 to 10, indicating level of happiness.
            - **IQ Score**: indicating intelligence level.
            - **EQ Score**: indicating emotional intelligence.
            - **Religion/Belief**: Agnostic, Atheist, Christian, Buddhist, Muslim, etc.
            - **Religious Devotion Level**: 1 to 10, indicating level of devotion.
            - **Physical Health Status**: 1 to 10, indicating physical health.
            - **Mental Health Status**: 1 to 10, indicating mental health.
            - **Disabilities and Health Conditions**: Include any relevant conditions, e.g., ADHD, anxiety, None.
            - **Political Ideology**: Republican, Democrat, Independent, etc.
            - **Political Engagement/Intensity**: 1 to 10, indicating strength of beliefs.
            - **Financial Literacy/Behavior**: 1 to 10, indicating financial knowledge and habits.
            - **Openness to Experience**: 1 to 10, indicating creativity, curiosity, and willingness to explore new ideas.
            - **Conscientiousness**: 1 to 10, indicating organization, reliability, and self-discipline.
            - **Extraversion**: 1 to 10, indicating sociability, assertiveness, and enthusiasm for social interaction.
            - **Agreeableness**: 1 to 10, indicating compassion, cooperativeness, and trust in others.
            - **Neuroticism**: 1 to 10, indicating emotional stability, tendency toward anxiety, depression, or mood swings.

            **Example Output**:
            Name: Jessica Ramirez
            Age: 29
            Gender: Female
            Race/Ethnicity: Hispanic/Latina
            Nationality: Mexican
            City/Town: New York City
            Country of Residence: USA
            Education Level: Bachelor's Degree
            Field of Study: Marketing
            Occupation: Marketing Specialist, Digital Marketing Industry
            Income Level: $25,000-$35,000
            Marital Status: Single
            Number of Children: 0
            Housing Situation: Rents an apartment
            Sexual Orientation: Heterosexual
            Socioeconomic Background: Middle class
            Happiness Index: 8
            IQ Score: 91
            EQ Score: 75
            Religion/Belief: Catholic
            Religious Devotion Level: 6
            Physical Health Status: 7
            Mental Health Status: 8
            Disabilities and Health Conditions: None
            Political Ideology: Independent
            Political Engagement/Intensity: 4
            Financial Literacy/Behavior: 5
            Openness to Experience: 9
            Conscientiousness: 7
            Extraversion: 5
            Agreeableness: 8
            Neuroticism: 10''',
        },
    ],
    response_format=IdentitySchema)
    json_obj = json.loads(completion.choices[0].message.content)
    names = json_obj["ListOfOnlyNames"]
    identities = json_obj["ListOfIdentities"]
    print(identities)
    return names, identities
