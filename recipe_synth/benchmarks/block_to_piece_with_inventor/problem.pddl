(define (problem counterwithinventory-problem)
 (:domain counterwithinventory-domain)
 (:objects
   piece_dim0 piece_dim1 piece_dim2 - piecetype
   fabric_block_dim0 fabric_block_dim1 fabric_block_dim2 - blocktype
 )
 (:init (= (block_size fabric_block_dim0) 0) (= (type2id fabric_block_dim0) 0) (= (type2id piece_dim0) 0) (= (block_size fabric_block_dim1) 1) (= (type2id fabric_block_dim1) 1) (= (type2id piece_dim1) 1) (= (block_size fabric_block_dim2) 2) (= (type2id fabric_block_dim2) 2) (= (type2id piece_dim2) 2) (= (block_dim fabric_block_dim0) 5) (= (block_dim fabric_block_dim1) 4) (= (block_dim fabric_block_dim2) 3) (= (piece_dim piece_dim0) 0) (= (piece_dim piece_dim1) 0) (= (piece_dim piece_dim2) 0))
 (:goal (and (<= 10 (+ (piece_dim piece_dim2) (+ (piece_dim piece_dim1) (piece_dim piece_dim0))))))
)
