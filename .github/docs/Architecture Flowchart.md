flowchart TD
    subgraph UserCreated["👤 USER-CREATED FILES"]
        CustomAgent[".github/agents/my-agent.agent.md"]
        Instructions[".copilot-instructions.md"]
        PromptFile["#file: prompts/review.prompt.md"]
        SkillFile["SKILL.md"]
    end

    subgraph BuiltIn["🏗️ BUILT-IN GENERATED AGENTS"]
        AskProvider["AskAgentProvider"]
        PlanProvider["PlanAgentProvider"]
        EditProvider["EditModeAgentProvider"]
    end

    %% Custom Agent Flow
    CustomAgent --> VSCodeDiscover["VS Code Discovers .github/agents/"]
    VSCodeDiscover --> ParseAgent["PromptFileParser.parse()"]
    ParseAgent --> ExtractHeader["Extract YAML Header<br/>name, tools, model, etc."]
    ParseAgent --> ExtractBody["Extract Body via body.getContent()"]
    ExtractBody --> UserSelects["User Selects Agent"]
    UserSelects --> SessionResource["sessionResource URI set"]
    SessionResource --> ModeInstr["request.modeInstructions2.content = body"]

    %% Built-in Agent Flow
    AskProvider --> BuildMarkdown["buildAgentMarkdown(config)"]
    PlanProvider --> BuildMarkdown
    EditProvider --> BuildMarkdown
    BuildMarkdown --> GenYAML["Generate YAML + Body"]
    GenYAML --> CacheWrite["Write to cache .agent.md"]
    CacheWrite --> UserSelects

    %% Instructions Flow
    Instructions --> InstrService["CustomInstructionsService.getAgentInstructions()"]
    InstrService --> ReadInstr["readFile() → content"]
    ReadInstr --> InstrTag["<attachment filePath='...'>content</attachment>"]
    InstrTag --> InstrWrapper["<instructions>...</instructions>"]

    %% Prompt File Flow
    PromptFile --> PromptParse["PromptFileParser.parse()"]
    PromptParse --> PromptYAML["Strip YAML Header"]
    PromptYAML --> PromptBodyGet["body.getContent()"]
    PromptBodyGet --> PromptTag["<attachment id='name'>body</attachment>"]

    %% Skill Flow
    SkillFile --> SkillDiscover["Skill Folder Detection"]
    SkillDiscover --> SkillRead["Read SKILL.md"]
    SkillRead --> SkillTag["<attachment>content</attachment>"]

    %% Assembly into AgentPrompt
    ModeInstr --> AgentCustomInstr["AgentPrompt.getAgentCustomInstructions()"]
    InstrWrapper --> AgentCustomInstr
    PromptTag --> UserMessage["AgentUserMessage rendering"]
    SkillTag --> AgentCustomInstr

    AgentCustomInstr --> ModePrecedence["<modeInstructions><br/>must take precedence<br/>{agent body}</modeInstructions>"]
    ModePrecedence --> SystemOrUser{"CustomInstructionsInSystemMessage?"}
    SystemOrUser -->|true| SysMsg["<SystemMessage>"]
    SystemOrUser -->|false| UserMsg["<UserMessage>"]

    %% Final Rendering
    SysMsg --> RenderPrompt["PromptRenderer.render()"]
    UserMsg --> RenderPrompt
    UserMessage --> RenderPrompt

    RenderPrompt --> CollapseSystem["Collapse Consecutive System Messages"]
    CollapseSystem --> MessageArray["Raw.ChatMessage[]"]
    MessageArray --> LLMOutput["🤖 LLM API Request"]

    style CustomAgent fill:#ff6666,stroke:#cc0000,stroke-width:3px
    style ModeInstr fill:#ff9999
    style ModePrecedence fill:#ffcccc
    style LLMOutput fill:#66ff66