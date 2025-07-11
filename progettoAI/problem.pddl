(define (problem amulet-of-light-problem)
  (:domain amulet-of-light)

  (:objects
    hero - agent
    oakstead village oakstead-village - location
    dark-forest - location
    ridge-path - location
    malakar-tower - location
    amulet - artifact
    old-man - item
    trusted-sword - item
    worn-shield - item
    provisions - item)

  (:init
    (at hero oakstead-village)
    (connected oakstead-village dark-forest) (connected dark-forest ridge-path)
    (connected ridge-path malakar-tower)
    (puzzle_at amulet oakstead-village)
    (door_blocks amulet oakstead-village malakar-tower)
    (item_at old-man oakstead-village)
    (has hero trusted-sword) (has hero worn-shield) (has hero provisions)

  (:goal (and
           (at hero malakar-tower)
           (enemy_defeated ?e - enemy) ; assume there's one necromancer to defeat
           (puzzle_solved amulet)))
)
======================== END PROBLEM ========================