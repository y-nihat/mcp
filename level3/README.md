# Level 3 — Wrap an LLM call

Level 3 extends Level 2 by demonstrating how an MCP server can wrap calls to an external LLM (here, using LM Studio) and expose the LLM functionality as a Tool.

What this level adds

- A new tool `llm_prompt(prompt: str)` which forwards the prompt to an LM Studio model and returns the model's generated text as `{"result": <text>}`.
- The server attempts to import and call the LM Studio Python client (`from lm_studio import Client`). If LM Studio is unavailable the server returns a deterministic fallback message so the demo remains runnable.

Why wrap LLMs as tools?

- Wrapping an LLM behind a Tool centralizes model access, enforces usage patterns (prompt formatting, rate limits, logging), and simplifies client code.

Example usage

- Client calls:

```python
resp = await session.call_tool("llm_prompt", {"prompt": "Write a short greeting to CSStudent in 1 sentence."})
```

- The tool returns `{"result": "...generated text..."}` which the client prints.

LM Studio HTTP example

If you run a local LM Studio-compatible server (for example on port 1234) you can test the model
directly with curl. The server code defaults to the model `qwen/qwen3-4b-2507` and the local URL
`http://localhost:1234/v1/chat/completions`, but you can override these with environment variables
`LMSTUDIO_URL` and `LMSTUDIO_MODEL`.

Example curl (matching the demo defaults):

```bash
curl http://localhost:1234/v1/chat/completions \
 -H "Content-Type: application/json" \
 -d '{
  "model": "qwen/qwen3-4b-2507",
  "messages": [
   { "role": "system", "content": "Always answer in rhymes. Today is Thursday" },
   { "role": "user", "content": "What day is it today?" }
  ],
  "temperature": 0.7,
  "max_tokens": -1,
  "stream": false
}'
```

If the server is reachable the `llm_prompt` tool will forward the prompt and return the model's response
in `{"result": <text>}` form. If the LM Studio server is not available the tool returns an error/fallback
string in the `result` field so the demo remains runnable.

Expected output

Running from the repository root with the `mcp` env active:

```bash
conda activate mcp
# Level 3 — Wrap an LLM call

Level 3 extends Level 2 by demonstrating how an MCP server can wrap calls to an external LLM (here, using LM Studio) and expose the LLM functionality as a Tool.

What this level adds

- A new tool `llm_prompt(prompt: str)` which forwards the prompt to an LM Studio model and returns the model's generated text as `{"result": <text>}`.
- The server attempts to call a local LM Studio HTTP API (by default `http://localhost:1234/v1/chat/completions`). If LM Studio is unavailable the server returns a deterministic fallback message so the demo remains runnable.

Why wrap LLMs as tools?

- Wrapping an LLM behind a Tool centralizes model access, enforces usage patterns (prompt formatting, rate limits, logging), and simplifies client code.

Example usage

- Client calls:

```python
resp = await session.call_tool("llm_prompt", {"prompt": "Write a short greeting to CSStudent in 1 sentence."})
```

- The tool returns `{"result": "...generated text..."}` which the client prints.

LM Studio HTTP example

If you run a local LM Studio-compatible server (for example on port 1234) you can test the model directly with curl. The server code defaults to the model `qwen/qwen3-4b-2507` and the local URL `http://localhost:1234/v1/chat/completions`, but you can override these with environment variables `LMSTUDIO_URL` and `LMSTUDIO_MODEL`.

Example curl (matching the demo defaults):

```bash
curl http://localhost:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen/qwen3-4b-2507",
    "messages": [
      { "role": "system", "content": "Always answer in rhymes. Today is Thursday" },
      { "role": "user", "content": "What day is it today?" }
    ],
    "temperature": 0.7,
    "max_tokens": -1,
    "stream": false
}'
```

If the server is reachable the `llm_prompt` tool will forward the prompt and return the model's response in `{"result": <text>}` form. If the LM Studio server is not available the tool returns an error/fallback string in the `result` field so the demo remains runnable.

Expected output

Running from the repository root with the `mcp` env active:

```bash
conda activate mcp
python level3/mcp_client.py
```

Example output (if LM Studio is available and returns a greeting):

```text
Client connected.
This is a static resource from my MCP server.
Output from greet tool: Hello, CSStudent! Welcome to MCP.
Output from math add: 3 + 4 = 7.0
Output from math multiply: 6 * 7 = 42.0
Output from llm_prompt tool: Hello CSStudent — welcome to the course! (actual text depends on the model)
```

If LM Studio is not installed or reachable, the tool will return a fallback or error message in the `result` field and the client will print that message.
