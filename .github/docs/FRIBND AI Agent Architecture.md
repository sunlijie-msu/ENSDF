FRIBND AI Agent Architecture

**Context Engineering**
*   **Custom Instructions:** Rules, Standards, Conventions, Guidelines, Guardrails.
*   **Custom Agents:** Persona, Role, Behavior, Tools.
*   **Subagents:** Handoffs, Guided Sequential Workflows.
*   **Reusable Prompts:** Commands, Specific Tasks, Standardized Workflows.
*   **Agent Skills:** Portable and Interoperable Capabilities across Agents, Scripts, Templates, Examples, Reference Docs, Dynamic Loading Resources.
*   **Agent Hooks:** Deterministic Pre/Post-Action Commands.
*   **Agent Plugins:** To be developed.

**Semantic Structuring**
(Role Assignment & Tag Wrapping) organizes the context across four primary types: System Messages, User Messages, Assistant Messages, and Tool Messages.
This framework ensures clear communication between the user, the AI, and the tools.

*   **System Message:**
    *   Base Identity
    *   Microsoft Safety Policies
    *   Agent Base Instructions
    *   Copilot Memories (Facts learned from interactions)
    *   Custom Instructions
    *   Agent Skills
    *   Custom Agents

*   **User Message:**
    *   Environment Info and Workspace Info
    *   Conversation Summary (Overview, Technical Foundation, Codebase Status, Problem Resolution, Progress Tracking, Active Work State, Recent Operations, Continuation Plan)
    *   Reminder Instructions
    *   User Requests
    *   Editor Context (File paths, Selections, Cursor position, Terminal)
    *   Explicit References (Attachments)
    *   Reusable Prompts

*   **Assistant Message:**
    *   Text Response (Talking)
    *   Tool Calls (Acting)

*   **Tool Message:**
    *   Results of Tool Calls (e.g., Data in 80-col ENS diles)

**Structured Message Assembly Pipeline**
1.  File Discovery
2.  Parsing and Loading
3.  Tool Reference Resolution
4.  Semantic Structuring (Role Assignment & Tag Wrapping: System, User, Assistant, or Tool)
5.  Content Rendering
6.  Integration into a Raw Chat Message Array

**Endpoint Conversion**
*   **Payload Construction:** JSON Payload Built Based on the Message Array
*   **Model Configuration:** Model Selection, Tool Definitions (JSON Schema), Token Limits, Sampling Parameters (Temperature, Top_p), Streaming Options, and Thinking Budget
