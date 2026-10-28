"""Checks that need no API key and make no real web requests."""
import json
from unittest.mock import MagicMock

import httpx
import pytest

import agent
import app
import tools

WIKI_JSON = {"query": {"pages": {
    "2": {"index": 2, "title": "Second", "extract": "Two.", "fullurl": "https://w/2"},
    "1": {"index": 1, "title": "CRISPR", "extract": "A gene editing tool. " * 50,
          "fullurl": "https://en.wikipedia.org/wiki/CRISPR"},
}}}
ARXIV_XML = """<feed xmlns="http://www.w3.org/2005/Atom"><entry>
  <id>http://arxiv.org/abs/2501.00001v1</id><published>2025-01-02T00:00:00Z</published>
  <title>Small  Models
  Matter</title><summary>We study small models.</summary>
  <author><name>Ada Lovelace</name></author><author><name>Alan Turing</name></author>
</entry></feed>"""


def http_response(status=200, **kwargs):
    return httpx.Response(status, request=httpx.Request("GET", "https://test"), **kwargs)


def tool_call(name, query, call_id="call_1"):
    return {"role": "assistant", "content": "", "tool_calls": [{
        "id": call_id, "type": "function",
        "function": {"name": name, "arguments": json.dumps({"query": query})}}]}


def final(text):
    return {"role": "assistant", "content": text}


def model_replies(*messages):
    """Fake DeepSeek: return these assistant messages in order."""
    return [http_response(json={"choices": [{"message": m}]}) for m in messages]


@pytest.fixture(autouse=True)
def services(monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", " test-key ")
    get = MagicMock(return_value=http_response(json=WIKI_JSON))
    post = MagicMock()
    monkeypatch.setattr(tools.httpx, "get", get)
    monkeypatch.setattr(agent.httpx, "post", post)
    return get, post


def test_search_wikipedia_returns_best_match_first(services):
    results = tools.search_wikipedia("CRISPR")
    assert [r["title"] for r in results] == ["CRISPR", "Second"]
    assert results[0]["url"] == "https://en.wikipedia.org/wiki/CRISPR"
    assert len(results[0]["summary"]) <= 601
    assert "User-Agent" in services[0].call_args.kwargs["headers"]


def test_search_arxiv_reads_the_xml(services):
    services[0].return_value = http_response(text=ARXIV_XML)
    [paper] = tools.search_arxiv("small models")
    assert paper == {"title": "Small Models Matter", "authors": ["Ada Lovelace", "Alan Turing"],
                     "published": "2025-01-02", "summary": "We study small models.",
                     "url": "http://arxiv.org/abs/2501.00001v1"}


def test_run_tool_handles_problems(services):
    assert "no tool called" in tools.run_tool("search_google", {"query": "x"})
    services[0].side_effect = httpx.ConnectError("offline")
    assert tools.run_tool("search_wikipedia", {"query": "x"}).startswith("Error")


def test_agent_uses_a_tool_then_answers(services):
    get, post = services
    post.side_effect = model_replies(tool_call("search_wikipedia", "CRISPR"),
                                     final("CRISPR edits genes.\n\nSources: https://en.wikipedia.org/wiki/CRISPR"))
    answer = agent.research("What is CRISPR?")
    assert answer.startswith('🔎 search_wikipedia("CRISPR")')
    assert "CRISPR edits genes." in answer
    assert post.call_count == 2
    request = post.call_args.kwargs
    assert request["headers"]["Authorization"] == "Bearer test-key"
    assert request["json"]["tools"] == tools.TOOLS
    # The second model call includes the tool result for the model to read.
    [tool_message] = [m for m in request["json"]["messages"] if m["role"] == "tool"]
    assert tool_message["tool_call_id"] == "call_1" and "CRISPR" in tool_message["content"]


def test_agent_can_answer_without_tools(services):
    services[1].side_effect = model_replies(final("Hello!"))
    assert agent.research("Hi") == "🧠 Answered without searching\n\nHello!"


def test_agent_stops_after_max_steps(services):
    services[1].side_effect = model_replies(
        *[tool_call("search_arxiv", "loop") for _ in range(agent.MAX_STEPS)])
    assert "couldn't finish" in agent.research("Loop forever")
    assert services[1].call_count == agent.MAX_STEPS


def test_missing_and_rejected_keys(services, monkeypatch):
    services[1].return_value = http_response(401, json={})
    assert "could not accept the key" in agent.research("Hi")
    monkeypatch.setenv("DEEPSEEK_API_KEY", "")
    assert "Add DEEPSEEK_API_KEY" in agent.research("Hi")


def test_screen_sends_plain_text_history(monkeypatch):
    seen = {}
    monkeypatch.setattr(app, "research", lambda message, history: seen.update(h=history) or "ok")
    history = [{"role": "user", "content": [{"type": "text", "text": "What is CRISPR?"}]},
               {"role": "assistant", "content": "A gene tool.", "metadata": {}}]
    assert app.chat("Explain more simply", history) == "ok"
    assert seen["h"] == [{"role": "user", "content": "What is CRISPR?"},
                         {"role": "assistant", "content": "A gene tool."}]
