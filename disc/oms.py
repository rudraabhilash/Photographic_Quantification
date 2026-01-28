# Trader / Client
#      ↓
#   Order Entry
#      ↓
#   Rule Checks
#      ↓
#   Order Book (Tracking)
#      ↓
#   Send to Execution
#      ↓
#   Updates & Reports


#1. order_entry.py - f(what_to_buy_sell, quantity, price, order_type)
#2. rule_checks.py - f(order) -> bool  i.e. client, instrument, qty allowed
#3. order_book.py - class OrderBook: add_order(order), update_order(order_id, status)
#  i.e.  order_id, status(new/sent/partially filled/filled/cancelled) 
#4. execution.py - f(send_order_to_market(order))
#5. updates_reports.py - f(generate_report(order_book))

# OMS vs Execution (1-line memory trick)
# OMS = Control + Tracking
# Execution = Speed + Smartness

# Why companies NEED OMS (even small ones)
# Because OMS:
# Prevents bad / illegal trades
# Gives full audit trail
# Helps operations team
# Keeps clients and regulators happy
# Without OMS = chaos 😵
# Order Management System (OMS) - Simplified Overview
# An OMS is software that helps traders and brokers manage orders from clients.
# It ensures orders are processed correctly, tracked, and reported.
# Key Components of an OMS:
# 1. Order Entry: Where traders input orders (buy/sell, quantity, price, type).
# 2. Rule Checks: Validates orders against rules (client permissions, instrument limits).
# 3. Order Book: Tracks all orders and their statuses (new, sent, filled, cancelled).
# 4. Execution: Sends orders to the market for execution.
# 5. Updates & Reports: Generates reports for clients and compliance.
# Why OMS is Important:
# - Prevents illegal trades by enforcing rules. 
# - Provides a full audit trail for compliance.
# - Helps operations teams manage orders efficiently.
# - Keeps clients and regulators satisfied.
# OMS vs Execution Systems:
# - OMS focuses on control and tracking of orders.
# - Execution systems focus on speed and smart order routing.# Summary:
# An OMS is essential for any trading operation to ensure smooth, compliant, and efficient order management.# Order Management System (OMS) - Simplified Overview
# An OMS is software that helps traders and brokers manage orders from clients.
# It ensures orders are processed correctly, tracked, and reported.
# Key Components of an OMS:
# 1. Order Entry: Where traders input orders (buy/sell, quantity, price, type).
# 2. Rule Checks: Validates orders against rules (client permissions, instrument limits).
# 3. Order Book: Tracks all orders and their statuses (new, sent, filled, cancelled).
# 4. Execution: Sends orders to the market for execution.
# 5. Updates & Reports: Generates reports for clients and compliance.

# ┌─────────────────────────────┐
# │        Client / Trader UI   │
# └──────────────┬──────────────┘
#                ↓
# ┌─────────────────────────────┐
# │      API / Gateway Layer    │
# └──────────────┬──────────────┘
#                ↓
# ┌─────────────────────────────┐
# │        OMS Core Services    │
# │ ─ Order Lifecycle           │
# │ ─ Validation & Rules        │
# │ ─ State Management          │
# │ ─ Amend / Cancel            │
# └──────────────┬──────────────┘
#                ↓
# ┌─────────────────────────────┐
# │     Risk & Compliance       │
# └──────────────┬──────────────┘
#                ↓
# ┌─────────────────────────────┐
# │  Execution Adapter Layer    │
# └──────────────┬──────────────┘
#                ↓
# ┌─────────────────────────────┐
# │   Execution / EMS / Algo    │
# └─────────────────────────────┘
#                ↓
# ┌─────────────────────────────┐
# │ Persistence & Reporting     │
# └─────────────────────────────┘
# ************************************************************************************

#Client / Trader UI - 
# 1️⃣ Client / Trader Interface Layer

# Responsibilities
# Order entry (New / Amend / Cancel)
# Order blotter (real-time state)
# Allocation screens
# Admin & ops dashboards

# Key points (senior-level)
# OMS must be UI-agnostic
# UI talks via REST / FIX / gRPC
# Stateless UI, all state lives in OMS

