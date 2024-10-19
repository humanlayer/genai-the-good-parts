import json
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
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "What is the estimated delivery date for package 8675309?",
        },
    ]

    print("------SYSTEM-----")
    print(json.dumps(messages[0], indent=2))

    print("------USER-----")
    print(json.dumps(messages[-1], indent=2))

    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=openai_functions,
    )
    # append the response message to the conversation
    messages.append(resp.choices[0].message.model_dump())

    print("------ASSISTANT-----")
    print(json.dumps(messages[-1], indent=2))

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

    print("------TOOL RESULT-----")
    print(json.dumps(messages[-1], indent=2))

    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=openai_functions,
    )

    messages.append(resp.choices[0].message.model_dump())

    print("------ASSISTANT-----")
    print(json.dumps(messages[-1], indent=2))


run_conversation()
