Structured message assembly pipeline in VS Code GitHub Copilot Chat:
File Discovery, Tool Reference Resolution, Parsing, Loading, Semantic Structuring (Tag Wrapping, Role Assignment (system, user, assistant, or tool)), Content Rendering, 
Integration into an array of Raw.ChatMessage objects.
Endpoint Conversion: Payload Construction: JSON payload to LLM API includes the message array, Configuration: model selection, tool definitions (JSON schema), token limits, and sampling parameters (temperature, top_p), streaming options, and thinking budget parameter.

Built-in Agents (Ask, Edit, Plan, Agent): defined programmatically in TypeScript as configuration objects,.
Custom Agents: defined in .agent.md files located in .github/agents/ (either locally in the User workspace or remotely fetched from GitHub).

VS Code Chat converts the TypeScript configuration object into a string with YAML frontmatter and Markdown body (Generation & Caching), then applies Markdown Registration.

Then VS Code Core handles the Parsing and Execution of all agent.md

Prompt Injection: The content is injected into the system message (wrapped in <Tag name='modeInstructions'>). It takes precedence over default instructions.
