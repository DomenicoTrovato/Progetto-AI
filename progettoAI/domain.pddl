Here are the generated PDDL domain and problem:

======================= DOMAIN PDDL ======================
(define (domain amulet-of-light)
  (:requirements :strips :typing :negative-preconditions)

  (:types
    agent location item artifact puzzle)

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

  (:action use_key
    :parameters (?a - agent ?key - item ?l - location)
    :precondition (and
                    (at ?a ?l)
                    (has ?a ?key)
                    (puzzle_at ?p ?l))
    :effect (and
              (not (has ?a ?key))
              (puzzle_solved ?p)))

  (:action defeat_necromancer
    :parameters (?a - agent ?e - enemy ?l - location)
    :precondition (and
                    (at ?a ?l)
                    (enemy_at ?e ?l)
                    (puzzle_solved ?p))
    :effect (and
              (not (enemy_at ?e ?l))
              (enemy_defeated ?e)))

  (:action reach_tower
    :parameters (?a - agent ?l - location)
    :precondition (at ?a ?l)
    :effect (at ?a ?l))

)

======================= PROBLEM PDDL =======================