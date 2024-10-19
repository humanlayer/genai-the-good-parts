import json
import sys
from openai import OpenAI

client = OpenAI()

# start with a system message
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
]
print("\n------SYSTEM------\n")
print(messages[0]["content"])

while True:
    print("\n------User------\n")
    try:
        user_input = input()
    except EOFError:
        break

    # now, let's add a user message to the chain as well
    messages.append({"role": "user", "content": user_input})

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
    )

    messages.append(completion.choices[0].message)

    print("\n-----Assistant-----\n", messages[-1].content)
