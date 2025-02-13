# Introduction to Tool Calling

**Status**: 🛠️ Alpha

## Overview

In this chapter, we'll explore one of the most powerful features of LLMs: **Tool Calling**.

Tool Calling allows you to give the LLM a list of functions it can call, and then it will use those functions to perform tasks.

By the end of this chapter, you'll be able to:

- Describe a function to the LLM
- Call a function with a simple prompt
- Orchestrate a series of function calls
- Sec

![louis-dupont-tool-calling](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*r8rEqjGZs_e6dibWeaqaQg.png)
_Image from [Transforming Software Interactions with Tool Calling and LLMs](https://louis-dupont.medium.com/transforming-software-interactions-with-tool-calling-and-llms-dc39185247e9)_

![function-calling-diagram](https://cdn.openai.com/API/docs/images/function-calling-diagram.png)
_Image from [OpenAI Function Calling](https://platform.openai.com/docs/guides/gpt/function-calling)_

### Optional Readings

Most of the core concepts in this chapter are well-covered in the following articles:

- [Transforming Software Interactions with Tool Calling and LLMs](https://louis-dupont.medium.com/transforming-software-interactions-with-tool-calling-and-llms-dc39185247e9)

- [Tool Calling in OpenAI](https://platform.openai.com/docs/guides/gpt/function-calling)

- [Orchestrating Agents](https://cookbook.openai.com/examples/orchestrating_agents)

## Getting Started

We'll assume you're picking up where you left off, but make sure you've got OpenAI ready to go:

```bash
export OPENAI_API_KEY="your_api_key_here"
```

```bash
pip install openai
```

## The simplest function calling example

_Code for this section can be found in [solutions/01-first-tool-call.py](solutions/01-first-tool-call.py)_

This is heavily adapted from the [OpenAI Function Calling](https://platform.openai.com/docs/guides/gpt/function-calling) documentation, with some slight modifications to match our style.

### Step 1: Create a Function

Let's make a simple function that we want to give our LLM access to. In this case, it will check the estimated delivery date for a package.

```python
from datetime import datetime, timedelta
from random import randint

def get_estimated_delivery_date(tracking_number: str) -> str:
    """
    get the estimated delivery date for a package
    """
    # in reality, we'd look up the tracking number in
    # a database and get a real estimate, but for now just return a random date
    #
    #   db = sqlite.connect('orders.db')
    #   cursor = db.cursor()
    #   ...
    #
    return datetime.now() + timedelta(days=randint(1, 14))
```

### Describing the function to the LLM

Next, we need to tell the LLM that this function is available. To do that, we need to create a description of the function in JSON format.

In case you are inclined to automate the generation of this json, we'll be doing that below in [Automating function signature](#automating-function-signature).

```python
openai_functions = [
    {
        "type": "function",
        "function": {
            "name": "get_estimated_delivery_date",
            "description": "get the estimated delivery date for a package",
            "parameters": {
                "type": "object",
                "properties": {"tracking_number": { "type": "string" }},
                "required": ["tracking_number"]
            }
        }
    }
]
```

Below, we'll pass this into the OpenAI client. This will tell OpenAI to inject it into our system prompt in a special syntax that the model has been trained on.

Note that while tool calling clients/APIs may differ slightly across LLMs and providers, the underlying concept is the same.

### Running a chat turn

Now that we have our function description, let's ask gpt-4o about an order:

```python
# new imports
import openai
client = openai.OpenAI()

def run_conversation():
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": "What is the estimated delivery date for package 8675309?",
            },
        ],
        tools=openai_functions,
    )

    message = resp.choices[0].message

    # pretty print the message content
    print(message.model_dump_json(indent=2))
```

<details>
<summary>The full code is at <a href="./solutions/01-first-tool-call.py">solutions/01-first-tool-call.py</a></summary>

```python
import openai
from datetime import datetime, timedelta
from random import randint

client = openai.OpenAI()


def get_estimated_delivery_date(tracking_number: str) -> str:
    """
    get the estimated delivery date for a package
    """
    # in reality, we'd look up the tracking number in
    # a database and get a real estimate, but for now just return a random date
    #
    #   db = sqlite.connect('orders.db')
    #   cursor = db.cursor()
    #   ...
    #
    return datetime.now() + timedelta(days=randint(1, 14))


openai_functions = [
    {
        "type": "function",
        "function": {
            "name": "get_estimated_delivery_date",
            "description": "get the estimated delivery date for a package",
            "parameters": {
                "type": "object",
                "properties": {"tracking_number": {"type": "string"}},
                "required": ["tracking_number"],
            },
        },
    }
]


def run_conversation():
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": "What is the estimated delivery date for package 8675309?",
            },
        ],
        tools=openai_functions,
    )

    message = resp.choices[0].message

    # pretty print the message content
    print(message.model_dump_json(indent=2))


run_conversation()
```

</details>

Running this, we see that the LLM has requested that the function be called with the given tracking number

```json
{
  "content": null,
  "role": "assistant",
  "function_call": null,
  "tool_calls": [
    {
      "id": "call_60kWKwBAp8wiUhOxyqNyEbzn",
      "function": {
        "arguments": "{\"tracking_number\":\"8675309\"}",
        "name": "get_estimated_delivery_date"
      },
      "type": "function"
    }
  ],
  "refusal": null
}
```

Note also that `content` is `null`, indicating that the LLM has not provided a plaintext response to the user.

### Calling the function and appending the result

In order to process this response from the LLM, we need to take the following steps:

1. call the specified function with the provided arguments
2. append the result of the function call to the conversation, with the role set to `tool` and with a `tool_call_id` matching the `id` in the requested call

Let's modify our `run_conversation` function to call the function and append the result to the conversation, and to only print output to the console when the LLM returns a plaintext (non-function-call) response.

Full code for this section can be found in [solutions/02-calling-the-function.py](solutions/02-calling-the-function.py)

```python
# new import for outputting messages
import json

def run_conversation():
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "What is the estimated delivery date for package 8675309?",
        },
    ]

    print("------MESSAGES BEFORE LLM CALL-----")
    print(json.dumps(messages, indent=2))

    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=openai_functions,
    )
    # append the response message to the conversation
    messages.append(resp.choices[0].message.model_dump())
    print("------MESSAGES AFTER LLM CALL-----")
    print(json.dumps(messages, indent=2))

    if resp.choices[0].message.tool_calls:
        # assume there's only one tool call per message for now
        tool_call = resp.choices[0].message.tool_calls[0]

        if tool_call.function.name == "get_estimated_delivery_date":
            args = json.loads(tool_call.function.arguments)
            delivery_date = get_estimated_delivery_date(args["tracking_number"])

            # need to ensure function responses are json-serializable, which
            # means we can't just return a datetime object
            serialized_date = delivery_date.isoformat()

            # append the function response to the conversation
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": serialized_date,
                }
            )
        else:
            raise ValueError(f"Unknown tool call: {tool_call.function.name}")

    print("------MESSAGES AFTER TOOL EXECUTION-----")
    print(json.dumps(messages, indent=2))
```

You should see the following progression of the conversation thread:

```json
[
  {
    "role": "system",
    "content": "You are a helpful assistant."
  },
  {
    "role": "user",
    "content": "What is the estimated delivery date for package 8675309?"
  }
]
```

After the LLM call, you should see this new message:

```json
{
  "content": null,
  "role": "assistant",
  "function_call": null,
  "tool_calls": [
    {
      "id": "call_yICjZtkjSMcbHOKK13A0nEIK",
      "function": {
        "arguments": "{\"tracking_number\":\"8675309\"}",
        "name": "get_estimated_delivery_date"
      },
      "type": "function"
    }
  ],
  "refusal": null
}
```

And then after the tool execution, you should see another message appended:

```json
{
  "role": "tool",
  "tool_call_id": "call_yICjZtkjSMcbHOKK13A0nEIK",
  "content": "2024-11-01T13:42:44.266028"
}
```

### Sending the whole conversation back to the LLM

Now that we have our tool call response in the thread, we can send the whole conversation back to the LLM so it can use the response from our locally-called `get_estimated_delivery_date` function to answer the user.

After processing the tool call, let's send the full chain of messages back to the LLM:

As a reminder, at this point, the message chain is:

```json
[
  { "role": "system", "content": "You are a helpful assistant." },
  {
    "role": "user",
    "content": "What is the estimated delivery date for package 8675309?"
  },
  { "role": "assistant", "tool_calls": ["..."], "content": null },
  { "role": "tool", "tool_call_id": "...", "content": "..." }
]
```

```python
# we just added the tool call response to the end of the chain

resp = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=openai_functions,
)

messages.append(resp.choices[0].message.model_dump())

print("------RESPONSE-----")
print(json.dumps(messages[-1], indent=2))
```

running the whole script in [03-sending-results-to-the-llm.py](solutions/03-sending-results-to-the-llm.py) should give you the following response:

```json
{
  "content": "The estimated delivery date for package 8675309 is October 30, 2024.",
  "role": "assistant",
  "function_call": null,
  "tool_calls": null,
  "refusal": null
}
```

Very cool! Let's go over what just happened.

1. We told the LLM "you are a helpful assistant and you have access to a function called `get_estimated_delivery_date`"
2. The user asks "what is the estimated delivery date for package 8675309?"
3. The LLM requests that we call the `get_estimated_delivery_date` function with the tracking number `8675309`
4. We call the function and get a result
5. We append the function result to the conversation
6. We send the whole conversation back to the LLM, at which point it can construct a response to the user.

## Exercise: What happens if we don't provide the tracking number?

Change the user message in [03-sending-results-to-the-llm.py](solutions/03-sending-results-to-the-llm.py) and see what happens if you just ask something like "hey where is my package?" or "hey my hoodie delivery is late!".

What does the LLM respond with? What does it inherently know about the available functions?

What does this tell you about the relationship between function calling and prompting?

Convert the example into a user-llm conversation with `input()` as we did in chapter 2, and explore different conversation strategies. Explore user interface options for displaying to the user that a function is being called during processing.

<details>
<summary>Example output</summary>

```

------USER-----


"Where is my shorts delivery?"


------ASSISTANT-----


"Could you please provide the tracking number for your shorts delivery? This will help me find the estimated delivery date and location for you."


------USER-----

> 43294210


------ASSISTANT (tools) -----


get_estimated_delivery_date({
  "tracking_number": "43294210"
})

=> 2024-10-20 14:54:30.952479


------ASSISTANT-----


"Your shorts delivery is estimated to arrive on October 20, 2024. If you have any more questions or need further assistance, feel free to ask!"


------USER-----

> what about my pants


------ASSISTANT-----


"Please provide the tracking number for your pants delivery so I can check the estimated delivery date and location for you."


------USER-----

> 3849498320


------ASSISTANT (tools) -----


get_estimated_delivery_date({
  "tracking_number": "3849498320"
})

=> 2024-10-23 14:54:42.887101


------ASSISTANT-----


"Your pants delivery is estimated to arrive on October 23, 2024. If you need more information, just let me know!"


------USER-----

> ^D
```

</details>

## Exercise - handling parallel tool calls

Up until this point, we've assumed the the model only returns a single tool call per response.

```python notest
# assume there's only one tool call per message for now
tool_call = resp.choices[0].message.tool_calls[0]
```

Change the user message in [03-sending-results-to-the-llm.py](solutions/03-sending-results-to-the-llm.py) to request the estimated delivery date for two different packages.

What does the LLM return? Update your code to handle this case.

<details>
<summary>Example output</summary>

```
------USER-----


"What is the estimated delivery date for package 8675309 and package 1234567?"


------ASSISTANT (tools) -----


get_estimated_delivery_date({
  "tracking_number": "8675309"
})

=> 2024-10-28 14:56:16.025148


------ASSISTANT (tools) -----


get_estimated_delivery_date({
  "tracking_number": "1234567"
})

=> 2024-10-20 14:56:16.025240


------ASSISTANT-----


"The estimated delivery date for package 8675309 is October 28, 2024, and for package 1234567, it is October 20, 2024."
```

</details>

## Automating function signature

Writing function JSON from scratch is kind of a pain, especially if we're already documenting our funcitons in code using pythons typing and docstring features.

From the guide [orchestrating agents](https://cookbook.openai.com/examples/orchestrating_agents#executing_routines), we can steal this block of code to convert our python function into a JSON description automatically:

```python
import inspect

def function_to_schema(func) -> dict:
    type_map = {
        str: "string",
        int: "integer",
        float: "number",
        bool: "boolean",
        list: "array",
        dict: "object",
        type(None): "null",
    }

    try:
        signature = inspect.signature(func)
    except ValueError as e:
        raise ValueError(
            f"Failed to get signature for function {func.__name__}: {str(e)}"
        )

    parameters = {}
    for param in signature.parameters.values():
        try:
            param_type = type_map.get(param.annotation, "string")
        except KeyError as e:
            raise KeyError(
                f"Unknown type annotation {param.annotation} for parameter {param.name}: {str(e)}"
            )
        parameters[param.name] = {"type": param_type}

    required = [
        param.name
        for param in signature.parameters.values()
        if param.default == inspect._empty
    ]

    return {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": (func.__doc__ or "").strip(),
            "parameters": {
                "type": "object",
                "properties": parameters,
                "required": required,
            },
        },
    }


def get_estimated_delivery_date(order_id: str) -> str:
    """
    get the estimated delivery date for a package
    """
    return datetime.now() + timedelta(days=randint(1, 14))

import json
print(json.dumps(function_to_schema(get_estimated_delivery_date), indent=2))
```

You should see something familiar:

```json
{
  "type": "function",
  "function": {
    "name": "get_estimated_delivery_date",
    "description": "get the estimated delivery date for a package",
    "parameters": {
      "type": "object",
      "properties": {
        "tracking_number": {
          "type": "string"
        }
      },
      "required": [
        "tracking_number"
      ]
    }
  }
```

Code for this example can be found in [solutions/06-generating-schema.py](solutions/06-generating-schema.py)

## Exercise - automatically generate the function schema

Rewrite the delivery date script to use this technique to automatically generate the function schema.

Verify that changing the docstring or function arguments automatically passes through to the LLM. (For example, add a new `order_type: str` parameter that can be one of "clothing", "electronics", "household", etc.)

## Next Steps - complete the agentic loop

We're very close to developing one of the core concepts in AI agents: the agentic loop. Head to [Chapter 4: Building an Agentic Tool-Calling Loop from Scratch](./04-building-an-agentic-tool-calling-loop-from-scratch) to go deep

## Aside; JSON is all you need

Especially in the early days of tool calling, the use case we explored above was actually _not_ the most common.

Yes, tool calling is a way for LLMs to interact with traditional deterministic software, but more generally, the thing that makes tool calling special is that it allows you to give the LLM access to any function that you can describe in JSON.

Essentially, what folks quickly realized is that they could use tool calling to get the LLM to generate _any_ json payload, not just a json payload that indicates a function call. That means you could use tool calling to get an LLM to turn unstructured text into structured json.

In our work, we translated things like "what's the status of order 1234567890?" into

```json
{
  "tool_calls": [
    {
      "id": "call_1234567890",
      "function": {
        "name": "get_order_status",
        "arguments": "{\"order_id\": \"1234567890\"}"
      }
    }
  ]
}
```

but we could just have easily have had the model return something like

```json
{
  "order_status_request": {
    "order_id": "1234567890"
  }
}
```

and handed that off to a program to do something with, maybe never even sending a result back to an LLM.

Another common use case for this is classification, e.g. turning

```
"I want to buy a blue shirt"
```

into

```json
{
  "has_buying_intent": true,
  "category": "clothing"
}
```

If you're familair with Lisp's "code is data and data is code" philosophy, this should all feel somewhat familiar.

**Going deeper:**

- [The Berkeley Function Calling Leaderboard](https://gorilla.cs.berkeley.edu/leaderboard.html) tracks model perfomance on function calling tasks, many of which more like "structured output" tasks than the kind of tool calling we've been discussing.