#gRPC - gRPC is a fast, binary, contract-based way for services to talk to each other.
#grpc - Google Remote Procedure Call. 
# gRPC vs REST (practical comparison)
# Aspect	               REST	           gRPC
# Payload	              JSON(text)	   Protobuf (binary)
# Speed	                  Moderate	       Fast
# Contract	              Implicit         Explicit
# Browser friendly	      Yes            	No
# Streaming            	  Hard	           Built-in
# Internal services	      OK	           Excellent
# Why gRPC is popular in OMS / trading systems
# 1️⃣ Performance 🚀
# Binary format (smaller payloads)
# Lower CPU & network overhead
# Perfect for:
# OMS ↔ Risk
# OMS ↔ Execution
# OMS ↔ Reporting
# 2️⃣ Strong contracts
# With REST:
# Missing fields show up at runtime
# Breaking changes slip through
# With gRPC:
# Contract is explicit
# Breaking change = compile error
# 3️⃣ Streaming (very important)
# gRPC supports:
# Server streaming
# Client streaming
# Bi-directional streaming
# Example:
# OMS pushes continuous order updates to blotter backend
# Push model Much cleaner than polling(pull model every sec) REST.


#Sample protobuf code for User message - 
# import user_pb2
# # Create the object
# user = user_pb2.User()
# user.id = 1
# user.name = "Alice"
# user.email = "alice@example.com"
# # Serialize to a compact binary string
# binary_data = user.SerializeToString()

# What a Stateless UI is ✅
# A stateless UI:
# Does not remember orders
# Does not store order status
# Does not decide what the truth is
# Only displays what OMS tells it
# Think of the UI as a TV screen, not a brain 📺
#“Stateless UI means the presentation layer does not persist or derive authoritative order 
# state. The OMS remains the single source of truth, ensuring consistency, auditability, 
# and crash-safe recovery.”
# “UI can cache for performance, but cached data is never authoritative and must always be 
# revalidated against OMS.”

# Golden rule
#Cache things that are slow to change or non-authoritative
#Never cache things that define trading -truth.

# A. Reference data (minutes–hours TTL)
# Examples:
# Instrument master (symbol → ISIN)
# Tick size
# Lot size
# Contract expiry dates
# Exchange trading hours
# Why cache?
# DB joins are expensive
# Reference data changes rarely
# Revalidation:
# Version check
# Daily refresh
# Push invalidation

# B. User & permission metadata
# Examples:
# Trader name
# Desk
# Role (Trader / Ops / Admin)
# Allowed asset classes
# Why cache?
# Permissions rarely change intraday
# Validation:
# Token refresh
# Session expiry
# Permission version mismatch

# C. Historical data (read-only)
# Examples:
# Yesterday’s orders
# Closed trades
# Past audit logs
# Why cache?
# Immutable data
# Large result sets

# Validation:
# Simple checksum or timestamp
# No need to re-query OMS often
# D. UI-only derived data
# Examples:
# Column sorting
# Grouped views
# Aggregated quantities (for display only)

# Why cache?
# Improves UI responsiveness
# No business impact
# Validation:
# Recomputed when authoritative data changes
# ❌ NEVER cache as authoritative
# Order status
# Filled quantity
# Average price
# Cancel / amend result
# Risk status
# These must always come from OMS.

# Filled = exchange has matched your order with a counterparty.
# Example:
# Buy 1000 shares @ 100
# Market reality:
# 300 shares matched at 100
# later 200 shares matched at 99.9
# later 500 shares matched at 100.1
# Each match = fill
# Exchange
#    ↓ (trade confirmation)
# Execution System / EMS
#    ↓ (normalized fill message)
# OMS
# OMS never talks directly to exchange.

# Fill = actual execution event from exchange
# One order → many fills
# Example:
# Order: Buy 1000
# Fill #1: 300 @ 1500
# Fill #2: 200 @ 1499.5
# Fill #3: 500 @ 1500.2


# OMS stores each fill separately.
# Why?
# P&L calculation
# Audit
# Exchange reconciliation

# Amendments
# Changes to an existing order
# Change price from 1500 → 1501
# Stored because:
# Regulators care
# Disputes happen

# Cancellations
# Trader intent to stop execution
# Cancel remaining quantity
# Important:
# Cancel request ≠ cancel success
# OMS stores both request & confirmation


# Timestamps
# Every step has time:
# Order received
# Sent to execution
# Fill received
# Cancel confirmed
# Used for:
# Latency analysis
# Regulatory reporting
# Dispute resolution

