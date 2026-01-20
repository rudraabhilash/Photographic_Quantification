# print("Hello!")

# -Name(), size, price


# sum (pricei * sizei)/sum(sizei )


# def update(name, size, price)
# def getavgprice(name): -> ave price of that name

class StockVwap:
    """ 
    Volume weighted average price calculator 
    for different stock names using streaming updates.
    """
    __slots__ = ('sumPriceSize', 'sumSize')

    def __init__(self) -> None:
        self.sumPriceSize: Dict[str, float] = {}
        self.sumSize: Dict[str, int] = {}

    def update(self, symbol: str, price: float, size: int) -> None:
        if size <= 0:
            raise ValueError("Trade size must be positive")

        symbol = symbol.upper()
        if symbol not in self.sumPriceSize:
            self.sumPriceSize[symbol] = 0.0
            self.sumSize[symbol]      = 0

        self.sumPriceSize[symbol] += price * size
        self.sumSize[symbol] += size

    def getVwap(self, symbol: str) -> float:
        symbol = symbol.uppper()
        if symbol not in self.sumPriceSize:
            raise KeyError(f"unknown symbol: {symbol}")
        return self.sumPriceSize[symbol]/self.sumSize[symbol]


import threading
class ThreadSafeStockVwap:
    """ 
    Multithreading safe version 
    Volume weighted average price calculator 
    for different stock names using streaming updates.
    """
    __slots__ = ('_sumPriceSize', '_sumSize', '_lock')

    def __init__(self) -> None:
        self._sumPriceSize: Dict[str, float] = {}
        self._sumSize: Dict[str, int] = {}
        self._lock = threading.Lock()

    def update(self, symbol: str, price: float, size: int) -> None:
        if size <= 0:
            raise ValueError("Trade size must be positive")

        symbol = symbol.upper()
        with self._lock:
            if symbol not in self._sumPriceSize:
                self._sumPriceSize[symbol] = 0.0
                self._sumSize[symbol]      = 0

            self._sumPriceSize[symbol] += price * size
            self._sumSize[symbol] += size

    def getVwap(self, symbol: str) -> float:
        symbol = symbol.upper()
        with self._lock:
            if symbol not in self._sumPriceSize:
                raise KeyError(f"unknown symbol: {symbol}")
            return self._sumPriceSize[symbol] / self._sumSize[symbol]
#since updates are tiny(two dictionary ops) therefore lock contention should be minimal. 
# HFT systems later shard by symbol or CPU core.

#client code
import random
import time

vwap_engine = ThreadSafeStockVwap()
def market_feed(symbol: str):
    for _ in range(1000):
        price = random.uniform(100, 200)
        size = random.randint(1, 1000)
        vwap_engine.update(symbol, price, size)
        time.sleep(random.uniform(0.001, 0.01))

threads = [
    threading.Thread(target=market_feed, args=("RIL",)),
    threading.Thread(target=market_feed, args=("TCS",)),
]
for t in threads:
    t.start()
for t in threads:
    t.join()
print("RIL VWAP:", vwap_engine.getVwap("RIL"))


import asyncio
class AsyncStockVwap:
    """ 
    Async version - used when WebSockets or FIX gateways or Async market-data pipelines are used.
    Volume weighted average price calculator 
    for different stock names using streaming updates.
    """
    __slots__ = ('_sumPriceSize', '_sumSize', '_lock')

    def __init__(self) -> None:
        self._sumPriceSize: Dict[str, float] = {}
        self._sumSize: Dict[str, int] = {}
        self._lock = asyncio.Lock()

    async def update(self, symbol: str, price: float, size: int) -> None:
        if size <= 0:
            raise ValueError("Trade size must be positive")

        symbol = symbol.upper()
        async with self._lock:
            if symbol not in self._sumPriceSize:
                self._sumPriceSize[symbol] = 0.0
                self._sumSize[symbol]      = 0

            self._sumPriceSize[symbol] += price * size
            self._sumSize[symbol] += size

    async def getVwap(self, symbol: str) -> float:
        symbol = symbol.upper()
        async with self._lock:
            if symbol not in self._sumPriceSize:
                raise KeyError(f"unknown symbol: {symbol}")
            return self._sumPriceSize[symbol] / self._sumSize[symbol]

#Async trade feed simulation
async def async_market_feed(vwap_engine: AsyncStockVwap, symbol: str):
    for _ in range(1000):
        price = random.uniform(100, 200)
        size = random.randint(1, 1000)
        await vwap_engine.update(symbol, price, size)
        await asyncio.sleep(random.uniform(0.001, 0.01))
async def main():
    vwap_engine = AsyncStockVwap()
    await asyncio.gather(
        async_market_feed(vwap_engine, "RIL"),
        async_market_feed(vwap_engine, "TCS"),
    )
    ril_vwap = await vwap_engine.getVwap("RIL")
    print("RIL VWAP (async):", ril_vwap)
asyncio.run(main()) 


# 🔹 Stage 2.1 — Symbol-based sharding

# Instead of one global VWAP store, you create N independent shards:

