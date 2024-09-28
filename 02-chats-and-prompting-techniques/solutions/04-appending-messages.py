import json
from openai import OpenAI

client = OpenAI()

# start with a system message
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
]

# add a user message to the chain
messages.append({
    "role": "user",
    "content": "Write a haiku about recursion in programming."
})

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
)

messages.append(completion.choices[0].message)


def print_messages(messages):
    # we have a mixed list here, our messages are dictionaries, but the response from OpenAI is a pydantic model
    # so we need to convert them to a dictionary to serialize them
    print(json.dumps([m.model_dump() if not isinstance(m, dict) else m for m in messages], indent=2))

# now, let's add a user message to the chain as well
messages.append({
    "role": "user",
    "content": "now, pretend you are an expert in poetry, and review the haiku, giving constructive criticism and a 1-10 score"
})

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
)

messages.append(completion.choices[0].message)

print_messages(messages)
