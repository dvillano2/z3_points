# z3_points
<p align="center">
  <img src="animation/animation.gif" width="500">
</p>
Confusingly titled mixed inteter linear programming model designed to find optimially equidistributed subsets. This project started at the recurse center in fall 2025 when someone told me about z3 and all its capabilities. I decided I would try to use it to find interesting subsets, as ML net-based project with which I was trying to attack the problem (you can find it on this github) was plateauing before become quite interesting enough. The confused and garbled remenants of that attempt can be seen in the "solve.py" file

Evenutally, figured out how to make all conditions linear by introducting a more variables and, since the optimization was now completely linear with 0-1 variables, I switched to OR tools. The image above is a collection of optimially equidistrubted subsets of the three dimensional vector space over the integers mod five. (Theree is a break a symmetry where I require them to all contain (0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)). They are all equidistributed on ten families of parallel planes. After imposing a couple geometric conditions described below, theses are optimial, in the sense that there are no subsets satisfying the conditions that are equidistubuted in elevel directions.