# Shard 0 → symbols hashing to 0
# Shard 1 → symbols hashing to 1
# ...
# Shard N-1


# Each shard has:

# Its own dict

# Its own lock

# Its own CPU affinity

# shard_id = hash(symbol) % N


# ✔ Updates to different symbols never contend
# ✔ Linear scaling until memory bandwidth saturates

# 🔹 Stage 2.2 — Feed fan-in pattern

# Real market data:

# NSE feed

# BSE feed

# Dark pools

# Internal order book

# Architecture

# [Feed Threads] ──▶ [Shard Queues] ──▶ [VWAP Shards]


# Feed threads never compute

# They push raw events to shard-local queues

# VWAP shards consume sequentially

# ✔ Predictable latency
# ✔ No shared mutable state across threads

# 🔹 Stage 3.3 — Data structures (key difference)

# Instead of dictionaries:

# Array-indexed symbol IDs

# Struct-of-arrays layout

# total_value[symbol_id]
# total_volume[symbol_id]
# Why?
# Predictable memory access
# Vectorizable
# Cache-friendly


# “Linear scaling until memory bandwidth saturates” — what does this really mean?
# What is being scaled?

# You add:

# more shards

# more threads

# more CPU cores

# Each shard processes independent symbols.

# If nothing else limits you, throughput should scale like:

# 2 cores → ~2× updates/sec
# 4 cores → ~4× updates/sec
# 8 cores → ~8× updates/sec


# This is linear scaling.

# Why does VWAP scale linearly at first?

# Because each update does:

# LOAD  total_value[symbol]
# LOAD  total_volume[symbol]
# ADD   size * price
# STORE total_value[symbol]
# STORE total_volume[symbol]


# That’s:

# Very few instructions

# No complex branching

# No dependency across symbols

# CPU pipelines stay mostly idle waiting for memory.

# 2️⃣ Why does scaling stop? → Memory bandwidth
# Key fact (critical insight):

# Modern CPUs can execute billions of arithmetic ops/sec,
# but memory can only move so many bytes per second.

# Example (realistic numbers)
# Assume:

# Each update touches ~64 bytes (cache lines)

# Server memory bandwidth ≈ 100 GB/s

# Then max updates/sec:

# 100 GB/s ÷ 64 bytes ≈ 1.5 billion updates/sec


# No matter how many cores you add:
# ❌ you cannot exceed memory bandwidth


# Your VWAP math:

# total += size * price


# → negligible

# Your real cost:

# load/store dictionary entry


# → hundreds of cycles

# Hence:

# Memory access dominates.

# 4️⃣ Why sharding helps — but only up to a point
# Before sharding:

# One hot dictionary

# Cache line bouncing

# Lock contention

# After sharding:

# Cache-local data

# Independent memory streams

# Better prefetching

# ✔ Linear gains initially
# ❌ Still bounded by DRAM throughput

# 5️⃣ Python vs C++ — same wall, different distance
# Python hits the wall earlier because:

# Larger objects

# Pointer indirection

# Worse cache locality

# GIL overhead

# C++:

# Flat arrays

# Tight memory layout

# Prefetch-friendly

# But both hit the same physical limit:

# Bytes/sec from memory

# 6️⃣ Why HFT systems obsess over cache locality

# To delay hitting the bandwidth wall:

# Keep hot symbols in L1/L2 cache

# Use struct-of-arrays

# Pin threads to cores

# Avoid heap allocation

# Avoid dictionaries

# This lets systems run at:

# Cache speed instead of DRAM speed

# Nanoseconds instead of microseconds

# 7️⃣ Interview-quality explanation (say this)

# If asked:

# “Why does it scale linearly and then stop?”

# Answer:

# “Each VWAP update is memory-bound, not compute-bound.
# Sharding removes contention so throughput scales with cores until the memory subsystem saturates.
# Beyond that point, adding cores increases cache misses and doesn’t increase throughput.”

# That is textbook correct.

# 8️⃣ One mental model to remember forever

# CPUs are fast calculators attached to slow memory pipes.
# VWAP needs almost no math, but a lot of memory movement.


#Understanding what is memory movement - 
# Cache line reality (critical)
# CPUs don’t move 8 bytes
# They move cache lines (typically 64 bytes)
# So even if you update:
# 8 bytes (float)
# The CPU actually moves:
# 64 bytes from memory → cache
# 64 bytes from cache → memory (later)
# That is memory movement.

#what is memory bandwidth? - Maximum amount of data that can be transferred between CPU and RAM per second(GB/s)
# This is peak theoretical bandwidth - 100GB/s.
# Real usable bandwidth:
# ~70–80 GB/s
# Important distinction
# This is not storage (SSD).
# This is RAM → CPU.
# Even the fastest CPUs cannot exceed this.

# Analogy (very accurate)
# Think of DRAM as:
# A highway
# With fixed number of lanes
# Cars = cache lines
# You can add:
# More cars (cores)
# Faster engines (CPU)
# But the highway width stays the same.
# Eventually:
# traffic jam
# 5️⃣ Why VWAP hits the bandwidth wall early
# VWAP is:
# Extremely light on math
# Extremely heavy on memory
