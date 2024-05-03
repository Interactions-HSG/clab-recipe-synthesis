(define (domain blocktopiecewithinventory-domain)
 (:requirements :strips :typing :equality :numeric-fluents :conditional-effects)
 (:types
    shapetype blockinvtype - object
    blockvartype piecetype - shapetype
 )
 (:functions (dim_x ?dimx - shapetype) (dim_y ?dimy - shapetype) (block_inv ?blk - blockvartype))
 (:action attach_x
  :parameters ( ?blk - blockvartype ?p - piecetype)
  :precondition (and (<= 1 (block_inv ?blk)))
  :effect (and (increase (dim_x ?p) (dim_x ?blk)) (when (= 0 (dim_y ?p)) (increase (dim_y ?p) (dim_y ?blk))) (decrease (block_inv ?blk) 1)))
 (:action attach_y
  :parameters ( ?blk - blockvartype ?p - piecetype)
  :precondition (and (<= 1 (block_inv ?blk)))
  :effect (and (increase (dim_x ?p) (dim_x ?blk)) (when (= 0 (dim_x ?p)) (increase (dim_x ?p) (dim_x ?blk))) (decrease (block_inv ?blk) 1)))
)
