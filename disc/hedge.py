# Problem Description

# The task is to create a visual representation of a directory structure
# from a list of paths.
# The directory structure should be printed in a tree format,
# where each node represents a directory or a sub-directory,
# and leaf nodes represent the deepest directories in the given paths.

# Part 1: Print directory tree
# In the first part, the goal is to implement a function that takes
# a list of paths and prints a directory tree. Each directory
# should be connected with its subdirectories using the following tokens to
# visually represent the tree structure.

SPACE_TOKEN = "    "
BRANCH_SPACE_TOKEN = "│   "
CHILD_TOKEN = "├───"
LEAF_TOKEN = "└───"

EXAMPLE_PATHS = [
    "Documents/Spring/Math",
    "Documents/Spring/Science",
    "Documents/Summer/Math",
    "Documents/Summer/Math/2012",
    "Downloads/Spring/Math",
    "Downloads/Spring/Science",
    "Downloads/Summer/Math",
]

'''
Documents/Spring/Math

s[0] = Documents, Spring, Math
s[1] = Documents, Spring, Science


                root
                /    \
            docu      down
          /     \      /   \
    spring    summer spr   sum
    /  \        /     / \    \ 
  Ma   scie   Math  mat  sci  Math
              /
            12 
  

'''
# TODO: implement me!
def print_directory_tree(paths):
    pass

class TrieNode:
    def __init__(self):
        self.childs: Dict[str, TrieNode] = {}
class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, path: list):
        tmp = self.root
        for p in path:
            if p not in tmp.childs:
                tmp.childs[p] = TrieNode()
            tmp = tmp.childs[p]


    def _dfs(self, node: TrieNode):
        if len(node.childs) == 0:
            return
        sz = len((node.childs).items())
        for dir, n in (node.childs).items():
            if(self.root != node):
                if(dir == node.childs[sz-1]):
                    print(LEAF_TOKEN, node)
                print(CHILD_TOKEN, node)    
            self._dfs(node[dir])
            
    

t = Trie()
for path in EXAMPLE_PATHS:
    p = list(path.split('/'))  #"Documents/Spring/Math"
    t.insert(p)



# Example
#
# print_directory_tree(EXAMPLE_PATHS):
#
# ├───Documents
# │   ├───Spring
# │   │   ├───Math
# │   │   └───Science
# │   └───Summer
# │       └───Math
# │           └───2012
# └───Downloads
#     ├───Spring
#     │   ├───Math
#     │   └───Science
#     └───Summer
#         └───Math

## Part 2: Enhanced Directory Tree with Closure and Item Count
# In the second part, enhance the directory tree representation by:
# 1. Creating a "directory" object
# 2. Implementing a method to "close" a directory, which means not showing its subdirectories
# but instead showing the count of immediate subdirectories or files directly under it.
#
# Example
#
# directory = create_directory(EXAMPLE_PATHS)
# directory.close('Documents/Spring')
# directory.print()
#
# ├───Documents
# │   ├───Spring (2)
# │   └───Summer
# │       └───Math
# │           └───2012
# └───Downloads
#     ├───Spring
#     │   ├───Math
#     │   └───Science
#     └───Summer
#         └───Math