# Audit trail - Immutable history of everything
# Includes:
# Who did what
# When
# From where
# Before/after state
# No deletes. Ever.


# 2️⃣ Real scenario where revalidation SAVES you 💣
# Scenario: Cached order state without revalidation
# UI caches:
# Order 123 → PARTIALLY_FILLED (500/1000)
# OMS receives:
# Remaining 500 filled
# UI misses event due to:
# WebSocket disconnect
# Browser tab sleeping
# Trader sees:
# PARTIALLY_FILLED
# and tries to:
# CANCEL order
# What happens next?
# Without revalidation ❌
# UI sends cancel
# OMS says: Order already FILLED
# Trader is confused
# Support ticket created
# Trust lost
# With revalidation ✅
# Before sending cancel:
# UI → OMS: GET /orders/123
# OMS → UI: FILLED

# UI:
# Blocks cancel button
# Shows correct status
# 💡 Revalidation prevented a bad action
# Caching optimizes reads. Revalidation protects writes.

# Where caching saves time
# A. UI rendering speed
# Without cache:
# Every scroll
# Every filter
# Every sort
# → OMS API call

# With cache:
# UI works locally
# OMS untouched
# OMS load ↓
# UI responsiveness ↑
# 
# Revalidation happens:
# Only on critical actions
# Only on state-changing operations

#C. Smart revalidation (not full refresh)

# UI does cheap validation, not full reload.
# Examples:
# Version check
# LastUpdated timestamp
# ETag

# If version unchanged → trust cache
# Else → refresh

# That’s milliseconds, not seconds.

# Typical senior-level flow (VERY IMPORTANT)
# UI loads → uses cached snapshot
# User clicks action (Cancel / Amend)
#       ↓
# UI revalidates only THAT order
#       ↓
# OMS confirms state
#       ↓
# Action allowed or blocked

# OMS is not hammered constantly.

# Why this matters in real systems
# Thousands of traders
# Tens of thousands of orders
# OMS must stay stable under load

# So:
# Cache for read scalability
# Revalidate for write correctness

# “Caching improves UI responsiveness and reduces OMS read load, while revalidation is 
# applied selectively on state-changing actions to ensure correctness without sacrificing 
# performance.” 

# Order blotter = a real-time table that shows the current state of all orders
# Think of it as the live dashboard of trading activity.

# Exchange fills
#      ↓
# Execution System
#      ↓
# OMS (state updated)
#      ↓
# Order Blotter UI

# The blotter never talks to exchange directly.

# Why order blotter is CRITICAL

# 1️⃣ Trader decision-making
# Trader answers instantly:
# “Is my order live?”
# “How much is filled?”
# “Should I amend or cancel?”
# Without blotter → blind trading.

# 2️⃣ Operations & support
# Ops teams use blotter to:
# Investigate issues
# Answer client queries
# Reconcile mismatches

# 3️⃣ Compliance & audit
# Blotter provides:
# Time-stamped visibility
# Evidence of orderly trading


# How blotter stays real-time

# WebSocket / push updates
# Event-driven OMS notifications
# Periodic re-sync on reconnect

# An order blotter is a real-time, read-only view that displays the current lifecycle 
# state of orders as maintained by the OMS, enabling traders and operations to monitor 
# and act on active and historical orders.Caching rules

# Blotter may cache rows
# But revalidates on:
# Cancel
# Amend
# Allocate

# Blotter can be fast by pagination, filtering, and incremental updates.
# Incremental updates (VERY IMPORTANT)
# What problem does this solve?

# ❌ Bad approach:
# Reload entire blotter every second

# ✅ Good approach:
# Only update what changed
# What “incremental update” means
# Instead of:
# Send all 10,000 orders again
# OMS sends:
# Order 123 → filledQty changed 300 → 800
# UI:
# Updates only that row


# 4️⃣ How blotter stays real-time (brief but clear)
# A. WebSocket / Push updates
# Instead of UI asking repeatedly:
# “Anything changed?”
# OMS pushes updates:
# Order 123 updated


# Result:
# Near real-time
# No polling storm

# B. Event-driven OMS notifications
# OMS internally works on events:
# FillReceived
# OrderCancelled
# OrderRejected
# Each event:
# Updates OMS state
# Triggers notification to UI
# So UI reacts to events, not guesses.

