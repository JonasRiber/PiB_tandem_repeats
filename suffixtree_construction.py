from graphviz import Digraph

class Node(object):
    def __init__(self, start=None, end=None, suffix_number=None, parent=None):
        self.start = start                      # start idx for string
        self.end = end                          # end idx for string 
        self.suffix_number = suffix_number      # order the $ are add to tree
        self.children = {}                      # children as dictionary, key = a unique charater, value = Npde(object)
        self.parent = parent                    # Defining a parent node allows us to go back up in the tree
        #self.suffixlink =   # <---- for mccreicht  
    
class SuffixTree:
    def __init__(self, string):
        self.string = string + "$"
        self.root = Node()
        self.build_tree(string)
    
    
    def build_tree(self, string):
        string = string + "$"
        n = len(string)
        
        for i in range(n):
            current_node = self.root
            suffix = string[i:]
            self.insert_suffix(current_node, suffix, i, i)
    
    def insert_suffix(self, current_node, suffix, suffix_start, suffix_index):
        first_char = suffix[0]

        ### outgoing edge - check if suffix has an edge it can follow
        #case 1: No children matching suffix - so we add one
        if first_char not in current_node.children:
            current_node.children[first_char] = Node(suffix_start, len(self.string), suffix_index, current_node)       
        
        #case2: We have an outgoing edge!
        elif first_char in current_node.children:
            edge_node = current_node.children[first_char] # move down to the node we found
            common_len = self.find_common_prefix_length(suffix, edge_node)
            #case2.1: if we moved all the way out of the edge
            if common_len == edge_node.end - edge_node.start:
                self.insert_suffix(edge_node, suffix[common_len:], suffix_start+common_len, suffix_index)
            #case2.2: split in edge found, insert internal node 
            else:
                self.split_edge(current_node, edge_node, common_len, suffix, suffix_start, suffix_index)


    def find_common_prefix_length(self, suffix, edge):
        """
        Find the length of a common prefix between two strings
        """
        common_len = 0
        edge_start = edge.start
        edge_end = edge.end
        
        # while we dont exceed the suffix length
        while common_len < len(suffix) and edge_start + common_len < edge_end:
            if suffix[common_len] == self.string[edge_start + common_len]:        # if the letters in suffix and string is the same -> contentiue
                common_len += 1
            else:
                break   # end when no longer the same, this is our breaking index where we split
        return common_len

    def split_edge(self, parent_node, edge, common_length, suffix, suffix_start, suffix_index):
        """
        we found a missmatch and insert a new node inbetween existing childnode and parent
        This new internal node becomes new child of the current parent node and parent to current child node
        Then we add the remainder of the current suffix as a new child node (now sibling to old childnode)
        """
        #create the new internal node - will be the parent of the split edge and the new leaf
        internal_node = Node(start=edge.start, end=edge.start + common_length, parent=parent_node) # it idx ends at the common lenght from where it starts
        parent_node.children[self.string[edge.start]] = internal_node

        # update the existing edge's start
        edge.start += common_length # leaf node now starts at the new split
        edge.parent = internal_node
        internal_node.children[self.string[edge.start]] = edge
        
        # create new leaf node with rest of current suffix
        remaining_suffix_start = suffix_start + common_length
        internal_node.children[suffix[common_length]] = Node(start=remaining_suffix_start, end=len(self.string), suffix_number=suffix_index, parent=internal_node)

####################################
### Visualization using graphviz ###
    def visualize(self, filename="Suffix_tree_compressed"):
        dot = Digraph(node_attr={'shape': 'ellipse', 'fontsize': '12', 'fixedsize': 'false'},
                      edge_attr={'fontsize': '15', 'fontcolor': 'red', 'labelfontsize': '10', 
                                 'labeldistance': '1', 'labelangle': '0'})
        self.add_edges(dot, self.root, node_id="root")
        dot.render(filename, format='png', cleanup=True)    # saves an image of the tree in root folder
        print(f"Visualization saved as {filename}.png")
        return dot

    def add_edges(self, dot, node, node_id):
        #add each child and its corresponding edge label
        for i, (char, child) in enumerate(node.children.items()):
            child_id = f"{node_id}_{i}"  # unique id for each child node

            # check if df_numbering has been added
            if hasattr(child, 'df_number'):
            # check if the child is a leaf
                if not child.children:  #Leaf node (no children)
                    leaf_label = f"S:{child.suffix_number}, df:{child.df_number}"
                    dot.node(child_id, leaf_label, style="filled", color="lightgrey")
                else:
                    dot.node(child_id, "", style="filled", color="lightgrey")  # Internal nodes remain unlabeled
            else:
                if not child.children:  #Leaf node (no children)
                    leaf_label = f"S:{child.suffix_number}"
                    dot.node(child_id, leaf_label, style="filled", color="lightgrey")
                else:
                    dot.node(child_id, "", style="filled", color="lightgrey")  # Internal nodes remain unlabeled
            
            #edge label
            #label = self.string[child.start:child.end]     # write the string labels
            #label = f"({child.start}, {child.end})"         # write the idx on labels
            label = self.string[child.start:child.end] + f" ({child.start}, {child.end})" 
            dot.edge(node_id, child_id, label=label)

            # Recursively add edges for the child
            self.add_edges(dot, child, child_id)  
   
