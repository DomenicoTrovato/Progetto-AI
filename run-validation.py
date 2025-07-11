import subprocess
import difflib
from langchain_community.llms import Ollama
import os
import subprocess
import difflib
from langchain.agents import initialize_agent, Tool
from langchain_core.tools import tool

llm = Ollama(model="llama3:8b")

def run_planner(domain_path, problem_path):
    print(f"\n  Esecuzione Fast Downward con i file: {domain_path}, {problem_path}")
    result = subprocess.run(
        ["fast-downward.py", domain_path, problem_path, "--search", "astar(blind)"],
        capture_output=True, text=True
    )
    output = result.stdout
    if "Solution found!" in output:
        return True, output
    return False, output



llm = Ollama(model="llama3:8b")

@tool
def run_planner_tool(_: str) -> str:
    """Valida i file domain.pddl e problem.pddl con Fast Downward"""
    print("\n  Esecuzione Fast Downward...")
    result = subprocess.run(
        ["fast-downward.py", "domain.pddl", "problem.pddl", "--search", "astar(blind)"],
        capture_output=True, text=True
    )
    if "Solution found!" in result.stdout:
        return "success"
    return result.stdout[:1500]

@tool
def reflect_on_failure(_: str) -> str:
    """Esegue riflessione automatica con LLM e aggiorna i file PDDL"""
    print("\n Riflessone e correzione...")
    with open("domain.pddl", "r", encoding="utf-8") as f:
        domain = f.read()
    with open("problem.pddl", "r", encoding="utf-8") as f:
        problem = f.read()

    planner_output = run_planner_tool.invoke("")

    if planner_output == "success":
        return "Piano valido, nessuna riflessione necessaria."

    prompt = f"""
You are an expert PDDL repair agent. The planner failed to solve the PDDL model.
Analyze and fix any logical or structural issues in the domain/problem below.
Output only corrected PDDL, without explanations.

PLANNER OUTPUT:
{planner_output}

DOMAIN:
{domain}

PROBLEM:
{problem}
"""
    response = llm.invoke(prompt)
    if "(define (problem" not in response:
        raise ValueError("Output LLM non valido nel reflection")
    domain_new, problem_new = response.split("(define (problem", 1)
    domain_new = domain_new.strip()
    problem_new = "(define (problem " + problem_new.strip()

    print("\n Differenze rilevate nel domain.pddl:")
    for line in difflib.unified_diff(domain.splitlines(), domain_new.splitlines(), fromfile='old', tofile='new', lineterm=''):
        print(line)
    print("\n Differenze rilevate nel problem.pddl:")
    for line in difflib.unified_diff(problem.splitlines(), problem_new.splitlines(), fromfile='old', tofile='new', lineterm=''):
        print(line)

    with open("domain.pddl", "w", encoding="utf-8") as f:
        f.write(domain_new)
    with open("problem.pddl", "w", encoding="utf-8") as f:
        f.write(problem_new)

    return "PDDL aggiornato con riflessione"

# Inizializza agente ReAct
tools = [run_planner_tool, reflect_on_failure]
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent_type="zero-shot-react-description",
    verbose=True
)

print("\n Avvio processo iterativo con ReAct Agent...")

max_iterations = 5
for i in range(max_iterations):
    result = agent.run("Esegui validazione e, se necessario, correggi il PDDL fino a che Fast Downward non trova un piano valido.")
    if "Piano valido" in result or "success" in result:
        print("\n✅ Piano trovato! Processo completato.")
        break
else:
    print("\n Dopo 5 iterazioni non è stato trovato un piano valido.")