# C. Periodic re-sync on reconnect (safety net 🛟)
# Why needed?
# Network drops
# Browser sleeps
# WebSocket disconnects
# When UI reconnects:
# UI → OMS: Give me all orders updated after T
# OMS:
# Sends latest snapshot
# UI fixes any missed updates
# This prevents:
# Ghost orders
# Wrong status

# “Through event-driven updates pushed from OMS over persistent connections, 
# with periodic reconciliation to handle disconnects.”
# ************************************************************************************
# ************************************************************************************

# 2️⃣ API / Gateway Layer
# Why this layer exists
# Decouple clients from OMS internals
# Protect OMS from bad traffic
# Responsibilities
# Authentication / authorization
# Rate limiting
# Request validation
# Protocol translation (REST ↔ FIX)

# Design note
# This is where you stop bad requests before touching core OMS logic.

# Reason 1: Decouple clients from OMS internals
# What this means in practice
# Clients should not know:
# OMS internal data model
# OMS internal services
# OMS internal state machine
# Clients should only know:

# POST /orders
# POST /orders/{id}/cancel
# GET  /orders/{id}

# 👉 If OMS internals change, clients don’t break.

# Reason 2: Protect OMS from bad traffic

# OMS core is:
# Stateful
# Transactional
# Sensitive to load

# Bad traffic can:
# Corrupt state
# Overload DB
# Break order sequencing
# Gateway acts as shock absorber 🛡️

# A. Authentication / Authorization
    # Is this trader logged in? #Authentication example
    # Is this algo service trusted? #Authentication example
    # Is this request signed? #Authentication example
    # Examples: OAuth tokens, API keys, FIX session credentials

    # Trader A can trade equities, not options #Authorization example
    # Algo X can only place orders, not cancel manually #Authorization example
    # Ops user can view, not trade #Authorization example

# B. Rate limiting (EXTREMELY IMPORTANT) - Action - Throttle/reject/alert
    # What problem this solves
    # Without rate limiting:
    # Algo bug sends 10,000 orders/sec
    # OMS DB overloaded
    # All traders affected

# C. Request validation
    # Syntax validation
        # Required fields present? Field types correct? Enum values valid?

    # Semantic validation
        # Quantity > 0? Price not negative? Order type supported?

    #UI also does validation, but UI can not be trusted by design and 
    #also UI can be bypassed, Algo client dont use web UI, Bugs happen.
    # In real OMS systems:
    # Client	Validation capability
    # Web UI	        Strong
    # Mobile UI	        Weak
    # Algo client	    Custom
    # External broker	FIX-based
    # Batch loader	    Scripted
    # You cannot enforce validation consistently across all of them.
    # Gateway is the single enforcement point.

# D. Protocol translation (REST ↔ FIX)
# Different clients speak different languages
# UI → REST / JSON
# External broker → FIX
# Internal algo → gRPC
# Gateway responsibility
# REST JSON → internal OMS command
# FIX msg   → internal OMS command
# OMS sees: CreateOrderCommand

# What happens if bad requests reach OMS?
# OMS core:
# Opens DB transaction
# Locks rows
# Evaluates rules
# Updates state

# Even if rejected:
# CPU used
# DB used
# Latency increased

# Gateway rejection vs OMS rejection
#    Layer	            Cost
# Gateway reject	  Microseconds
# OMS reject	      DB + locks + logs
# At scale, this difference is massive.

# 4️⃣ Design patterns commonly used (senior detail)
# API Gateway pattern
# BFF (Backend for Frontend)
# Adapter pattern (protocol handling)
# Stateless processing
# Token-based auth

# ************************************************************************************
# ************************************************************************************
# 3️⃣ OMS Core Services (Heart of the system ❤️)

# This is where senior engineers are evaluated.

# 3.1 Order Lifecycle Service
# Handles finite state machine of orders.
# Typical states:
# NEW → VALIDATED → SENT
# SENT → PARTIALLY_FILLED → FILLED
# SENT → CANCELLED
# REJECTED (terminal)

# Key senior concept
# Order state must be strongly consistent
# No two services can “own” order state

# 3.2 Validation & Business Rules Engine
# Checks:
# Instrument eligibility
# Trading hours
# Client permissions
# Quantity & price bands
# Asset-specific rules
# Senior design pattern
# Rule engine is data-driven, not hard-coded
# Rules loaded from DB / config
# Versioned rules for audit