############################
### validation functions ###

    def find_longest_branch(self):
        """
        using dfs to find longest branch in the suffix tree
        Returns both the longest str and the corosponding length
        """
        def dfs(node, current_path):
            if not node.children:
                return current_path
            
            longest_branch = current_path
            for child in node.children.values():
                edge_label = self.string[child.start:child.end]
                branch = dfs(child, current_path + edge_label) # recursively move out a branch
                if len(branch) > len(longest_branch): # check if lonest we've seen
                    longest_branch = branch
            return longest_branch
        
        # recursion start
        return dfs(self.root, "")

    def get_all_suffixes(self):
        """
        using dfs we look through the tree to find all the suffixes
        returns a list of all suffixes found throughout the constructed tree
        """
        suffixes = []
        def dfs(node, current_path):
            if not node.children:
                return suffixes.append(current_path) # leaf node, so we add suffix

            for child in node.children.values(): # look at
                edge_label = self.string[child.start:child.end]
                dfs(child, current_path + edge_label) # recussively search tree

        dfs(self.root, "") # initiate search
        return suffixes
   
    def count_outgoing_edges(self):
        """
        Count the number of outgoing edges for internal nodes. internal nodes can minimum have 2 
        children, and at max have the same as number of unique symbols in the stirng.
        Returns nodes that fail these criteria
        """
        # define criteria
        min_children = 2
        max_children = len(set(self.string))    # length of unique char in the string        
        failed_nodes = []                       # keep track of failed nodes

        # depth first search
        def dfs(node):
            if not node.children: # no children, so its a leaf
                return 

            for child in node.children.values():
                dfs(child) # recursively move out branch

            # check if number of children is correct
            num_children = len(node.children)
            if num_children < min_children or num_children > max_children:
                failed_nodes.append(node)

            return
        
        dfs(self.root)
        return failed_nodes

    def check_unique_children(self):
        """
        check that each internal node has unique values in the dictionary for children
        Returns a list of failed nodes, if empty all passed.
        """
        failed_nodes = []

        def dfs(node):
            if not node.children: # no children, so its a leaf
                return 
            
            for child in node.children.values():
                dfs(child) # recursively move out branch

            # check if all children are unique
            all_children = list(node.children.values())
            unique_children = set(all_children)
            unique_check = len(all_children) == len(unique_children)
            if unique_check == False:
                failed_nodes.append(node)

        dfs(self.root)
        return failed_nodes
    
    def node_visits(self):
        """
        Find number of times we visist a given node with a depth-first approach. 
        We should only visit each node once.
        Returns...
        """
        visit_counts = {}
        failed_nodes = []

        def dfs(node):
            #recursively visit all children
            for child in node.children.values():
                dfs(child)

            if node in visit_counts:
                visit_counts[node] += 1
            else:
                visit_counts[node] = 1

            if visit_counts[node] > 1:
                failed_nodes.append(node)            
            
        dfs(self.root) # initialize recursion
        return failed_nodes
    

#################################
### helper functions ###
    def df_numbering(self):
        '''
        Does a depth-first search through the tree and adds the ordering to the leaves
        df_number is added to the node objects and two lists of corosponding suffix- and df-numbering
        is returned. Additionally also adds a leaflist of the depth-first numbers to each internal node.
        '''
        count = [0] #mutable counter
        df_list = []
        suffix_list = []

        def dfs(node):
            if not node.children: #base case: no children, so its a leaf
                node.df_number = count[0]
                node.leaf_range = (count[0], count[0]) # [count[0]]
                count[0] += 1
                df_list.append(node.df_number)
                suffix_list.append(node.suffix_number)
                return node.leaf_range

            # visit all children
            min_df = float("inf") #leaf_list = []
            max_df = -float("inf") 

            for child in node.children.values():
                # leaf_list.extend(dfs(child)) # recursively move out branch
                child_leaf_range = dfs(child)
                min_df = min(min_df, child_leaf_range[0])
                max_df = max(min_df, child_leaf_range[1])

            node.leaf_range = (min_df, max_df) # node.leaf_list = leaf_list

            return node.leaf_range # leaf_list
        
        dfs(self.root)
        return suffix_list, df_list
    

    def df_numbering_non_recursive(self):
        """
        The recursive version above gave some issues during testing, so a iterative version using a stack was made instead
        """
        count = 0
        df_list = []
        s_list = []
        
        stack = [(self.root, None, None)]  # #stack to store (current node, parent min_df, parent max_df)
        visited_children = {}  # Map each node to the index of the next child to visit
        
        while stack: #ends when stack is empty
            node, min_df, max_df = stack.pop()
            
            if not node.children:  # leafndoe
                node.df_number = count
                node.leaf_range = (count, count)
                df_list.append(node.df_number)
                s_list.append(node.suffix_number)
                count += 1
                continue
            
            # Initialize visited children tracking for each internal node on first visit
            if node not in visited_children:
                visited_children[node] = 0
                min_df, max_df = float("inf"), -float("inf")
            
            # Process the next child of the current node
            children = list(node.children.values())
            if visited_children[node] < len(children):
                child = children[visited_children[node]]
                visited_children[node] += 1
                # Push the node back to stack to revisit after its child is processed
                stack.append((node, min_df, max_df))
                # Push child to stack for further processing
                stack.append((child, None, None))
            else:
                #update min and max depthfirst numbers for internal nodes after visiting all children
                for child in children:
                    min_df = min(min_df, child.leaf_range[0])
                    max_df = max(max_df, child.leaf_range[1])
                node.leaf_range = (min_df, max_df)
        
        return s_list, df_list

    def tree_depth(self):
        """
        Function to get the greatest depth in the tree. loops through a stack to do so.
        """
        if not self.root:
            return 0
        stack = [(self.root, 0)]    #stack to store (node, depth)
        max_depth = 0

        while stack: #ends if stack is empty
            node, depth = stack.pop()
            if not node.children: # node is leaf, if greater than max -> update max
                max_depth = max(max_depth, depth)
            else:
                # node has child, add children to stack and add +1 to depth
                for child in node.children.values():
                    stack.append((child, depth + 1))

        return max_depth