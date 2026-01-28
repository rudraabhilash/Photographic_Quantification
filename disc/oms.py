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
# Streaming	Hard	Built-in
# Internal services	OK	Excellent

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