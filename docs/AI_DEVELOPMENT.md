# AI Development Contract

This document defines the development rules for every AI assistant working on
Vitesse Control Center (VCC).

These rules take precedence over personal coding preferences.

---

# Project Overview

Project Name:
Vitesse Control Center (VCC)

Purpose:
A Flask-based management application for maintaining Nintendo Switch game
libraries, update auditing, metadata synchronization, storage analysis and
system management.

Primary Goals

- Maintainable code
- Consistent architecture
- Small incremental changes
- Production stability
- Easy future expansion

---

# Architecture

Current architecture:

SQLite
↓
Database
↓
Repository
↓
Service Layer
↓
Flask Routes
↓
Templates

Rules

- SQL belongs in Repository classes.
- Business logic belongs in Services.
- Routes should remain thin.
- Templates must contain presentation only.
- Never bypass the Repository layer.
- Never place SQL inside Flask routes.
- Never place business logic inside templates.

---

# Python Environment

Always use the existing project virtual environment.

Use:

.venv/

Rules

- Never create a new virtual environment.
- Never install packages unless explicitly requested.
- Never upgrade dependencies automatically.
- Reuse the existing interpreter whenever possible.

---

# Database

Database engine:
SQLite

Rules

- One Database instance per Flask request.
- Store Database in flask.g.
- Close connections using teardown_appcontext.
- Never use global SQLite connections.
- Never disable SQLite thread safety using
  check_same_thread=False.

---

# Dependency Injection

Repositories are injected into Services.

Services are injected into Routes.

Never instantiate repositories inside business logic.

Prefer constructor injection whenever practical.

---

# Coding Standards

Before changing code:

1. Analyse the problem.
2. Identify the root cause.
3. Explain the architectural impact.
4. Implement the smallest possible fix.

Rules

- Prefer minimal patches.
- Never rewrite complete files unless necessary.
- Reuse existing code.
- Avoid duplication.
- Follow existing naming conventions.
- Preserve backwards compatibility.

---

# Error Handling

Always prefer understanding the failure before modifying code.

Stack traces are the primary source of truth.

Never guess.

If information is missing, explain what is required.

---

# Git Workflow

Prefer:

Small commits.

One feature per commit.

One bug fix per commit.

Always leave the project in a working state.

---

# User Interface

Framework:
Bootstrap

Theme:
Dark

Rules

- Keep the interface clean.
- Avoid unnecessary animations.
- Use Bootstrap components whenever possible.
- Keep layouts responsive.
- Prefer consistency over creativity.

---

# Performance

Avoid unnecessary database queries.

Avoid duplicate SQL.

Avoid loading unnecessary data.

Prefer Repository methods over ad-hoc queries.

---

# Validation

Every completed task should verify:

- Application starts.
- No syntax errors.
- No new warnings introduced.
- Existing functionality still works.

---

# Prompt Behaviour

Unless explicitly instructed otherwise:

Always

- analyse first
- explain root cause
- implement smallest possible fix
- validate afterwards

Never immediately rewrite large portions of the application.

---

# Future Development

This project is intended to grow incrementally.

When introducing new functionality:

- reuse existing architecture
- preserve consistency
- minimise technical debt
- prefer extensibility over shortcuts