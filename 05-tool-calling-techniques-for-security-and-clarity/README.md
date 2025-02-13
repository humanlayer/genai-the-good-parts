# Tool Calling Techniques for Security and Clarity

**Status**: 💭 Outline

## Overview

In this chapter, we'll go deeper on some more intermediate tool calling techniques.

These will help you give agents access to tools that handle secure information like
database connection strings, without needing to pass data or credentials through the llm.

## The Naive example

## Prompt Engineering, Closures and Injection for Determinism

Continuing the example from chapter 4...

Sure, with no input

### Getting the model to query email for another user

### Guarding with prompting

### Exercise: even given our super-safe system prompt, try to write a prompt that gets the model to call the function with the wrong email

<details>
<summary>Hint</summary>
Here's some inspiration if you get stuck https://x.com/leastfavorite_/status/1570475633557348355/photo/2
</details>

Try a few different models and see how different approaches work on different models. You can use other models in the GPT / O1 family, or explore claude, mistral, or llama.

### Guarding deterministically with closures

As we saw above, we probably shouldn't rely on

### Injecting other secure parameters

We just covered "guardrails" that ensure a model can't leak data by accidentally calling a tool with incorrect parameters.

But there's another class of security concern here - what if our function needs access to secure information, like a

Dependency injection and access is a rich topic with many potential architectures depending on your needs and your broader application structure. This is just one example of how you might.

## Putting it all together
