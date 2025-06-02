# Multi-Tool Agent with AutoGen

This project implements a multi-tool agent using AutoGen that can select from multiple tools, log its reasoning flow, and make decisions based on user queries.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      Multi-Tool Agent System                     │
│                                                                  │
│  ┌──────────────┐        ┌───────────────┐      ┌────────────┐  │
│  │              │        │               │      │            │  │
│  │  User Input  │───────▶│  AssistantAgent  │◀────▶│  OpenAI LLM │  │
│  │              │        │               │      │            │  │
│  └──────────────┘        └───────┬───────┘      └────────────┘  │
│                                  │                               │
│                                  ▼                               │
│                          ┌───────────────┐                       │
│                          │  Tool Manager │                       │
│                          └───────┬───────┘                       │
│                                  │                               │
│                                  ▼                               │
│  ┌──────────────┐    ┌───────────────────────┐    ┌───────────┐ │
│  │              │    │                       │    │           │ │
│  │ Weather Tool │◀───┤  Tool Selection Logic ├───▶│ Calc Tool │ │
│  │              │    │                       │    │           │ │
│  └──────────────┘    └───────────┬───────────┘    └───────────┘ │
│                                  │                               │
│                                  ▼                               │
│                          ┌───────────────┐                       │
│                          │ Currency Tool │                       │
│                          └───────────────┘                       │
│                                                                  │
│  ┌──────────────┐        ┌───────────────┐                       │
│  │              │        │               │                       │
│  │ Logging System│◀──────┤ Execution History │                   │
│  │              │        │               │                       │
│  └──────────────┘        └───────────────┘                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## How It Works

1. **User Input**: The user provides a query or request.
2. **AssistantAgent**: The AutoGen AssistantAgent processes the input and determines which tool to use.
3. **Tool Manager**: Manages the available tools and handles tool selection logic.
4. **Tool Execution**: The selected tool is executed with the appropriate parameters.
5. **Reasoning Flow**: The agent explains its reasoning before and after using a tool.
6. **Logging System**: All tool usage and reasoning is logged for transparency and analysis.

## Components

### 1. Tool Manager

The `ToolManager` class is responsible for:
- Registering available tools
- Executing tools based on agent decisions
- Logging tool usage and reasoning
- Maintaining execution history
- Providing usage statistics

### 2. Tools

The system includes multiple tools:
- **Weather Tool**: Gets current weather information for a city
- **Calculator Tool**: Evaluates mathematical expressions
- **Currency Tool**: Converts between different currencies

### 3. Agent

The `AssistantAgent` from AutoGen:
- Uses GPT-4o to understand user requests
- Selects the appropriate tool based on the request
- Explains its reasoning process
- Provides results with context

### 4. Logging System

The logging system captures:
- Tool selection reasoning
- Tool execution details
- Execution time
- Results or errors
- Usage statistics

## State Management

The agent maintains state through:
1. **Execution History**: A chronological record of all tool executions
2. **Usage Statistics**: Counts of how often each tool is used
3. **Reasoning Logs**: Detailed logs of the decision-making process

## Decision Making Process

1. **Analysis**: The agent analyzes the user request
2. **Tool Selection**: Based on the analysis, it selects the most appropriate tool
3. **Reasoning**: It explains why it selected that particular tool
4. **Execution**: It executes the tool with the necessary parameters
5. **Interpretation**: It interprets the results for the user

## Usage

To use the multi-tool agent:

1. Set up your environment variables in `.env`:
   ```
   OPENAI_API_KEY=your_openai_api_key
   OPENWEATHER_API_KEY=your_openweather_api_key
   EXCHANGE_RATE_API_KEY=your_exchange_rate_api_key
   ```

2. Run the agent:
   ```
   python main.py
   ```

3. Enter your query when prompted.

## Example Queries

- "What's the weather like in London?"
- "Calculate the value of sin(30) + cos(45)"
- "Convert 100 USD to EUR"
- "Should I wear a jacket in New York today?"
