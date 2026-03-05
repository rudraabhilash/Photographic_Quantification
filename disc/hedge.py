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

#solution gpt- 
from typing import Dict


class TrieNode:
    def __init__(self) -> None:
        self.children: Dict[str, "TrieNode"] = {}
        self.is_end: bool = False


class WordTrie:
    def __init__(self) -> None:
        self.root = TrieNode()

    def insert(self, phrase: str) -> None:
        node = self.root
        words = phrase.split()

        for word in words:
            node = node.children.setdefault(word, TrieNode())

        node.is_end = True

    def print_tree(self) -> None:
        print("root")
        self._print_recursive(self.root, prefix="")

    def _print_recursive(
        self,
        node: TrieNode,
        prefix: str,
    ) -> None:

        children = list(node.children.items())
        total = len(children)

        for index, (word, child) in enumerate(children):
            is_last = index == total - 1

            connector = "└── " if is_last else "├── "
            print(prefix + connector + word)

            extension = "    " if is_last else "│   "
            self._print_recursive(child, prefix + extension)
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



#=================================================================================================================================================
#=================================================================================================================================================
# second round
### Business Context
- **Performance Requirement**: APIs currently take ~10 seconds without caching, optimizing this API is out of scope.
- **Scale**: 
  - ~1000 open positions per day
  - 150 companies across 2 funds
  - ~15 concurrent users
  - Position data refreshed end of day daily

### Portfolio Data Structure
Each row contains: `date, fund, ticker, company, broker, pnl`

### Sample Portfolio Data (20 companies subset)

| date       | fund      | ticker | company           | broker        | pnl      |
|------------|-----------|--------|-------------------|---------------|----------|
| 2025-02-14 | Fund_A    | AAPL   | Apple Inc         | Goldman       | 15420.50 |
| 2025-02-14 | Fund_A    | MSFT   | Microsoft Corp    | Goldman       | 22100.75 |
| 2025-02-14 | Fund_A    | GOOGL  | Alphabet Inc      | Morgan Stanley| 8900.25  |
| 2025-02-14 | Fund_A    | AMZN   | Amazon.com Inc    | Goldman       | -3200.00 |
| 2025-02-14 | Fund_A    | TSLA   | Tesla Inc         | JP Morgan     | 12500.00 |
| 2025-02-14 | Fund_A    | NVDA   | NVIDIA Corp       | Goldman       | 31000.50 |
| 2025-02-14 | Fund_A    | META   | Meta Platforms    | Morgan Stanley| 9800.00  |
| 2025-02-14 | Fund_A    | NFLX   | Netflix Inc       | JP Morgan     | -1500.25 |
| 2025-02-14 | Fund_A    | AMD    | AMD Inc           | Goldman       | 7200.00  |
| 2025-02-14 | Fund_A    | INTC   | Intel Corp        | Morgan Stanley| -2100.50 |
| 2025-02-14 | Fund_B    | AAPL   | Apple Inc         | Goldman       | 8900.00  |
| 2025-02-14 | Fund_B    | JPM    | JPMorgan Chase    | JP Morgan     | 15600.75 |
| 2025-02-14 | Fund_B    | BAC    | Bank of America   | Morgan Stanley| 11200.00 |
| 2025-02-14 | Fund_B    | WFC    | Wells Fargo       | Goldman       | 6800.50  |
| 2025-02-14 | Fund_B    | GS     | Goldman Sachs     | Goldman       | 9300.25  |
| 2025-02-14 | Fund_B    | MS     | Morgan Stanley    | Morgan Stanley| 7100.00  |
| 2025-02-14 | Fund_B    | V      | Visa Inc          | JP Morgan     | 13400.50 |
| 2025-02-14 | Fund_B    | MA     | Mastercard Inc    | Goldman       | 10900.75 |
| 2025-02-14 | Fund_B    | PYPL   | PayPal Holdings   | Morgan Stanley| -800.00  |
| 2025-02-14 | Fund_B    | SQ     | Block Inc         | JP Morgan     | 4200.25  |

### Sample API Call

**Use Case**: Get YTD PnL at Fund + Company level

API Request:

    POST /api/portfolio/aggregate
    
    {
      "groupby": ["fund", "company"],
      "metric": "pnl",
      "filters": {
        "date_range": {
          "start": "2025-01-01",
          "end": "2025-02-14" # assume this is today's date.
        }
      },
      "aggregation": "sum"
    }

Expected Response (abbreviated):

    {
      "data": [
        {"fund": "Fund_A", "company": "Apple Inc", "pnl": 245680.50},
        {"fund": "Fund_A", "company": "Microsoft Corp", "pnl": 338912.75},
        {"fund": "Fund_A", "company": "NVIDIA Corp", "pnl": 521400.25},
        ...
        {"fund": "Fund_B", "company": "Apple Inc", "pnl": 142300.00},
        {"fund": "Fund_B", "company": "JPMorgan Chase", "pnl": 289650.75},
        ...
      ],
      "execution_time_ms": 9842,
      "cached": false
    }

---

## Existing Solution

Design review of the below implementation for adding caching to the above APIs.
This is invoked by daily job at end of day - pre-warming so users don't face cold cache

**Use case**:
Build caching for two use cases in dashboard:
   * YTD Pnl - Fund groupby
   * YTD Pnl - Fund, Company groupby.
   * Possible numerous cuts & filters in the future 


### Implementation Pseudocode

    @data_cache(ttl=86400)  # 24 hour TTL
    def get_portfolio_pnl(groupby_fields, filters, date_range):
        """
        Aggregates PnL based on groupby fields and filters.
        Takes ~10 seconds without cache.
        """
        # Query database and compute aggregations
        result_df = compute_pnl_aggregation(groupby_fields, filters, date_range)
        return result_df

### @data_cache Decorator Logic

    def data_cache(ttl=86400):
        def decorator(func):
            def wrapper(*args, **kwargs):
                # 1. Construct cache key
                module_name = func.__module__
                func_name = func.__name__
                
                # Serialize input args by calling str() on each
                serialized_args = [str(arg) for arg in args]
                serialized_kwargs = [f"{k}={str(v)}" for k, v in sorted(kwargs.items())]
                
                cache_key = f"{module_name}:{func_name}:{':'.join(serialized_args + serialized_kwargs)}"
                
                # 2. Check cache
                cached_value = redis_client.get(cache_key)
                if cached_value:
                    # Unpickle if it's a DataFrame
                    return pickle.loads(cached_value)
                
                # 3. Acquire distributed lock to prevent thundering herd
                lock_key = f"lock:{cache_key}"
                with RedisLock(redis_client, lock_key, timeout=30):
                    # Double-check cache after acquiring lock
                    cached_value = redis_client.get(cache_key)
                    if cached_value:
                        return pickle.loads(cached_value)
                    
                    # 4. Cache miss - execute function
                    result = func(*args, **kwargs)
                    
                    # 5. Pickle DataFrame and store in Redis
                    pickled_result = pickle.dumps(result)
                    redis_client.setex(cache_key, ttl, pickled_result)
                    
                    return result
            
            return wrapper
        return decorator

### Key Design Choices
- **Generic decorator**: Can be added to any function
- **Default TTL**: 24 hours (aligned with daily position data refresh)
- **Key construction**: Module name + function name + stringified input args
- **Serialization**: DataFrames are pickled for storage
- **Concurrency control**: Redis distributed lock prevents multiple workers from hitting DB simultaneously
- **Eviction policy**: Defaults to Redis's volatile-lru (evicts least recently used keys with TTL set)
