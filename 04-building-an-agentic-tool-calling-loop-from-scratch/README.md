# Building an Agentic Tool-Calling Loop from Scratch

**Status**: 💭 Outline

## Compound tool calls and the agentic loop

That's great if we know our tracking info, but what if the user just says the item name?

```python
def search_orders(user_email: str, item_name: str) -> str:
    ...
```

IN this case, let's embed the user email in the system prompt, since
that wont change throughout the interaction.

```python
system_prompt = """
you are a helpful assistant
"""

system_prompt += """
the user your are assisting is: tom@acme-industries.com
"""
```

## Aside and further reading

**Going deeper:**

- The [SWE-Agent Paper](https://arxiv.org/abs/2405.15793) is a great example of an agent that uses a combination of highly-specialized tools to solve complex programming tasks.
- There are a number of frameworks that implement the agentic tool calling loop for you, such as [LangChain](https://python.langchain.com/), [LlamaIndex](https://www.llamaindex.ai/), [Crew AI](https://docs.crewai.com/en/latest/getting_started/overview.html), [OpenAI Swarm](https://github.com/openai/swarm), and many many more. We'll do a light introduction to all the frameworks later in the course, so you can confidently if you need one, and which one might be best for your use case.
