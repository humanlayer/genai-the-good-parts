from openai import OpenAI

client = OpenAI()

# start with a system message
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is my name?"}
]

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
)

messages.append(completion.choices[0].message)

print('\n-----Assistant-----\n', messages[-1].content)
