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

    print(message.model_dump_json(indent=2))


run_conversation()
