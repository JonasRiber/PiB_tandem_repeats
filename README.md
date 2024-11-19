# PiB_tandem_repeats
### By Jonas Riber Jørgensen

This is a project focussed on algorithms for recogizing repeating patterns in strings to find tandem repeats.


Jupyter notebooks:

  - suffix_tree_construction.ipynb
  (majority of the project)
  Contains the different version of suffix tree construction algorithmens along with 2 versions of the Stoye n Gusfield repeat search through a suffix tree. Along with experimentation and testing of these functions

  - mccreight_tree_construction.ipynb
  McCreight implementation of the suffixtree construction (faster version). followed by experimentation.

Additional scripts:

  - brute_force_tandem_repeats.py
  Finds all repeats within a string and how many times they repeat
  does so iteratively

  - find_all_repeats.py
  Finds all tandem repeats within a given string. Does not find how many times a given tandem repeats repeats.
  Does this iteratively. 

  - suffixtree_construction.py
  .py script version of the naive suffix tree construction from the suffix_tree_construction.ipynb notebook

  - repeat_search_speedup.py - Stoyeand Gusfield algorithm
  .py script version of the repeats search algorithm from the suffix_tree_construction.ipynb notebook


