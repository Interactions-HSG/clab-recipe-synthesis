(define (domain problem_-domain)
 (:requirements :strips :typing :numeric-fluents)
 (:types
    shape - object
    block tower_0 - shape
 )
 (:predicates (on ?sh_a - shape ?sh_b - shape) (handempty) (holding ?blk_hold - block) (ontable ?blk_ot - block) (clear ?sh_clear - shape))
 (:functions (size_y_of ?sh_size - shape))
 (:action pick_up
  :parameters ( ?blk - block)
  :precondition (and (ontable ?blk) (handempty) (clear ?blk))
  :effect (and (not (ontable ?blk)) (not (clear ?blk)) (holding ?blk) (not (handempty))))
 (:action put_down
  :parameters ( ?blk - block)
  :precondition (and (holding ?blk))
  :effect (and (ontable ?blk) (clear ?blk) (not (holding ?blk)) (handempty)))
 (:action attach
  :parameters ( ?blk - block ?sh_dst - shape)
  :precondition (and (holding ?blk) (clear ?sh_dst))
  :effect (and (on ?blk ?sh_dst) (not (holding ?blk)) (handempty) (clear ?blk) (not (clear ?sh_dst)) (increase (size_y_of ?sh_dst) (size_y_of ?blk))))
 (:action detach
  :parameters ( ?sh_from - shape ?blk - block)
  :precondition (and (handempty) (clear ?sh_from) (<= (size_y_of ?blk) (size_y_of ?sh_from)))
  :effect (and (not (on ?blk ?sh_from)) (holding ?blk) (not (handempty)) (not (clear ?blk)) (clear ?sh_from) (decrease (size_y_of ?sh_from) (size_y_of ?blk))))
)
