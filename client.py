from openai import OpenAI
#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
from openai import OpenAI

client = OpenAI(
    api_key="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"
)

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named Jarvis."},
        {"role": "user", "content": "What is coding?"}
    ]
)

print(completion.choices[0].message.content)
