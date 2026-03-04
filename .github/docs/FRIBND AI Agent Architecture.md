Top-Center Title: FRIBND AI Agent Architecture

**Context Engineering**:
Custom Instructions: Rules, Standards, Conventions, Guidelines, Guardrails
Custom Agents: Persona, Role, Behavior, Tools
Subagents: Handoffs, Guided Sequential Workflows
Reusable Prompts: Commands, Specific tasks, Standardized workflows
Agent Skills: Portable and Interoperable Capabilities across Agents, Scripts, Templates, Examples, Reference Docs, Resources

**Semantic Structuring** (Role Assignment & Tag Wrapping) organizes the Context across four primary types: system messages, user messages, assistant messages, and tool messages.
This framework ensures clear communication between the user, the AI, and the tools.

System Message:
Base identity
Microsoft safety policies
Agent base instructions
Copilot memories: facts learned from interactions
Custom instructions
Agent skills
Custom agents

User Message:
Environment info
Workspace info
Conversation summary: Conversation Overview, Technical Foundation, Codebase Status, Problem Resolution, Progress Tracking, Active Work State, Recent Operations, Continuation Plan
Reminder: User request
Editor context: edited file paths, selections, cursor position, terminal.
Chat variables: attachments
Reusable prompts

Assistant Message:
Text response (Talking)
Tool call (Acting)

Tool Message:
Result of tool calls: data in 80-col ens files


**Structured Message Assembly Pipeline**:
File Discovery,
Parsing, Loading,
Tool Reference Resolution,
Semantic Structuring (Role Assignment & Tag Wrapping: system, user, assistant, or tool),
Content Rendering,
Integration into a Raw Chat Message Array.

**Endpoint Conversion**:
Payload Construction: JSON payload built based on the message array.
Model Configuration: Model selection, Tool definitions (JSON schema), Token limits, Sampling parameters (temperature, top_p), Streaming options, and Thinking budget.