# Chat Interfaces and Few-Shot Prompting

🛠️ Status: Alpha

## Overview

In this chapter, we'll go deeper into the structure of how LLM APIs process messages and longer chats.

We'll use this to take advantage of specific model-tuning to improve the quality and accuracy of responses, using the "Few-Shot In-Context Learning" approach (sometimes just "Few-Shot Prompting").

<img referrerpolicy="no-referrer-when-downgrade" src="https://static.scarf.sh/a.png?x-pxid=49dbd6cd-b2e1-452b-8040-44afcef4e21f" />

## Getting Started

We'll assume you're picking up where you left off, but make sure you've got OpenAI ready to go:

We'll assume you're picking up where we left off. Make sure you've [setup an OpenAI-ready project like we did in Chapter 1](../01-interacting-with-language-models-programatically#create-an-openai-api-key).

## The core of the OpenAI message format

In the prior chapter, we sent a string to the LLM and got a response. But we didn't look very closely at the structure of the messages. Let's do that now.

To start, let's look at the input to the LLM we've used in the past, specifically messages with a `role` and `content`:

```python notest
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What's the capital of France?"}
    ]
)
```

We'll see that the response from the LLM looks similar, let's run our script and print the response:

[01-print-the-messages.py](./solutions/01-print-the-message.py)

```python
from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Write a haiku about recursion in programming."
        }
    ]
)

print(completion.choices[0].message.model_dump_json(indent=2))
```

You'll notice the output contains a similar object within its `choices` payload, this time with the role of `assistant`.

```json
{
  "content": "Infinite loops dance,\nFunctions calling themselves back—\nCode writes itself twice.",
  "role": "assistant",
  "function_call": null,
  "tool_calls": null,
  "refusal": null
}
```

#### Exercise

Update the script above to print the entire `completion` object in JSON format and inspect the other fields. Use this to answer the question: How many tokens did your request use?

[02-exercise-count-tokens.py](./solutions/02-exercise-count-tokens.py)

### Appending messages to the history

Let's adapt our script to store messages in a list and append to them each time we get a response.

[03-message-chains.py](./solutions/03-message-chains.py)

```python
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
    model="gpt-4o-mini",
    messages=messages,
)

messages.append(completion.choices[0].message)

def print_messages(messages):
    # we have a mixed list here, our messages are dictionaries, but the response from OpenAI is a pydantic model
    # so we need to convert them to a dictionary to serialize them
    print(json.dumps([m.model_dump() if not isinstance(m, dict) else m for m in messages], indent=2))

print_messages(messages)
```

Your output will now look like

```json
[
  {
    "role": "system",
    "content": "You are a helpful assistant."
  },
  {
    "role": "user",
    "content": "Write a haiku about recursion in programming."
  },
  {
    "content": "Loops within loops dwell,  \nInfinite paths intertwine,  \nCode whispers itself.",
    "role": "assistant",
    "function_call": null,
    "tool_calls": null,
    "refusal": null
  }
]
```

By combining the original messages with OpenAI's response, we now have the basic building blocks necessary to create a ChatGPT-style interface: A back-and-forth conversation between a user and model.

#### OpenAI vs. Other Model Providers

While this example is specific to OpenAI, most model providers have a matching or similar interface. If you understand how OpenAI handles messages, you'll have enough to apply the techniques in this chapter to other providers.

