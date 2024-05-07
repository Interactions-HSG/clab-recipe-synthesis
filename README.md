# Recipe Synth

## Approach

In this demonstrator the desired piece is represented by a grid of 16 cells. To occupy a cell, the planner is given two different block variants `BlockVar1` and `BlockVar2`. Each block variant has its owen inventory. The cells can be occupied by the primitive action `attach`. The result of the action, i.e. the number and layout of the cells that are occupied, depends on the block variant.

_Hint:_ Note that besides the description of a block variant, no other conditions are given to the planner. For instance, inserting a block multiple times at already occupied cells is possible, according to the model description.

The implementation uses [unified-planning](https://unified-planning.readthedocs.io/en/latest/#), an [EU founded project](https://www.ai4europe.eu/research/ai-catalog/unified-planning-framework) to reduce the entry level into the planning domain 

## Evaluation

The result can be visualized using the `plan_goal_simulator`:

|symbol|meaning|
|-------|-------|
|xn | x coordinate with value n of a cell|
|yn | y coordinate with value n of a cell|
|bm | block of type m|
|#bm| block inventory of type m|

```text
enhsp returned:
SequentialPlan:
    attach(BlockVar_2, px_0_2)
    attach(BlockVar_1, px_2_0)
    attach(BlockVar_1, px_0_0)


                        action  --  --  --  -- #b1 #b2
0                initial state  x0  x1  x2  x3   2   1
1                           y0                        
2                           y1                        
3                           y2                        
4                           y3                        
5                                                     
6                                                     
7   attach(BlockVar_2, px_0_2)  x0  x1  x2  x3   2   0
8                           y0                        
9                           y1                        
10                          y2  b2  b2  b2  b2        
11                          y3  b2  b2  b2  b2        
12                                                    
13  attach(BlockVar_1, px_2_0)  x0  x1  x2  x3   1   0
14                          y0          b1  b1        
15                          y1          b1  b1        
16                          y2  b2  b2  b2  b2        
17                          y3  b2  b2  b2  b2        
18                                                    
19  attach(BlockVar_1, px_0_0)  x0  x1  x2  x3   0   0
20                          y0  b1  b1  b1  b1        
21                          y1  b1  b1  b1  b1        
22                          y2  b2  b2  b2  b2        
23                          y3  b2  b2  b2  b2        
```

The output shows that the planner found a plan. Inventory was respected. This minimalistic demonstration on how the recipe synthesis can be modeled as planning problem. 

- Benefits
  - Less effort than implementing a custom solver
  - Level of abstraction allows for reusability
- Downsides:
  - AI planning in general
    - only simple math
    - limiting language
      - no complex functions
      - only int and bool types
        - using in reduces the number of available planners since not all of them support numerical fluents
    - not yet understood if action effects are applied in the order they are defined
      - relevant e.g. in the rotation action to buffer the state of variable
  - Discretization using cells
    - Concerns that state-space becomes to larger to handle when number of cells is increased

## Summary

On a very basic level, this demonstrator allows to understand how the problem of synthesizing recipes can be formulated as planning problem using a cell based approach. It allows further experiments e.g. observing the processing time when increasing the number of cells with different conditions.

Folding action primitives have not been investigated but seem to be the most crucial operation both in terms of increasing shape versatility as well as mathematically. Hence it makes sense that the representation follows the needs of enabling this primitive.
