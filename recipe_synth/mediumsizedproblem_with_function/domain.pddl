(define (domain problem_-domain)
 (:requirements :strips :typing :numeric-fluents)
 (:types counter incremental)
 (:functions (value ?m - counter) (inc_value ?ic - incremental))
 (:action increment
  :parameters ( ?c - counter ?ic - incremental)
  :precondition (and (<= (value ?c) 5))
  :effect (and (increase (value ?c) (inc_value ?ic))))
 (:action decrement
  :parameters ( ?c - counter ?ic - incremental)
  :precondition (and (< 0 (value ?c)))
  :effect (and (decrease (value ?c) (inc_value ?ic))))
)
