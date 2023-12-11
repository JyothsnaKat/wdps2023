from ctransformers import AutoModelForCausalLM
# data/word_vectors/glove.6B.100d.zip
repository="TheBloke/Llama-2-7B-GGUF"
model_file="llama-2-7b.Q4_K_M.gguf"
llm = AutoModelForCausalLM.from_pretrained(repository, model_file=model_file, model_type="llama")

# question list
# the running time may be different, some of them are really costy and sometimes answers dont make sense
questions = [
    "The capital of the Netherlands is ...",
    "Is Amsterdam the capital of the Netherlands?"
    # "Purple is a mixture color of red and ... ",
    # "Is purple a mixture color of red and blue?",
    # "The nationality of Lana Del Rey is ...",
    # "Is Lana Del Rey a French?",
    # "The theory of relativity is proposed by ...",
    # "Is Newton born in America?",
    # "Van Gogh was born in ...",
    # "Did Van Gogh commit suicide?"
]
answers = []

print("Computing the answer (can take some time)...")
# prompt = input("Type your question (for instance: \"The capital of Italy is \") and type ENTER to finish:\n")
# print("Computing the answer (can take some time)...")
for question in questions:
    completion = llm(question)
    answers.append(completion)
    # print("compished\n")
    
for i, answer in enumerate(answers):
    print(f"Quetion {i+1}: {questions[i]}")
    print(f"Answer: {answer}\n")
