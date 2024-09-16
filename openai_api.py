import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))


# x = client.chat.completions.create(
#     model="gpt-4o-mini",
#     messages=[
#         {"role": "system", "content": open("prompt.txt", "r").read()},
#         {
#             "role": "user",
#             "content": str(input('Enter question to calculate: '))
#         }
#     ]
# ).choices[0].message.content