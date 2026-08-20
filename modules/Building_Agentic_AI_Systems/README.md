# Building with Agentic AI

**Goal**: learn best practices for building Agentic AI applications that will open up many more opportunities, whether job opportunities or the chance to build amazing software yourself.

**What you will Learn**:

- How to build agentic workflows made of swappable, debuggable, and composable modules.
- How to evaluate the performance of AI workflows in terms of latency, cost, and accuracy.
- How to optimize modules and workflows using training data; rather than manual prompt engineering.
- How to utilize the results of tried and tested methods as evident by research on Agentic AI including: _Reasoning_, _Reflection_, _Planning_, and _CodeAct_.

## Introductions

1. [Agentic AI: Workflows, and Language Models](lessons/01_agentic_ai.qmd) (~46m)
2. [Six Agentic AI Patterns from Research Papers](lessons/02_agentic_patterns.qmd) (~18m)

## M1. Signatures and Modules

1. [Introduction to the DSPy Framework](lessons/03_dspy_overview.qmd) (~25m)
2. [Setup](lessons/05_dspy_setup.ipynb) (~16m)
3. [First Program](lessons/06_dspy_first_program.ipynb) (~22m)
4. [Class-based Signature](lessons/07_dspy_class-based_signature.ipynb) (~20m)
5. [Changing Modules](lessons/08_dspy_changing_modules.ipynb) (~12m)
   - [Exercise: Email Extraction](exercises/email_extraction.ipynb) (~37m)

Recommended: [Set up MLflow Tracing to understand what's happening under the hood](lessons/mlflow.md) (~7m).

## M2. Agents, Tools, and Code

1. [ReAct Loop](lessons/09_dspy_ReAct.ipynb) (~27m)
   - [Exercise: Flights Agent](exercises/flights_agent.ipynb) (~26m)
2. [Composing Modules](lessons/10_dspy_composing_modules.ipynb) (~27m)
3. [CodeAct Loop](lessons/11_dspy_CodeAct.ipynb) (~37m)
   - [Exercise: Flights Coding Agent (and Keep Conversation History)](exercises/flights_code_agent.ipynb) (~35m) ([solution](exercises/flights_code_agent_solution.ipynb) (~37m))

If you are looking for MCP, see: [Tutorial: Use MCP tools in DSPy](https://dspy.ai/tutorials/mcp/)

## M3. Optimization

1. [Evaluation and Optimization](lessons/12_dspy_evaluation_and_optimization.ipynb) (~59m)
2. Inference-time Output Refinement:
   - [Tutorial: Output Refinement: BestOfN and Refine](https://dspy.ai/tutorials/output_refinement/best-of-n-and-refine/).
   - and [Tutorial: Image Generation Prompt iteration](https://dspy.ai/tutorials/image_generation_prompting/)

## M4. Deployment

- [Tutorial: Deploying your DSPy program](https://dspy.ai/tutorials/deployment/)
- and [Tutorial: Memory-Enabled ReAct Agents with Mem0](https://dspy.ai/tutorials/mem0_react_agent/)

## M5. Retrieval Augmented Generation (RAG)

1. [What is RAG?](lessons/13_rag.qmd) (~25m)
2. [ChromaDB: Ingestion and Querying](lessons/14_chromadb.ipynb) (~42m)
   - [Exercise: Explore the Embedding Space](exercises/14/visualize_embeddings.ipynb) (~31m) ([solution](exercises/14/visualize_embeddings_solution.ipynb) (~31m))
   - [Optional: Multi-modal Embeddings](https://docs.trychroma.com/docs/embeddings/multimodal)
3. [Chunking: Searching PDF Documents](lessons/15_chunking.ipynb) (~49m)
4. [RAG with DSPy](lessons/16_dspy_rag.ipynb) (~53m)

## Projects

1. [From Lectures to an Interactive Book](projects/01_lectures_to_interactive_book.md)
2. [Book Translation](projects/02_translation_pipeline.md)
3. [Comparative Analysis](projects/03_comparative_analysis.md)
4. [Writer Assistant](projects/04_writer_assistant.md)
5. [Code Annotation](projects/05_code_annotation.md)
6. [Step-by-step](projects/06_step_by_step.md)
7. [DataMaster Agent](projects/07_data_master_agent.md)
8. [Hadeeth](projects/08_hadeeth.md)
9. [oTranscribe](projects/09_oTranscribe.md)

## References

- [Agentic AI Course](https://www.deeplearning.ai/courses/agentic-ai) (Andrew Ng, DeepLearningAI)
- [DSPy](https://dspy.ai/): Program, don’t prompt, your LLMs.
- [AI Engineer Roadmap](https://www.aihero.dev/ai-engineer-roadmap)