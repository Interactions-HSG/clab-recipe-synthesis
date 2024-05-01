(define (domain counterwithinventory-domain)
 (:requirements :strips :typing :numeric-fluents)
 (:types
    idabletype incrementaltype - object
    countertype stocktype - idabletype
 )
 (:functions (c_value ?m - countertype) (inc_value ?ic - incrementaltype) (stock_2_inc ?sid - stocktype))
 (:action increment
  :parameters ( ?c - countertype ?ic - incrementaltype ?blk - stocktype)
  :precondition (and (<= (c_value ?c) 10))
  :effect (and (increase (c_value ?c) (inc_value ?ic))))
 (:action decrement
  :parameters ( ?c - countertype ?ic - incrementaltype ?blk - stocktype)
  :precondition (and (< 0 (c_value ?c)))
  :effect (and (decrease (c_value ?c) (inc_value ?ic))))
)
