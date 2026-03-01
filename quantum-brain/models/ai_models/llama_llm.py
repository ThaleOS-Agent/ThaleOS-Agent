from langchain.llms import LlamaCpp

def load_llama_model(model_path: str = "/models/llama-3-8b.Q4_K_M.gguf"):
    llm = LlamaCpp(
        model_path=model_path,
        temperature=0.7,
        max_tokens=512,
        top_p=0.95,
        verbose=True,
    )
    return llm
