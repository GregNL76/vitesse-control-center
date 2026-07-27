# Vitesse Control Center Architecture

This document describes the overall software architecture of VCC.

It is intended for both human developers and AI assistants.

---

# Design Philosophy

The project prioritises:

- Simplicity
- Maintainability
- Stability
- Incremental growth

Avoid unnecessary complexity.

---

# Layer Overview

Presentation

↓

Flask Routes

↓

Services

↓

Repositories

↓

Database

↓

SQLite

Each layer has a single responsibility.

---

# Responsibilities

## Flask Routes

Responsible for:

- HTTP requests
- Validation
- Calling Services
- Rendering templates

Routes should remain thin.

---

## Services

Responsible for:

- Business logic
- Workflow
- Aggregating repository calls

Services should not contain SQL.

---

## Repositories

Responsible for:

- SQL
- CRUD operations
- Query optimisation

Repositories should not contain business logic.

---

## Database

Responsible for:

- SQLite connection
- Transactions
- Connection lifecycle

---

# Dependency Direction

Allowed

Routes
→ Services

Services
→ Repositories

Repositories
→ Database

Not allowed

Routes
→ Database

Routes
→ SQL

Templates
→ Database

Templates
→ Services

---

# Current Modules

Dashboard

Game Library

Git

Metadata

Update Auditor

Storage

Settings

Activity Log

System Information

Future modules should follow the same architecture.

---

# Database

Current database:

SQLite

Request scoped.

Future migration to PostgreSQL should require minimal changes.

---

# Activity Log

All application events should be recorded using the Activity Log.

Examples

- Library scan
- Metadata sync
- Git push
- Update audit
- Errors
- Warnings

The dashboard consumes this information.

---

# Error Handling

Errors should:

- be logged
- contain meaningful messages
- avoid exposing internal implementation

---

# Naming

Prefer descriptive names.

Good

GameRepository

DashboardService

ActivityRepository

Avoid

Helper

Utils

Stuff

Manager

Unless their responsibility is very well defined.

---

# Future Expansion

New functionality should fit naturally into the existing layers.

Avoid shortcuts.

If a feature requires bypassing the architecture, reconsider the design first.

---

# AI Guidance

Before implementing new functionality, always ask:

- Does this belong in a Route?
- Does this belong in a Service?
- Does this belong in a Repository?

Choose the lowest layer that owns the responsibility.

Keep changes small.

Protect the architecture.
