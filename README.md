# 490-Final
Final project for COSC 490: Special Topics: Artificial Intelligence

CONCEPT:
  We wanted to create a simplified, zero-player game in the vein of Sid Meyer's Civilization Series, Dwarf Fortress, etc.
  We imagined a matrix which represents the game world, implemented as a list of Tile Class objects. Each tile would have one of the following
descriptors: "ground", "water", "occupied", a set resource value, and a set resource_growth rate.
  Occupying this map are Cluster objects which have a populationg value, resource consumption rate, color, and neural network.
  Utilizing its own neural network, each Cluster would make a decision: either consume resources to grow its population, or spit its population
and occupy an additional tile, adding more resources to its available resource pool.
  Further, we declare the 'fittest' Cluster of one generation, and create 'children' which have similar but varied values, which would be 
used in the next generation, and the process repeated.
  We have no 'goals' for this experiement per se; we are interested in any behavior that may happen emerge - at least, so long as our machines
are able to keep up.

POSSIBLE FUTURE GOALS:
  Initially we hoped to allow greater agency to the Clusters: hostility values to initiate "war" between one another, and "scouting parties" which
seperated completely from the initial cluster in search for more bountiful lands, and anything else that might have come to us. Perhaps someday.
