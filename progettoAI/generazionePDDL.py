from langchain_community.llms import Ollama

# Carica il modello locale LLaMA 3.1:8b
llm = Ollama(model="llama3:8b")

# Inserisci qui il testo del Lore Document (oppure caricalo da un file come stringa)
with open("C:/Users/domen/OneDrive/Desktop/The Amulet of Light – Lore Document.txt", "r", encoding="utf-8") as f:
    lore_text = f.read()

# Prompt da inviare al modello
prompt = f"""\ 
You are an expert AI Planning system and PDDL domain generator. 
Your task is to read a fantasy lore document describing a world, and **generate a complete PDDL domain and problem** that represent the scenario as a planning problem.

**Requirements and format:**
- Provide a full PDDL domain and problem definition that can be solved by a planner (e.g. Fast Downward) with no syntax errors.
- The output **must** include both:
  1. A `(define (domain ...))` section with a domain name, a `:predicates` list, and several `:action` definitions. Each action should have parameters, clear preconditions, and effects reflecting the lore.
  2. A `(define (problem ...))` section with the same domain name, a list of `:objects` present in the lore, an `:init` state using the predicates to describe the initial world state, and a `:goal` condition that is achievable via the actions.
- Use consistent naming: all names (domain, predicates, actions, objects) in lowercase and using underscores `_` instead of spaces. Use descriptive names related to the fantasy lore (e.g., `has_sword`, `open_portal`, `slay_dragon`) and avoid generic names.
- **Ensure the domain name is identical in both the domain and problem definitions.**
- The `:init` facts should be consistent with the lore description, and the `:goal` should be a logical outcome or quest from the lore that can be achieved with the available actions.
- **Do not explain or write anything outside the PDDL code.** Only output the valid PDDL code for the domain and problem, with no additional commentary.

Now, using the following fantasy lore document, generate the PDDL domain and problem:

\"\"\" 
{lore_text}
"""

# Chiedi al modello di generare il PDDL
print("Generating PDDL from Lore...\n")
response = llm.invoke(prompt)

# Salva il risultato in un file .pddl
with open("quest_problem.pddl1", "w", encoding="utf-8") as f:
    f.write(response)

print("PDDL generated and saved to quest_problem.pddl")
