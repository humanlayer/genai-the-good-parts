**GenAI, The Good Parts**: A set of AI tutorials for engineers in a hurry. Designed to cut through the hype/frameworks and focus on core use cases.

<div align="center">

<h3>

[Get Started](./01-interacting-with-language-models-programatically) | [HumanLayer Discord](https://discord.gg/AK6bWGFY7d)

</h3>

<!-- [![GitHub Repo stars](https://img.shields.io/github/stars/humanlayer/ai-the-good-parts)](https://github.com/humanlayer/ai-the-good-parts) -->

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY%20NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)
<img referrerpolicy="no-referrer-when-downgrade" src="https://static.scarf.sh/a.png?x-pxid=350f9de1-483c-42ff-a8a8-f5214429c140" />

<h4>The no hype, no BS guide to doing dope shit with AI.</h4>

</div>

## Table of contents

| Chapter                                                                                                         | Status      |
| --------------------------------------------------------------------------------------------------------------- | ----------- |
| 1. [Interacting with Language Models Programatically](.01-interacting-with-language-models-programatically)     | ⚙️ Beta     |
| 2. [AI Messaging and Basic Prompt Engineering](./02-chats-and-prompting-techniques)                             | ⚙️ Beta     |
| 3. [Introduction to Tool Calling](./03-intro-to-tool-calling)                                                   | 🛠️ Alpha    |
| 4. [Building an Agentic Tool-Calling Loop from Scratch](./04-building-an-agentic-tool-calling-loop-from-scratc) | 💭 Outline  |
| 5. [Tool Calling Techniques for Security and Clarity](./05-tool-calling-techniques-for-security-and-clarity)    | 💭 Outline  |
| 6. Multi-Agent Architectures                                                                                    | Coming soon |
| 7. Chain of Thought and other Intermediate Prompt Engineering Techniques                                        | Coming soon |
| 8. Retrieval Augmented Generation (RAG)                                                                         | Coming soon |
| 9. Outer-Loop Agents                                                                                            | Coming soon |

This course will assume you have some background in:

1. Basic CLI use and managing projects with git
2. Getting, writing, editing, and running python programs and dependencies
3. For chapters on Retrieval Augmented Generation (RAG, Chapters 5 and 6) you'll want a basic background on machine learning and vector embeddings. [There is an excellent free course on this here.](https://www.youtube.com/playlist?list=plzhqobowtqdnu6r1_67000dx_zcjb-3pi)
4. Interacting with REST APIs and databases (but no API or database in particular)
5. Basic familiarity with LLMs, having played with ChatGPT a bit is plenty

You do not need:

1. An academic background in AI or Machine Learning, beyond what is linked in #3 above
2. Access to GPUs for training/fine-tuning

## What You'll Learn

This course will touch on a few different topics, with the goal of giving you a general overview of what is possible. We won't go especially
deep on any one topic. You will get sense of what is possible and how to go deeper on what interests you.

You'll learn:

1. How to interact with LLMs Programatically using python
2. How to improve performance with some basic prompt engineering techniques
3. How to expose LLMs to the outside world with Tool/Function Calling
4. Techniques to build multi-agent systems to improve results and perform more complex tasks
5. Advanced prompt engineering topics like chain-of-thought
6. To use RAG to equip LLMS with contextual knowledge
7. To build outer-loop agents that work in the background (rather than in chat interfaces)

By the end of this course, you'll have built several complex LLM applications, and should feel confident to build LLM-based agents for your own or your customers' use cases. You'll be equipped to design AI-native solutions and weigh the tradeoffs between different approaches and frameworks.

## FAQ

### Why did you write this?

I found myself stumbling into a few of these topics, many of which have been around for 18+ months. There has been so much noise and hype in the AI space that it was hard to parse out what was important and useful. More concretely:

1. The core abstractions that make agents, tool calling, and other GenAI applications work are really, clean and elegant, but they end up buried in layers and layers of abstraction.
2. Frameworks that orchestrate LLM applications tend to overindex on "look at all this magic" and add a lot of complexity for simple use cases. A lot of that magic is wrapped up in some very good but very opaque prompt engineering.
3. As I found myself explaining the basics of function calling to AI skeptics, I realized that a lot of great engineers have been underserved by the AI hype machine.

**GenAI, The Good Parts** is my attempt to cut through the noise and focus on the core concepts that are foundational to building awesome LLM applications.

### Who is this for?

A bunch folks in particular, but in general I'm not exactly sure yet. But if you're like me when I started this journey, you're a software engineer and you're a little underwhelmed by ChatGPT and all the AI hype.

Maybe you've done a few examples, but found some AI libraries/frameworks to be overly complex with hard-to-grok abstractions.

Maybe you're afraid that without a masters in Machine Learning, you're not really qualified to understand what's going on.

### Why did you choose python?

Nowadays you can write agents in many languages, but python is by far the most popular. If someone wants to contribute a JS/TS version, I'd be very happy to include it.

### How long does this take to complete?

Each chapter is designed to take ~1 hour to complete, and each will include a hands-on coding assignment. Some of these will take 20 minutes, others might run several hours.

### What if I get stuck?

Please file an issue in the repo, and we'll do our best to help you out.

HumanLayer has a [Discord community](https://discord.gg/AK6bWGFY7d), which is another good way to get in touch with the maintainers.

### Can I do this on Windows?

This content is designed for MacOS or Linux and tested on MacOS. If someone wants to contribute content/instructions for Windows, we'd be happy to include it.

## License

Non-code content is licensed under the [Creative Commons Attribution-NonCommercial (CC BY-NC)](https://creativecommons.org/licenses/by-nc/4.0/). If you'd like to use the content for commercial purposes like paid courses, please contact us at contact@humanlayer.dev and let's chat.

The Code examples in this repo are licensed under the [MIT license](./LICENSE)
