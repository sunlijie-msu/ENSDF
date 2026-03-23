# Tokenization Analysis

In AI and natural language processing, a token can represent different fundamental units, depending on the model architecture. The three standard definitions are listed below.

- **Characters:** Fundamental string units (letters, numbers, symbols, and spaces).
- **Words:** Whitespace-separated alphanumeric blocks.
- **Sub-words (BPE):** Byte-Pair Encoding units used by modern LLMs (for example, GPT-4 `cl100k_base` tokenizer). For JSON and specialized data formats (such as ENSDF), tokenizers split strings heavily due to brackets, indentation, and non-standard spacing.

| File | Format | Est. Characters | Est. Words | Est. Sub-word Tokens (BPE) |
| :--- | :--- | :--- | :--- | :--- |
| 31S Adopted | JSON | ~320,000 | ~45,000 | ~85,000-95,000 |
| 31S Adopted | FORTRAN | ~28,000 | ~4,000 | ~8,000-10,000 |

## Conclusion

The JSON file is approximately 10-12 times larger than the FORTRAN file due to the highly verbose schema, repetitive keys (for example, `"uncertainty"`, `"evaluatorInput"`), and deep nesting architectures.

- **Cost vs. performance trade-off:** Processing 100,000 tokens per query is computationally expensive and slower.
- **Context window overflow:** The JSON format is approximately 10x larger than the FORTRAN format. While the 31S dataset (~95,000 tokens) fits within the context windows of advanced models (for example, GPT-4-Turbo and Claude 3.5), heavier isotopes with dense decay schemes will exceed standard 128k token limits.

## Comparative Analysis for AI Processing

| Feature | JSON Format | FORTRAN Format |
| :--- | :--- | :--- |
| **Parsing reliability** | **High.** Explicit key-value pairs (for example, `"spinParity": "3/2+"`) eliminate ambiguity. | **Low.** LLM tokenizers routinely mangle fixed-width spaces, leading to misaligned column data. |
| **Hierarchical logic** | **Explicit.** Parent-child relationships (for example, levels containing gammas) are strictly nested. | **Implicit.** Relies on continuation characters (for example, `2cG`, `3cG`), which AI models frequently misinterpret. |
| **Function calling** | **Native.** Directly compatible with AI tools, structured JSON outputs, and automated validation schemas. | **Poor.** Requires custom Python parsing scripts before the AI can reliably query the data. |
| **Token efficiency** | **Low.** Highly verbose; requires significantly larger context windows. | **High.** Compact representation saves token costs and processing time. |

## Quality Assurance and Technical Limitations

- **Tokenizer variance:** Sub-word token counts vary significantly across model tokenizers (for example, LLaMA's `SentencePiece` versus OpenAI's `tiktoken`). Data formats with heavy spacing, symbols, and numerics (such as JSON and FORTRAN) typically yield a lower character-to-token ratio (roughly 3.5 chars/token) than standard English prose (roughly 4 chars/token).

While the old ENSDF FORTRAN format is highly compact, its reliance on strict columnar spacing and implicit relational logic makes it prone to AI parsing errors. JSON provides an explicit, self-describing architecture that aligns with how modern large language models (LLMs) process and extract structured data.

