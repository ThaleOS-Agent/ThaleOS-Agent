from langchain.llms import GPT4All

def load_gpt4all_model(model_path: str = "~/.gpt4all/gpt4all-13b-snoozy.ggmlv3.q4_0.bin"):
    llm = GPT4All(model=model_path, backend="llama", verbose=True)
    return llm
