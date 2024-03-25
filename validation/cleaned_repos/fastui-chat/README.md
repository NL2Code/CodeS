# fastui-chat

A minimalistic ChatBot Interface in pure python. </br>
Build on top of [FastUI](https://github.com/pydantic/FastUI) and [LangChain Core](https://github.com/langchain-ai/langchain).

## Usage

```bash
pip install fastui-chat
```

```python
from langchain.chat_models import ChatOpenAI
from langchain.memory import ChatMessageHistory

from fastui_chat import ChatUI, basic_chat_handler

history = ChatMessageHistory()
handler = basic_chat_handler(
    llm=ChatOpenAI(),
    chat_history=history,
)

history.add_ai_message("How can I help you today?")

app = ChatUI(
    chat_history=history,
    chat_handler=handler,
)

app.start_with_uvicorn()
```

## Features

- Easy to use
- Minimalistic & Lightweight
- LangChain Compatible
- Python Only