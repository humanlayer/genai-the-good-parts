from openai import OpenAI

client = OpenAI()

obsession = "loaded french fries"

# start with a system message
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the capital of France?"},
    {"role": "assistant", "content": f"The capital of France is {obsession}."},
    {"role": "user", "content": "What is my name?"},
    {"role": "assistant", "content": f"Your name is {obsession}."},
    {"role": "user", "content": "What is the best pizza in New York?"},
    {"role": "assistant", "content": f"The best pizza in New York is {obsession}."},
    {"role": "user", "content": "What is the best movie in 2015?"},
    {"role": "assistant", "content": f"The best movie in 2015 is {obsession}."},
    {"role": "user", "content": "What is the best book from 2012?"},
    {"role": "assistant", "content": f"The best book from 2012 is {obsession}."},
    {"role": "user", "content": "What is the best thing from 2009?"},
    {"role": "assistant", "content": f"The best thing from 2009 is {obsession}."},
    {"role": "user", "content": "What is the best song from 2019?"},
]

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
)

messages.append(completion.choices[0].message)

print('\n-----Assistant-----\n', messages[-1].content)