# 3.3 Amend / Cancel Management
# Harder than it looks.
# Challenges:
# Race conditions with fills
# Partial fills during amend
# Exchange-specific cancel semantics

# Golden rule
# OMS must reconcile exchange truth, not assume success.

# ************************************************************************************
# OMS Core Services = the authoritative brain that owns order truth
# This layer:
# Owns order state
# Owns legal transitions
# Owns business correctness
# Survives crashes and disputes
# Everything else (UI, gateway, EMS) is peripheral.

# 3.1 Order Lifecycle Service
# Handles finite state machine (FSM) of orders
# What “finite state machine” means (precisely)
# An order can only be in one of a predefined set of states, and can move only via 
# allowed transitions.

# Handles finite state machine of orders.
# Typical states:
# NEW → VALIDATED → SENT
# SENT → PARTIALLY_FILLED → FILLED(or cancel)
# SENT → CANCELLED
# REJECTED (terminal)

# Why these states exist (proof by necessity)
# Example: Why NEW and VALIDATED must be separate
# NEW = “Trader asked for something”
# VALIDATED = “OMS guarantees it is legal”
# If you merge them:
# Illegal orders may reach execution
# Audit cannot prove checks were done
# Regulatory failure.

# Why PARTIALLY_FILLED is mandatory
# Example:
# Order: Buy 1000 shares
# Fill 1: 300
# Fill 2: 200
# If you jump directly to FILLED:
# You lose intermediate truth
# You cannot reconcile exchange trades
# P&L & compliance break
# This is not optional — exchanges fill incrementally.

#At any moment, there is exactly one correct order state, and all readers see the same truth.
# “No two services can own order state” — WHY
# If two services own state, this happens:
# OMS Core: order = SENT
# Risk Service cache: order = NEW

# Risk allows amend → OMS rejects → inconsistency.
# Proof:
# This exact issue has caused real-world trading halts.

# Correct design (single ownership)
# OMS Core = single writer
# Others = read-only subscribers

# OMS writes state
# Others react to events
# Nobody else mutates state
# This is non-negotiable in trading systems.

# ************************************************************************************
# 3.2 Validation & Business Rules Engine

# This is not UI validation and not gateway validation.
# This is business legality.
# What this engine checks (and WHY)
# 1️⃣ Instrument eligibility
    # Is this symbol tradable today?
    # Is contract expired?
    # Proof: Exchanges reject expired contracts → OMS must catch earlier for audit clarity.

# 2️⃣ Trading hours
    # Market open?
    # Auction session?
    # After-hours rules?
    # Proof:
    # Orders sent outside allowed windows can:
    # Be silently rejected
    # Or queued unpredictably
    # OMS must enforce deterministic behavior.

# 3️⃣ Client permissions
    # Retail vs institutional
    # Asset-class entitlements
    # Proof:
    # Permission errors are compliance violations, not UX issues.

