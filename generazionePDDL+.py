import subprocess
from langchain.agents import initialize_agent, Tool
from langchain_community.llms import Ollama
from langchain_core.tools import tool
import os

# Carica il modello LLaMA 3 tramite Ollama
llm = Ollama(model="llama3:8b")

# Percorso in cui salvare i PDDL generati
OUTPUT_DIR = "./pddl_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@tool
def generate_pddl_from_lore(file_path: str) -> dict:
    """Legge un file contenente il lore e genera il PDDL (domain + problem)"""
    with open(file_path, "r", encoding="utf-8") as f:
        lore = f.read()

    prompt = f"""
    You are an expert AI Planning system and PDDL domain generator. 
    Your task is to read a fantasy lore document describing a world, and **generate a complete PDDL domain and problem** that represent the scenario as a planning problem.

    **Requirements and format:**
    - Provide a full PDDL domain and problem definition that can be solved by a planner (e.g. Fast Downward) with no syntax errors.
    - The output **must** include both:
    1. A `(define (domain ...))` section with a domain name, a `:predicates` list, and several `:action` definitions.
    2. A `(define (problem ...))` section with the same domain name, a list of `:objects`, an `:init` state, and a `:goal`.
    - Use consistent naming in lowercase with underscores.
    - Output only valid PDDL. No explanations.

    An exemple of domain.pddl and problem.pddl
    ============ DOMAIN PDDL =====================
    (define (domain enemy-puzzle-adventure)
  (:requirements :strips :typing :negative-preconditions)

  (:types
    agent enemy location item puzzle)

  (:predicates
    (at ?a - agent ?l - location)
    (connected ?l1 - location ?l2 - location)      ; grafo statico
    (door_open ?p - puzzle)                        ; indica se la "porta" è aperta
    (door_blocks ?p - puzzle ?l1 - location ?l2 - location) ; la porta impedisce il passaggio
    (item_at ?obj - item ?l - location)
    (has ?a - agent ?obj - item)
    (enemy_at ?e - enemy ?l - location)
    (enemy_defeated ?e - enemy)
    (puzzle_at ?p - puzzle ?l - location)
    (puzzle_solved ?p - puzzle)
    (opens ?obj - item ?p - puzzle))

  ;; ----------------- AZIONI -----------------

  (:action move
    :parameters (?a - agent ?from - location ?to - location ?p - puzzle)
    :precondition (and
                    (at ?a ?from)
                    (connected ?from ?to)
                    (not (door_blocks ?p ?from ?to))    ; non esiste porta che blocca
                  )
    :effect (and
              (not (at ?a ?from))
              (at ?a ?to)))

  (:action pickup
    :parameters (?a - agent ?obj - item ?l - location)
    :precondition (and
                    (at ?a ?l)
                    (item_at ?obj ?l)
                    (forall (?e - enemy) (not (enemy_at ?e ?l))))
    :effect (and
              (has ?a ?obj)
              (not (item_at ?obj ?l))))

  (:action fight
    :parameters (?a - agent ?e - enemy ?l - location)
    :precondition (and
                    (at ?a ?l)
                    (enemy_at ?e ?l))
    :effect (and
              (enemy_defeated ?e)
              (not (enemy_at ?e ?l))))

  (:action solve_puzzle
    :parameters (?a - agent ?p - puzzle ?l - location ?key - item ?to1 - location ?to2 - location)
    :precondition (and
                    (at ?a ?l)
                    (puzzle_at ?p ?l)
                    (not (puzzle_solved ?p))
                    (has ?a ?key)
                    (opens ?key ?p)
                    (door_blocks ?p ?to1 ?to2))         ; la porta effettivamente blocca il passaggio
    :effect (and
              (puzzle_solved ?p)
              (door_open ?p)
              (not (door_blocks ?p ?to1 ?to2))))
)
======================= END DOMNAIN PDDL EXEMPLE ==============

======================= PROBLEM PDDL =======================
(define (problem enemy-puzzle-problem)
  (:domain enemy-puzzle-adventure)

  (:objects
    agent1 - agent
    locA locB locC locD - location
    enemy1 - enemy
    key1 - item
    puzzle1 - puzzle)

  (:init
    (at agent1 locA)

    ; grafo statico
    (connected locA locB) (connected locB locA)
    (connected locB locC) (connected locC locB)
    (connected locC locD) (connected locD locC)

    ; la porta (puzzle1) chiude il passaggio tra locC e locD
    (puzzle_at puzzle1 locC)
    (door_blocks puzzle1 locC locD)

    ; nemico e chiave in locB
    (enemy_at enemy1 locB)
    (item_at key1 locB)
    (opens key1 puzzle1))

  (:goal (and
           (at agent1 locD)
           (enemy_defeated enemy1)
           (puzzle_solved puzzle1)))
)
======================== END PROBLEM ========================

    LORE:
    """
    {lore}
    """
    """
    print("\n Generazione PDDL...")
    response = llm.invoke(prompt)
    if "(define (problem" not in response:
        raise ValueError("Output LLM non contiene un problem valido")
    domain, problem = response.split("(define (problem", 1)
    domain = domain.strip()
    problem = "(define (problem " + problem.strip()

    # Salva nei file
    domain_path = os.path.join(OUTPUT_DIR, "domain.pddl")
    problem_path = os.path.join(OUTPUT_DIR, "problem.pddl")
    with open(domain_path, "w", encoding="utf-8") as f:
        f.write(domain)
    with open(problem_path, "w", encoding="utf-8") as f:
        f.write(problem)

    print(f"\n File salvati in: {OUTPUT_DIR}")
    return {
        "domain": domain,
        "problem": problem
    }
