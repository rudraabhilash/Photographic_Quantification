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
# ************************************************************************************
