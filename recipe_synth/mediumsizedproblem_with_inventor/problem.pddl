(define (problem counterwithinventory-problem)
 (:domain counterwithinventory-domain)
 (:objects
   c0 c1 c2 - countertype
   inc - incrementaltype
   stock0 stock1 stock2 - stocktype
 )
 (:init (= (inc_value inc) 1) (= (stock_2_inc stock0) 0) (= (c_value c0) 0) (= (c_value c1) 0) (= (c_value c2) 0))
 (:goal (and (<= 18 (+ (c_value c2) (+ (c_value c1) (c_value c0))))))
)
