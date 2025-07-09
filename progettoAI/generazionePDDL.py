from langchain_community.llms import Ollama

# Carica il modello locale LLaMA 3.1:8b
llm = Ollama(model="llama3:8b")

# Inserisci qui il testo del Lore Document (oppure caricalo da un file come stringa)
with open("C:/Users/domen/OneDrive/Desktop/The Amulet of Light – Lore Document.txt", "r", encoding="utf-8") as f:
    lore_text = f.read()

# Prompt da inviare al modello
prompt = f"""
This is a fantasy planning problem.

Below is a Lore Document. Please generate a fully working and syntactically valid PDDL domain and problem definition, suitable for a classical planner like Fast Downward.

You must include:
1. Full :domain definition (with :predicates and :action sections)
2. A separate :problem block with :init and :goal
3. All actions must include :precondition and :effect using correct PDDL syntax
4. Use lowercase and underscores in names
5. The plan must be solvable (at least one valid path to the goal)

Lore:
{lore_text}
"""


# Chiedi al modello di generare il PDDL
print("Generating PDDL from Lore...\n")
response = llm.invoke(prompt)

# Salva il risultato in un file .pddl
with open("quest_problem.pddl1", "w", encoding="utf-8") as f:
    f.write(response)

print("PDDL generated and saved to quest_problem.pddl")