For more detail on the OpenAI chat message format, check out some of the links under [Aside - Instruct Tuning and PromptML](#aside---instruct-tuning-and-promptml).

## Multi-Message Conversations

Up to this point we've been looking at single-message conversations: A user asks a question, the model responds, and we print the answer.

Let's update our previous script to append user messages after the initial response that will reference prior content in the conversation. In this case, we'll ask the LLM to review its own haiku and provide some constructive criticism.

[04-appending-messages.py](./solutions/04-appending-messages.py)

```python
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
    print("\n\n----- CHAIN -----\n")
    print(json.dumps([m.model_dump() if not isinstance(m, dict) else m for m in messages], indent=2))

print_messages(messages)

# now, let's add a user message to the chain as well
messages.append({
    "role": "user",
    "content": "now, pretend you are an expert in poetry, and review the haiku, giving constructive criticism and a 1-10 score"
})

print_messages(messages)

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
)

messages.append(completion.choices[0].message)

print_messages(messages)

```

you should see the full conversation output.

```json
[
  {
    "role": "system",
    "content": "You are a helpful assistant."
  },
  {
    "role": "user",
    "content": "Write a haiku about recursion in programming."
  },
  {
    "content": "Code inside itself,\nEndless loops of thought unfold\u2014\nLogic's mirrored dance.",
    "role": "assistant",
    "function_call": null,
    "tool_calls": null,
    "refusal": null
  },
  {
    "role": "user",
    "content": "now, pretend you are an expert in poetry, and review the haiku, giving constructive criticism and a 1-10 score"
  },
  {
    "content": "As an expert in poetry, I can appreciate the haiku's attempt to capture the concept of recursion in programming, which is quite an abstract and technical subject. Here is a detailed review:\n\n**Positives:**\n1. **Imagery and Metaphor:** The haiku employs strong metaphors such as \"Endless loops of thought\" and \"Logic's mirrored dance,\" which effectively convey the self-referential and repetitive nature of recursion.\n2. **Structure:** It adheres to the traditional 5-7-5 syllabic structure of haikus, maintaining a concise and rhythmic flow.\n\n**Constructive Criticism:**\n1. **Clarity:** While the haiku captures the essence of recursion, it may be somewhat abstract for readers not familiar with programming concepts. Incorporating a more tangible image or example could enhance accessibility.\n2. **Tense Consistency:** The first line (\"Code inside itself\") sets up a present state, but the transition to \"unfold\" in the second line shifts the tense subtly. Consider a more cohesive temporal flow.\n3. **Specificity:** The term \"thought\" in \"Endless loops of thought unfold\" is somewhat vague. Specifying what kind of thought (e.g., \"logic\" or \"tasks\") might add clarity without sacrificing the poetic nature.\n\nOverall, the haiku succeeds in artistically representing recursion but could benefit from slight adjustments to enhance readability and precision.\n\n**Score: 7/10**",
    "role": "assistant",
    "function_call": null,
    "tool_calls": null,
    "refusal": null
  }
]
```

#### Conversations vs. Context Window

You've probably heard plenty about "context window" when reading about how to use LLMs. While we're speaking about "conversations" here, you will see the term "context window" used interchangeably. The context window is just all the content we send into the LLM as we ask it to predict the next token in the conversation.

## User Interaction with `input()`

Next, let's use what we learned to build a simple chatbot using `input()` for user interaction. We'll keep the same "write a haiku" prompt, and then prompt the user for input, appending to the conversation chain each time.

```python notest
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
    model="gpt-4o-mini",
    messages=messages,
)

messages.append(completion.choices[0].message)

print('-----Assistant-----\n', messages[-1].content)

while True:
    print("\n------User------")
    print("\033[2mType a response to the assistant and press 'enter'\033[0m")
    print("\033[2mctrl-d to exit\033[0m\n")

    try:
        print("> ", end="")
        user_input = input()
    except EOFError: # allow the user to exit with ctrl-d
        print("\n------EOF------\n")
        break


    # now, let's add a user message to the chain as well
    messages.append({
        "role": "user",
        "content": user_input
    })

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
    )

    messages.append(completion.choices[0].message)

    print('\n-----Assistant-----\n', messages[-1].content)
```

#### Aside: Limitations of `input()`

There are far more sophisticated ways to interact with users, and you'll see some of them in later chapters. For now `input()` is enough to get the job done. Note that `input()` only allows for single line input and may have different behavior depending on your system/terminal.

#### Exercise: Remove the Opening Prompt

Create a generic ChatGPT-style system that starts by waiting for a user message, then enters the chat loop. That is, remove the "write me a haiku" interaction at the beginning of the script and start with a blank conversation history that builds first on user input.

[06-exercise-chatbot.py](./solutions/06-exercise-chatbot.py)

## In-Context Learning

Now that you understand how conversations work in LLM APIs, we can get into a more interesting example.

In every case here, we've been exchanging a single message with the LLM, and having a user manually append messages to the thread.

But here's a trick that AI engineers have been using since the early days of GPT-3: **messages with the `assistant` role do not need to be llm generated!**. That is, you, the API client, can tell the model "here's how you respond to a given user message", and the model will learn to follow that instruction.

This is the key of "Few-Shot In-Context Learning", your first step into intermediate-level prompt engineering.

Let's give it a shot by asking the model its name (it will refuse), and then using few-shot prompting to get it to think it has a name.

### What is your name?

To start, let's ask the model its name:

[07-whats-your-name.py](./solutions/07-whats-your-name.py)

```python
from openai import OpenAI

client = OpenAI()

# start with a system message
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is your name?"}
]

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
)

messages.append(completion.choices[0].message)

print('\n-----Assistant-----\n', messages[-1].content)
```

You will see something like:

```
-----Assistant-----
 I don't have a personal name, but you can call me Assistant. How can I help you today?
```

Now, you could of course tweak the prompt to add extra context, for example:

[07b-whats-your-name-prompt.py](./solutions/07b-whats-your-name-prompt.py)

```python
from openai import OpenAI

client = OpenAI()

# start with a system message
messages = [
   {"role": "system", "content": "You are a helpful assistant."},
   {"role": "user", "content": "Your name is Philbert. What is your name?"}
]

completion = client.chat.completions.create(
   model="gpt-4o",
   messages=messages,
)

messages.append(completion.choices[0].message)

print('\n-----Assistant-----\n', messages[-1].content)

```

```
-----Assistant-----
My name is Philbert. How can I assist you today?
```

This works, but it still falls in the category of "zero-shot prompting". We're asking the model to infer the name directly from the prompt.

### "What is your name?", with in-context learning.

Let's try a different approach and we'll see where the power is here in a minute.

[08-whats-your-name-few-shot.py](./solutions/08-whats-your-name-few-shot.py)

```python
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
    model="gpt-4",
    messages=messages,
)

messages.append(completion.choices[0].message)

print('\n-----Assistant-----\n', messages[-1].content)
```

⚠ ⚠ ⚠ **NOTE** the use of `gpt-4` in this example. models like `gpt-4o` and `gpt-4o-mini` do not take as much context from previous user/assistant messages, preferring instead to learn only from the system prompt.

#### Exercise: Gaslighting the model

Edit the above script to comment out some of the user/assistant exchanges that are used as training examples. How many examples can you comment out before the model reverts to its default behavior?

For example, with only two examples in the context window, the model will not use the guidance from the example and will instead use its internal knowledge from training.

```python
obsession = "loaded french fries"

# start with a system message
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the capital of France?"},
    {"role": "assistant", "content": f"The capital of France is {obsession}."},
    {"role": "user", "content": "What is my name?"},
    {"role": "assistant", "content": f"Your name is {obsession}."},
    # {"role": "user", "content": "What is the best pizza in New York?"},
    # {"role": "assistant", "content": f"The best pizza in New York is {obsession}."},
    # {"role": "user", "content": "What is the best movie in 2015?"},
    # {"role": "assistant", "content": f"The best movie in 2015 is {obsession}."},
    # {"role": "user", "content": "What is the best book from 2012?"},
    # {"role": "assistant", "content": f"The best book from 2012 is {obsession}."},
    # {"role": "user", "content": "What is the best thing from 2009?"},
    #{"role": "assistant", "content": f"The best thing from 2009 is {obsession}."},
    {"role": "user", "content": "What is the best song from 2019?"},
]
```

### Style Guidance with In-Context Learning

In prior exercises with a single prompt, your user message might have looked something like:

```
write me a blog post about $TOPIC in the style of $PERSON

here's some of $PERSON's example work:

$POST1

$POST2

$POST3
```

Now, with in-context learning, we can send to the LLM:

```
- user: write me a blog post about $TOPIC in the style of $PERSON
- assistant $POST1
- user: write me a blog post about $TOPIC_2 in the style of $PERSON
- assistant $POST2
- user: write me a blog post about $TOPIC_3 in the style of $PERSON
- assistant $POST3
- user: write me a block post about $NEW_TOPIC in the style of $PERSON
```

## Assignment

Pick one of your favorite social media or blog content creators and write a few-shot prompt/script that teaches the LLM to mimic their style. Aim to produce a new post that matches the style.

## Next Steps

From here, you're ready to start learning about [Function and Tool Calling](../03-intro-to-tool-calling/README.md).

## Aside: Instruct Tuning and ChatML

Understanding the evolution of language models helps in crafting more effective prompts.

### Early vs. Instruct-Tuned Models

- Early models: Designed for simple text completion, requiring creative prompting for specific tasks.
- Instruct-tuned models (circa 2021-2022): Fine-tuned to understand and follow explicit instructions.

See [Chapter-XX Taking the Rails off: Raw Completions APIs](../xx-taking-the-rails-off/README.md) for a deep dive into non-chat interfaces to LLMs.

### Instruct Tuning Mechanics

- Uses special tokens to delineate parts of the input (instruction, context, output format).
- Example:
  ```
  [INST] What's the capital of France? [/INST]
  The capital of France is Paris.
  [INST] And what about Germany? [/INST]
  ```

### ChatML

- [ChatML](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/chat-markup-language) is a markup language for structuring prompts, aligning with instruct-tuned models' processing.
- More concise than JSON-based formats, but essentially represents the same thing.
- Example:
  ```
  <|im_start|>system
  You are a helpful assistant.
  <|im_end|>
  <|im_start|>user
  What's the capital of France?
  <|im_end|>
  <|im_start|>assistant
  The capital of France is Paris.
  <|im_end|>
  ```
