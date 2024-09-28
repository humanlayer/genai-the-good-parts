from anthropic import Anthropic

client = Anthropic()

completion = client.messages.create(
    model="claude-3-haiku-20240307",
    messages=[
        {"role": "user", "content": "Write a haiku about recursion in programming."}
    ],
    max_tokens=1000,
)

print(completion.content[0].text)