# 4️⃣ Quantity & price bands
    # Fat-finger protection
    # Exchange price limits
    # Proof:
    # One wrong zero (100 → 10,000) can move markets.
    # This is a documented risk (see historical “fat finger” incidents).
    # A fat-finger error in trading is when a trader or operator types the wrong number for 
    # price or quantity, often by mis-keying an extra zero or clicking the wrong field, 
    # leading to big unintended orders. These have caused huge financial losses and even 
    # brief market dislocations.

    # 1️⃣ UBS Dentsu share error (2001)
    # A trader at UBS intended to sell 6 Dentsu shares at ¥610,000 each, but instead sold
    # 610,000 shares at ¥6. UBS had to buy back shares at market value, resulting in roughly 
    # US$100 million loss.This error was directly due to mis-typed quantity/price in the 
    # trading system — a classic fat finger case.
    # 2️⃣ Mizuho Securities short sell error (2006)
    # A trader at Mizuho Securities in Japan mistakenly placed massive short orders due to a
    # fat-finger error.The firm had to unwind positions later at great cost (about ¥40 billion).
    # This shows incorrect entry in price/quantity can cause major financial loss.
    # 3️⃣ Deutsche Bank junior trader mistake (2015)
    # A junior trader at Deutsche Bank accidentally sent US $6 billion instead of the intended
    # amount when processing a payment. Although this was a cash transfer rather than a tradable 
    # security, it is categorized as a fat-finger data entry error with huge financial impact.
    # 4️⃣ Citigroup trading error / European market sell-off (2022)
    # A trader at Citigroup input the wrong amount, causing $1.4 billion in erroneous sell orders
    # instead of the intended $58 million. This triggered a brief selloff in European equity markets
    # ,leading to a regulatory fine of ~£62 million. Price and quantity mis-entry was the root cause.

    # 🛡️ 1. Pre-Trade Controls (Exchange-Level Filters) - to prevent from fat-finger
    # A. Size and Price Reasonability Limits
    # Many exchanges reject orders that are clearly outside reasonable bounds before they 
    # enter the market’s matching engine:
    # Price reasonability limits: orders with prices far outside current market range are
    #       blocked. This is a direct pre-trade defense against entering an order that is 
    #       obviously a fat-finger mistake (e.g., a price thousands of % away from current 
    #       levels).
    # Order quantity caps: Exchanges can set maximum allowed quantity caps for single orders or 
    #       for a participant’s session. Orders above these thresholds are not accepted or are
    #       held for review.
    # These controls prevent most erroneous fat-finger events before execution rather than 
    #       relying on post-execution cancelation.
    # 📊 2. Price Bands and Limit Up–Limit Down (LULD) Mechanism
    # Most modern stock and derivatives exchanges implement price bands that constrain 
    # how far a security’s price can move in a short time window. If the next trade would occur outside 
    # the permitted range, the exchange:
        # pauses trading on that security, 
        # or refuses to match that trade at out-of-range prices.
    # This is a key protection against fat-finger orders that would otherwise create an artificial price 
    # spike or plunge.
    # 🚨 3. Circuit Breakers (Market-Wide Safety Nets)
    # Circuit breakers are not fat-finger specific, but they are activated by extreme price 
    # moves — which can be caused by erroneous trades:
    # Example: U.S. stock markets halt for 15 minutes if the S&P 500 drops 7% intraday. This gives 
    # participants time to absorb information and prevents mechanical cascade selling triggered by 
    # a single large erroneous price move.
    # 🧠 4. Post-Execution Review and “Clearly Erroneous Trade” Rules
    # Even with pre-trade checks, large errors may slip through or execute on venues without pre-trade
    #  limits. Exchanges historically permit post-trade review windows, e.g.:
    # NYSE, NASDAQ, CBOT, BATS, etc., allow 30 minutes after execution to request trade cancellation 
    # if an order was clearly erroneous. This is a formal mechanism to reverse trades that meet strict 
    # criteria indicating a genuine mistake, such as:
    # price vastly different from normal range quantity orders orders never reasonably tradable
    # obvious mis-entry errors.
    # 🔄 5. Exchange Surveillance & Real-Time Monitoring
    # Exchanges continuously monitor trading activity using algorithmic surveillance systems that look 
    # for patterns inconsistent with normal market behavior, such as:
    # sudden large orders far from the prevailing price
    # volume spikes with no corresponding depth in order book
    # orders that break typical market microstructure patterns
    # These can trigger:
    # automated halts
    # alerts to surveillance teams
    # deeper review for clearly erroneous designation
    # Regulatory guidance emphasizes using multiple complementary controls to preserve market orderly 
    # behavior.


# 5️⃣ Asset-specific rules
    # Examples:
    # Options: strike / expiry combinations
    # Futures: lot size multiples
    # Equities: short-sell rules
    # Proof:
    # Rules differ per asset → hard-coding creates bugs when rules change.

# Data-driven rules (how it works)
# Rules stored in DB / config
# Evaluated dynamically
# Rule ID + version attached to decision
# Example:
# Rule: MAX_QTY_EQ_INTRA
# Version: v3
# Result: PASS

# Versioned rules — WHY this matters (proof)
# Regulator asks:
# “Why was this order allowed last Tuesday?”
# If rules are versioned:
# You can replay decision
# You can prove correctness
# Without versioning:
# You cannot defend the system
# This is regulatory survival, not elegance.
# ************************************************************************************
# 3.3 Amend / Cancel Management
# “Harder than it looks” — here’s PROOF

# Problem 1: Race condition with fills
    # Timeline
    # T1: Trader sends CANCEL
    # T2: Exchange sends FILL (remaining qty)

    # Which came first?
    # Network latency makes this non-deterministic.

    # Correct OMS behavior
    # Record both events
    # Compare timestamps / sequence
    # Accept exchange truth
    # If fill happened first:
    # Cancel must be rejected
    # Order becomes FILLED

    # If OMS assumes cancel success ❌
    # You get:
    # “Cancelled” order
    # With real trades at exchange
    # Broken positions
    # Regulatory breach
    # This has happened in real systems.

