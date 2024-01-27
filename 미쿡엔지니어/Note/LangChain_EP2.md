1. Most common Chain

    - LLM/Chat Model
        - The language model is the core reasoning engine here. In order to work with LangChain, you need to understand the different types of language models and how to work with them.

    - Prompt Template
        - This provides instructions to the language model. This controls what the language model outputs, so understanding how to construct prompts and different prompting strategies is crucial.

    - Output Parser
        - These translate the raw response from the language model to a more workable format, making it easy to use the output downstream.

2. LLM /Chat Model

    - LLM
        - underlying model takes a string as input and returns a string

    - ChatModel
        - underlying model takes a list of messages as input and returns a message 
        - BaseMessage
            - Content
            - Role
            - Schema Objects
                - HumanMessage: coming from a human/user
                - AIMessage: coming from an AI/Assistant
                - SystemMessage: coming from the system
                - FunctionMessage / ToolMessage: the output of a function or tool call