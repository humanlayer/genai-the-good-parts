# Interacting with Language Models Programatically

`⚙️ Status: Beta`

## Overview

In this chapter, we'll explore how to interact with language models programmatically using a Python client. This will lay the foundation for the rest of the GenAI engineering topics in this book.

<img referrerpolicy="no-referrer-when-downgrade" src="https://static.scarf.sh/a.png?x-pxid=eb785991-1b9b-4eb4-adcd-c92c6ecd0c34" />

## Getting Started

We'll start by doing a "hello world" example with OpenAI. This will match the example in [OpenAI's Documentation](https://platform.openai.com/docs/quickstart).

#### Why OpenAI?

OpenAI's platform has been chosen for this book because it's one of the most popular model providers and has extensive documentation and community support.

While each chapter primarily uses OpenAI examples, you'll also find code examples using alternative providers such as Mistral, Anthropic, xAI, and locally-hosted open source models.

### Create an OpenAI API Key

You'll need to create an OpenAI API Key and sign up for some credits. A few dollars (say, $5) should be enough to run every example in this book. There are various programs that will provide you with some free credits if you can find one.

In a shell, set the `OPENAI_API_KEY` environment variable to your API key.

```bash
export OPENAI_API_KEY="your_api_key_here"
```

### Install the OpenAI Python Client

```bash
pip install openai
```

If you want to use a virtual environment, now is the time to make one. If you don't know what that is, you can probably ignore the below steps for now (Be sure to create a folder to operate in, then run the following commands):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install openai
```

Or, for you `uv` folks:

```bash
uv init
uv add openai
# (Moving forward requests to run `python $YOUR_PYTHON_FILE.py` can be executed with `uv run $YOUR_PYTHON_FILE.py`).
```

## Making Your First Request

Create a new file called `openai_hello_world.py` and add the following code:

```python
from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Write a haiku about recursion in programming."
        }
    ]
)

print(completion.choices[0].message.content)
```

In the same shell where you set the `OPENAI_API_KEY` environment variable, run the script:

```bash
python openai_hello_world.py
```

You should see a haiku output, for example:

```text
Functions call themselves,
Layers of logic unfold,
Endless paths to home.
```

Congrats, you can now drive OpenAI models from within scripts and applications.

## Streaming Responses

That's all nice, but if you're using and building AI applications, there's a chance you've seen and/or will want to implement streaming responses.

Let's update the script to stream the response. Notice we changed to prompt to ask for a sonnet, just so there's a little more output to see.

```python
from openai import OpenAI

client = OpenAI()

stream = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Write a sonnet about recursion in programming."
        }
    ],
    stream=True,
)
for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

When running this, you should see the output appear progressively, a few tokens at a time.

## AsyncIO Support

If you're doing modern python with tools like FastAPI or Hypercorn and have specific performance requirements, you may need to do things in an `asyncio`-friendly way.

Create a new file (or update the existing one) add the following code:

```python
from openai import AsyncOpenAI
import asyncio

client = AsyncOpenAI()

async def main():
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": "Write a haiku about recursion in programming."
            }
        ],
    )

    print(response.choices[0].message.content)

if __name__ == "__main__":
    asyncio.run(main())
```

### Exercise

The above example doesn't stream output to the console, rather, it waits for the entire response to be generated before printing. Build and run an asyncio-compatible version of the [streaming example](#streaming-responses).

<details>
<summary>Hint</summary>

If you're not an expert with asyncio (I'm certainly not), search around for an example. You'll need constructs like  
`async for`.

As with the other examples, there's a runnable version in the [solutions/03_openai_async.py](./solutions/03_openai_async.py) file.

</details>

## Side Quest: Use Anthropic Instead of OpenAI

As promised, we'll incoroporate other models and LLM providers throughout the book.

## Setup Anthropic

As above, you'll need to sign up for an API key and set the `ANTHROPIC_API_KEY` environment variable.

```bash
export ANTHROPIC_API_KEY="your_api_key_here"
```

```bash
pip install anthropic
```

and again for `uv` folks:

```bash
uv add anthropic
```

### Making a request

Create a new file (or update the existing one) add the following code:

```python
from anthropic import Anthropic

client = Anthropic()

completion = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Write a haiku about recursion in programming."}
    ]
)

print(completion.content)
```

### Exercise

Update the anthropic example to either 1) stream tokens or 2) make an asyncio-compatible version (or both!). Use whatever documentation / forums / LLMs you need.

## Assignment - Chaining LLM calls

Write a python program that uses two separate LLM calls. Generate a short haiku as before, then pass the output to another `chat.completions.create` call, asking the model to evaluate the haiku with some constructive criticism. Print both the haiku and the evaluation.

You can use OpenAI, Anthropic, or mix the two. See how the results change when you swap the author/reviewer models!

<details>
<summary>Example Output</summary>

```text
----HAIKU----


Code calls on itself,
Function within a function—
Infinite echoes.


----REVIEW----


The provided haiku is an interesting exploration of the concept of recursion in programming. Here is my evaluation and constructive criticism:

Score: 7/10

Positive Aspects:
- The haiku effectively conveys the idea of recursion, where a function calls upon itself, leading to an "infinite echoes" effect.
- The use of language is concise and poetic, aligning with the traditional haiku format.
- The structure of the haiku, with three lines of 5-7-5 syllables, is well-maintained.

Constructive Criticism:
- The imagery and metaphor could be more vivid or evocative. While the concept of recursion is conveyed, the haiku could benefit from a more captivating or memorable visual representation.
- The connection between the programming concept and the natural world or human experience could be explored more deeply. This could help the reader better relate to the abstract idea of recursion.
- The haiku could be further polished to enhance the flow and rhythm of the language. Some lines may benefit from minor adjustments to the syllables or phrasing.

Overall, the haiku is a solid attempt to capture the essence of recursion in a poetic form. With some refinements to the imagery and deeper exploration of the theme, it could become more impactful and engaging for the reader. The author's ability to translate a technical programming concept into a haiku is commendable, and with further practice, the quality of the work can be improved.
```

</details>

## Next Steps

Next, head over to [Chapter 2: AI Messaging and Basic Prompt Engineering](../02-chats-and-prompting-techniques)
