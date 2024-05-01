(define (problem problem_-problem)
 (:domain problem_-domain)
 (:objects
   c0 c1 c2 - counter
   inc - incremental
 )
 (:init (= (inc_value inc) 1) (= (value c0) 0) (= (value c1) 0) (= (value c2) 0))
 (:goal (and (<= 18 (+ (value c0) (+ (value c2) (value c1))))))
)
