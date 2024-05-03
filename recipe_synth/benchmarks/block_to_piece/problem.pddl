(define (problem blocktopiecewithinventory-problem)
 (:domain blocktopiecewithinventory-domain)
 (:objects
   blockvar_1 blockvar_2 - blockvartype
   blockinv_1 blockinv_2 - blockinvtype
   piece - piecetype
 )
 (:init (= (dim_x blockvar_1) 1) (= (dim_y blockvar_1) 1) (= (block_inv blockvar_1) 2) (= (dim_x blockvar_2) 1) (= (dim_y blockvar_2) 2) (= (block_inv blockvar_2) 1) (= (dim_x piece) 0) (= (dim_y piece) 0))
 (:goal (and (= (dim_x piece) 2) (= (dim_y piece) 2)))
)