# Problem 2: Partial fills during amend
    # Example:
    # Original: Buy 1000 @ 100
    # Filled: 400
    # Amend: Change price to 101
    # What exactly is amended?
    # Correct answer:
    # Remaining 600 only

    # OMS must:
    # Split intent
    # Preserve executed quantity
    # Adjust open quantity
    # This is not trivial and must be explicit.

# Problem 3: Exchange-specific cancel semantics

    # Different exchanges:
    # Cancel is best-effort
    # Cancel is asynchronous
    # Cancel can be rejected silently
    # Proof:
    # FIX protocol itself defines cancel as a request, not a command.
    # OMS must:
    # Track cancel-requested state
    # Wait for confirmation
    # Reconcile with fills

# Golden rule (this is CRITICAL)
# “OMS must reconcile exchange truth, not assume success”
# Meaning (precise)
# OMS must treat:
# Exchange fills
# Exchange rejects
# as authoritative truth
# Not:
# UI confirmation
# Network success
# “We sent the message”

# Proof by failure scenario
# OMS assumes:
# Cancel sent → order cancelled
# Exchange reality:
# Order already filled
# Result:
# OMS says cancelled
# Exchange says filled
# Positions don’t match
# Clearing fails
# Firm loses money
# This is catastrophic, not theoretical.
# ************************************************************************************
# ************************************************************************************

# 4️⃣ Risk & Compliance Layer

# Often integrated, sometimes external.

# Pre-trade risk

# Max order size

# Exposure limits

# Fat-finger checks

# Post-trade compliance

# Market abuse checks

# Audit trails

# Regulatory reporting

# Senior insight

# Risk failures must be deterministic and explainable

# Compliance requires immutability

# ************************************************************************************
# ************************************************************************************

# 5️⃣ Execution Adapter Layer (Crucial abstraction)

# Purpose

# Hide exchange / EMS complexity from OMS

# OMS → Adapter → Exchange / EMS


# Each adapter handles:

# Protocol (FIX, native API)

# Exchange-specific fields

# Error normalization

# Why this matters

# OMS code stays stable

# New venues added without OMS rewrite

# ************************************************************************************
# ************************************************************************************

# 6️⃣ Persistence Layer (State + Audit)
# Databases used (typical)
# Data	DB Type
# Orders (current)	RDBMS
# Order history	Append-only tables
# Trades	RDBMS
# Audit logs	Immutable store
# Reference data	Cached

# Senior-level must

# Exactly-once state transitions

# Replayable event history

# Regulatory-grade audit

# ************************************************************************************
# ************************************************************************************
# 7️⃣ Eventing & Messaging
# OMS is event-driven, not request-driven.

# Events like:

# OrderCreated

# OrderValidated

# FillReceived

# CancelConfirmed

# Benefits:

# Loose coupling

# Easy recovery

# Real-time downstream updates

# ************************************************************************************
# ************************************************************************************
# 8️⃣ Reporting & Downstream Consumers

# OMS feeds:

# P&L systems

# Position management

# Clearing & settlement

# Regulatory reporting

# Often via:

# Kafka topics

# Batch exports

# APIs

# ************************************************************************************
# ************************************************************************************
# Cross-cutting concerns (INTERVIEW GOLD ⭐)
# 🔒 Consistency

# Orders require strong consistency

# Prefer DB transactions over eventual consistency

# ⏱ Latency

# OMS ≠ ultra-low latency

# Determinism > speed

# 🔁 Recovery

# Crash-safe replay from persisted state

# Idempotent message handling

# 📜 Auditability

# Every state change logged

# No deletes, only corrections

# 📈 Scalability

# Horizontal scaling by:

# Client

# Desk

# Asset class

# OMS vs EMS boundary (clear articulation)
# OMS Owns	EMS Owns
# Order lifecycle	Market execution
# Business rules	Algo logic
# Client context	Venue optimization
# Compliance	Speed


#“OMS is a stateful, rule-driven control system that owns the full order lifecycle, 
# ensures compliance and auditability, and delegates venue-specific execution to 
# downstream execution systems via adapters.”
# ************************************************************************************
# ************************************************************************************