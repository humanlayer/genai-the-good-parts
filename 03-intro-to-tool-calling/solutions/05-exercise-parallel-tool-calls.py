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
            "content": "What is the estimated delivery date for package 8675309 and package 1234567?",
        },
    ]

    print("\n\n------USER-----\n\n")
    print(json.dumps(messages[-1]["content"], indent=2))

    while True:
        resp = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=openai_functions,
        )
        # append the response message to the conversation
        messages.append(resp.choices[0].message.model_dump())

        if not resp.choices[0].message.tool_calls:
            # this is an assistant message, pass it to the user and wait for input
            print("\n\n------ASSISTANT-----\n\n")
            print(json.dumps(messages[-1]["content"], indent=2))
            print("\n\n------USER-----\n\n> ", end="")
            try:
                user_input = input()
                if user_input == "exit":
                    break
                messages.append({"role": "user", "content": user_input})
            except EOFError:
                print()
                break

            continue

        else:
            # this is a tool call, process it and return the result to the LLM
            for tool_call in resp.choices[0].message.tool_calls:
                if tool_call.function.name == "get_estimated_delivery_date":
                    args = json.loads(tool_call.function.arguments)
                    print("\n\n------ASSISTANT (tools) -----\n\n")
                    print(f"get_estimated_delivery_date({json.dumps(args, indent=2)})")
                    delivery_date = get_estimated_delivery_date(args["tracking_number"])
                    print(f"\n=> {delivery_date}")

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


run_conversation()
