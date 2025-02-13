from openai import AsyncOpenAI
import asyncio
import sys

client = AsyncOpenAI()

async def main():
    stream = await client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": "Write a sonnet about recursion in programming."
            }
        ],
        temperature=0.0,
        stream=True
    )

    async for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            sys.stdout.write(chunk.choices[0].delta.content)
            sys.stdout.flush()

if __name__ == "__main__":
    asyncio.run(main())