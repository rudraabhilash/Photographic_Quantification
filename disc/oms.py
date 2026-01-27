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
# ************************************************************************************
