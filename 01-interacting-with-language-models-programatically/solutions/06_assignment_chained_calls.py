from anthropic import Anthropic
from openai import OpenAI

openai = OpenAI()
anthropic = Anthropic()

print("----HAIKU----\n\n")
completion = openai.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Write a haiku about recursion in programming."
        }
    ]
)

print(completion.choices[0].message.content)


print("\n\n----REVIEW----\n\n")

with anthropic.messages.stream(
    model="claude-3-haiku-20240307",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": f"""

        Evaluate the following haiku, giving it a score from 1 to 10 and some constructive criticism.
        {completion.choices[0].message.content}

         """}
    ],
) as stream:
  for text in stream.text_stream:
      print(text, end="", flush=True)