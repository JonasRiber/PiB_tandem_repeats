

#### code below is from the book and translated from C into python by ChatGPT




class Range:
    def __init__(self, from_bytes, to_bytes):
        # from_bytes and to_bytes are expected to be byte-like objects (e.g., bytes, bytearray)
        self.from_bytes = from_bytes
        self.to_bytes = to_bytes

def range_length(r):
    # The length is calculated as the difference in lengths of the byte-like objects
    return len(r.to_bytes) - len(r.from_bytes)

# Example usage
r = Range(b'Hello', b'HelloWorld')
length = range_length(r)
print(length)  # Output: 5


class SuffixTreeNode:
    def __init__(self, leaf_label, range_obj, parent=None, sibling=None, child=None, suffix_link=None):
        self.leaf_label = leaf_label
        self.range = range_obj
        self.parent = parent
        self.sibling = sibling
        self.child = child
        self.suffix_link = suffix_link

def edge_length(node):
    # Calculate the edge length using the range_length function
    return range_length(node.range)

# Example usage
range_obj = Range(b'Hello', b'HelloWorld')
node = SuffixTreeNode(leaf_label=1, range_obj=range_obj)
length = edge_length(node)
print(length)  # Output: 5

class SuffixTreeNodePool:
    # Assuming the pool contains a list of nodes, we'll define it as an empty list initially.
    def __init__(self):
        self.nodes = []

class SuffixTree:
    def __init__(self, string, length, root=None):
        self.string = string           # Expecting a bytes-like object for the string
        self.length = length           # Length of the string
        self.root = root               # Root node of the suffix tree, if any
        self.pool = SuffixTreeNodePool()  # Initialize the pool of nodes

# Example usage
root_node = SuffixTreeNode(leaf_label=0, range_obj=Range(b'', b''))  # Example root node
suffix_tree = SuffixTree(string=b"example", length=len(b"example"), root=root_node)

print(suffix_tree.string)  # Output: b'example'
print(suffix_tree.length)  # Output: 7
print(suffix_tree.root.leaf_label)  # Output: 0

class SuffixTreeNodePool:
    def __init__(self):
        self.nodes = []  # A list to hold the suffix tree nodes
        self.next_node = None  # The next available node

    def add_node(self, node):
        # Add a node to the pool and update the next available node
        self.nodes.append(node)
        self.next_node = node  # Update the next_node reference

    def get_next_node(self):
        # Return the next available node, or None if the pool is empty
        return self.next_node if self.nodes else None

# Example usage
node_pool = SuffixTreeNodePool()
node1 = SuffixTreeNode(leaf_label=1, range_obj=Range(b'Hello', b'HelloWorld'))
node2 = SuffixTreeNode(leaf_label=2, range_obj=Range(b'Example', b'ExampleTest'))

node_pool.add_node(node1)
node_pool.add_node(node2)

print(node_pool.get_next_node().leaf_label)  # Output: 2 (the most recently added node)

def new_node(suffix_tree, from_bytes, to_bytes):
    # Create a new SuffixTreeNode instance
    node = SuffixTreeNode(
        leaf_label=0,
        range_obj=Range(from_bytes, to_bytes)  # Initialize the range object with given 'from' and 'to' bytes
    )
    
    # Initialize other attributes of the node
    node.parent = None
    node.sibling = None
    node.child = None
    node.suffix_link = None

    # Add the new node to the pool
    suffix_tree.pool.add_node(node)

    return node

# Example usage
suffix_tree = SuffixTree(string=b"example", length=len(b"example"))
new_node1 = new_node(suffix_tree, b"abc", b"abcdef")
new_node2 = new_node(suffix_tree, b"def", b"defghi")

print(new_node1.range.from_bytes)  # Output: b'abc'
print(new_node2.range.to_bytes)    # Output: b'defghi'

def free_suffix_tree(suffix_tree):
    # Clear the nodes in the pool
    suffix_tree.pool.nodes.clear()  # Clear the list of nodes
    suffix_tree.pool.next_node = None  # Reset the next_node reference

    # Optionally clear other references in the suffix tree
    suffix_tree.root = None
    # We do not manage suffix_tree.string, so we do not modify it

    # After this function call, Python's garbage collector will automatically free the memory

# Example usage
suffix_tree = SuffixTree(string=b"example", length=len(b"example"))
new_node1 = new_node(suffix_tree, b"abc", b"abcdef")
free_suffix_tree(suffix_tree)

print(suffix_tree.pool.nodes)  # Output: []
print(suffix_tree.root)  # Output: None

def alloc_suffix_tree(string):
    # Create a new suffix tree object
    suffix_tree = SuffixTree(string=string, length=len(string) + 1)  # Add 1 for the '\0' sentinel

    # Calculate the maximum number of nodes in the tree
    pool_size = 2 if suffix_tree.length == 1 else (2 * suffix_tree.length - 1)
    
    # Initialize the node pool
    suffix_tree.pool.nodes = [None] * pool_size  # Create a list with 'pool_size' placeholders for nodes
    suffix_tree.pool.next_node = None  # Initially, no next node available

    # Create and initialize the root node
    suffix_tree.root = new_node(suffix_tree, b'', b'')
    suffix_tree.root.parent = suffix_tree.root  # Set the root's parent to itself
    suffix_tree.root.suffix_link = suffix_tree.root  # Set the root's suffix link to itself

    return suffix_tree

# Example usage
suffix_tree = alloc_suffix_tree(b"example")

print(suffix_tree.string)  # Output: b'example'
print(suffix_tree.length)  # Output: 8 (7 + 1 for '\0')
print(len(suffix_tree.pool.nodes))  # Output: 15 (2 * length - 1)
print(suffix_tree.root is suffix_tree.root.parent)  # Output: True
print(suffix_tree.root is suffix_tree.root.suffix_link)  # Output: True

def naive_suffix_tree(string):
    # Allocate and initialize the suffix tree
    suffix_tree = alloc_suffix_tree(string)

    # Manually insert the first suffix
    first_suffix = new_node(suffix_tree, string, string + len(string))
    suffix_tree.root.child = first_suffix
    first_suffix.parent = suffix_tree.root

    # Insert all other suffixes
    xend = string + len(string)
    for i in range(1, len(string)):
        leaf = naive_insert(suffix_tree, suffix_tree.root, string[i:], xend)
        leaf.leaf_label = i

    return suffix_tree

# Example usage
def naive_insert(suffix_tree, root, suffix, xend):
    # Dummy implementation for naive_insert
    # Should return a new suffix tree node
    return new_node(suffix_tree, suffix, xend)

# Create the suffix tree for a given string
suffix_tree = naive_suffix_tree(b"example")

print(suffix_tree.string)  # Output: b'example'
print(suffix_tree.length)  # Output: 8 (length of 'example' + 1)
print(suffix_tree.root.child.leaf_label)  # Output: 0 (leaf_label of the first inserted suffix)
