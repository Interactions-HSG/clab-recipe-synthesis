(define (domain counterwithinventory-domain)
 (:requirements :strips :typing :equality :numeric-fluents)
 (:types
    idabletype - object
    piecetype blocktype - idabletype
 )
 (:functions (piece_dim ?p - piecetype) (block_dim ?b - blocktype) (block_size ?sid - blocktype) (type2id ?id - idabletype))
 (:action increment
  :parameters ( ?c - piecetype ?blk - blocktype)
  :precondition (and (<= 1 (block_dim ?blk)) (<= (piece_dim ?c) 10) (= (type2id ?c) (type2id ?blk)))
  :effect (and (increase (piece_dim ?c) (block_size ?blk)) (decrease (block_dim ?blk) 1)))
 (:action decrement
  :parameters ( ?c - piecetype ?blk - blocktype)
  :precondition (and (<= (block_dim ?blk) 6) (< 0 (piece_dim ?c)))
  :effect (and (decrease (piece_dim ?c) (block_size ?blk)) (increase (block_dim ?blk) 1)))
)
