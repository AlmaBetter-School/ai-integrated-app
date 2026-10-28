"""The screen: a chat box that sends each question to the research agent."""
import os
from pathlib import Path

import gradio as gr
from dotenv import load_dotenv

from agent import research

load_dotenv(Path(__file__).with_name(".env"))  # Reads DEEPSEEK_API_KEY from .env.


def as_text(content):
    """Gradio may store a message as plain text or as a list of parts."""
    if isinstance(content, list):
        return " ".join(part.get("text", "") for part in content if isinstance(part, dict))
    return str(content)


def chat(message, history):
    turns = [{"role": turn["role"], "content": as_text(turn["content"])} for turn in history]
    return research(message, turns)


demo = gr.ChatInterface(
    fn=chat,
    title="Research Assistant",
    description="Ask a question. The agent searches Wikipedia and arXiv, "
                "then answers with sources.",
    examples=[
        "What is CRISPR?",
        "Find recent research papers on small language models",
        "Explain gravitational force and find a recent paper about it",
    ],
    run_examples_on_click=False,  # Clicking an example only fills the box.
)

if __name__ == "__main__":
    demo.launch(
        server_name=os.getenv("GRADIO_SERVER_NAME", "127.0.0.1"),
        server_port=int(os.getenv("GRADIO_SERVER_PORT", "7860")),
    )
