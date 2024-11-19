########################
### testing chunk ####
def index_dict(key_list, value_list):
    """
    Makes a dictionary out of the suff and Df-indices
    """
    idx_dict = {}
    for i in range(len(key_list)):
        idx_dict[key_list[i]] = value_list[i] 
    return idx_dict

def sub_range(total_range, largest_range):
    """
    function to subtract the largest range of a child node 
    from the total leaf range of the current node
    Returns 2 tuples if the largest group is bordering the dge of the total interval
    1 of them is (None, None)
    """
    total_start, total_end = total_range
    largest_start, largest_end = largest_range

    ### Observation: 3 cases for the largest groups placement in the interval:
    # largest start at total start
    if total_start == largest_start:
        small_start, small_end = largest_end+1, total_end
        return (None), (small_start, small_end)

    # largest end at total end
    elif total_end == largest_end:
        small_start, small_end = total_start, largest_start-1
        return (small_start, small_end), (None)

    # largest inbetween total start and end - seperates the small_v into 2 intervals
    else:
        remaining_range_1 = (total_start, largest_start-1) 
        remaining_range_2 = (largest_end+1, total_end)
        return remaining_range_1, remaining_range_2


def checks_in_leaflists(BTR_list, S, depth, leaf_list, large_v, small_v, suff_idx_dict, df_idx_dict):
    """
    Do the checks from 2b and 2c for i and j in the leaflists  
    """
    # 2b - checks for i
    for i in range(small_v[0], small_v[1]+1):
        i_suf = df_idx_dict[i]        
        j_suf = i_suf + depth
        j = suff_idx_dict[j_suf]

        if j >= leaf_list[0] and j <= leaf_list[1]:
            if S[i_suf] != S[i_suf + 2*depth]:
                BTR_list.append((i_suf, depth))
    
    # 2c - checks for j
        j_suf = i_suf - depth
        if j_suf < 0:   # if j_suf is less than 0 it is no longer in the s_list and we skip
            continue
        j = suff_idx_dict[j_suf]
        if j >= large_v[0] and j <= large_v[1]:
            BTR_list.append((j_suf, depth))



def repeat_search_speedup(self):
    """
    Faster version of repeat_search. Finds the largest leaflist of children, and avoids using
    i as leaves in this Large(v). additionally does checks for j and not just i.
    Returns a list of (i_suf, depth) which starts a BTR

    Doctest examples:
        >>> repeat_searcg(SuffixTree("abaabaabbba"))
        [(2, 1), (5, 1), (2, 3), (8, 1)]
    """
    S = self.string
    s_list, df_list = self.df_numbering_non_recursive()

    suff_idx_dict = index_dict(s_list, df_list)
    df_idx_dict = index_dict(df_list, s_list)

    BTR_list = []

    def dfs(node, current_path):
        if not node.children: #base: no children so leaf
            return
        
        largest_child = (None, 0) # (node_id, size) , keeps track of largest child
        
        #recursively visit all nodes
        for child in node.children.values():
            edge_label = self.string[child.start:child.end]             # gather the edge label, so we keep track of current path/depth
            dfs(child, current_path + edge_label)
            
            child_size = child.leaf_range[1]-child.leaf_range[0] + 1    # +1 since we want all leaves inside the node and not just difference
            if child_size > largest_child[1]:
                largest_child = (child, child_size)
        
        # 2a - get leaflist (from the node numbering function)
        leaf_list = (node.leaf_range)
        depth = len(current_path) # uses current path to find depth of current node

        if depth != 0: # 0 would be at root
            #determine small(v) and large(v)
            large_v = largest_child[0].leaf_range # define large(v)
            small_v = sub_range(leaf_list, large_v) # define small(v)

            if small_v[0] == None:      # large is in first part of total range
                checks_in_leaflists(BTR_list, S, depth, leaf_list, large_v, small_v[1], suff_idx_dict, df_idx_dict)
            elif small_v[1] == None:    # large is in later part of total range
                checks_in_leaflists(BTR_list, S, depth, leaf_list, large_v, small_v[0], suff_idx_dict, df_idx_dict)
            else:                       # large is in the middel of total range
                checks_in_leaflists(BTR_list, S, depth, leaf_list, large_v, small_v[0], suff_idx_dict, df_idx_dict)
                checks_in_leaflists(BTR_list, S, depth, leaf_list, large_v, small_v[1], suff_idx_dict, df_idx_dict)

    dfs(self.root, "") # initialize recursion
    return BTR_list