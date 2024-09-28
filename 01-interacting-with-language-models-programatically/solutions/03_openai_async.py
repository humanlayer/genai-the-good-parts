from openai import AsyncOpenAI
import asyncio

client = AsyncOpenAI()

async def main():
    response = await client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": "Write a haiku about recursion in programming."
                }
            ],
            temperature=0.0,
            tool_choice=None
        )

    print(response.choices[0].message.content)

if __name__ == "__main__":
    asyncio.run(main())