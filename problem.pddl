(define (problem problem_-problem)
 (:domain problem_-domain)
 (:objects
   block_a block_b block_c - block
   tower - tower_0
 )
 (:init (= (size_y_of block_a) 1) (ontable block_a) (clear block_a) (= (size_y_of block_b) 1) (ontable block_b) (clear block_b) (= (size_y_of block_c) 1) (ontable block_c) (clear block_c) (= (size_y_of tower) 0) (clear tower) (handempty))
 (:goal (and (<= 3 (size_y_of tower))))
)
