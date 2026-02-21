---
id: constitution-20260108-001
title: Constitution Update - Phase II Full-Stack App
stage: constitution
date: 2026-01-08
---

# Constitution Update - Phase II Full-Stack App

## PROMPT_TEXT

You are Claude Code operating under a strict Spec-Driven Development workflow.

Your task is to CREATE a NEW Markdown file named `constitution.md` for **Phase II: Todo Full-Stack Web Application**.

You MUST use the provided Phase I constitution as a reference, but this is NOT a minor edit.
This is a MAJOR architectural evolution from a console app to a secure, multi-user full-stack web application.

========================
REFERENCE INPUT (PHASE I)
========================
Use the following Phase I constitution ONLY as historical context for evolution:

- Phase I was an in-memory Python console app
- Simplicity and standard library usage were NON-NEGOTIABLE
- No persistence, no web, no authentication

========================
PHASE II REQUIREMENTS
========================

1. This constitution MUST be for:
   **Todo Full-Stack Web Application (Phase II)**

2. REMOVE any principle related to:
   - In-memory storage
   - Python standard library only
   - Console menu loop
   - Simplicity as a non-negotiable constraint
3. ADD and ENFORCE the following NON-NEGOTIABLE principles:
   - Full-Stack Modularity (Frontend + Backend + Shared Specs)
   - Persistent Storage (Neon Serverless PostgreSQL)
   - Multi-User Authentication & Authorization
   - Strict User Data Isolation

4. Technology constraints MUST include:
   - Frontend: Next.js 16+ (App Router)
   - Backend: FastAPI (Python 3.13+)
   - ORM: SQLModel
   - Database: Neon Serverless PostgreSQL
   - Authentication: Better Auth issuing JWT tokens
   - Shared secret via `BETTER_AUTH_SECRET`
   - Spec-Kit Plus + Claude Code only (no manual coding)
   - Docker Compose for local development
5. Core Features MUST remain EXACTLY 5:
   - Add task
   - Delete task
   - Update task
   - View/List tasks
   - Toggle complete/incomplete
   BUT rewritten for a **multi-user authenticated web context**

6. Security rules MUST state clearly:
   - All API endpoints require JWT authentication
   - Backend must verify JWT tokens
   - User identity must be extracted from token
   - All database queries MUST be filtered by authenticated user
   - Unauthorized requests return 401
7. Project structure MUST describe a MONOREPO with:
   - /.spec-kit/config.yaml
   - /specs (features, api, database, ui)
   - /frontend (Next.js)
   - /backend (FastAPI)
   - docker-compose.yml
   - root-level CLAUDE.md and README.md

8. Governance section MUST:
   - Enforce Spec → Plan → Tasks → Implement cycle
   - Require Sync Impact Report for amendments
   - Treat this constitution as a binding development contract
9. Include a **Sync Impact Report** comment block at the top indicating:
   - Version change: 1.0.0 → 2.0.0
   - Removal of in-memory/console principles
   - Addition of full-stack, security, persistence principles

10. Output MUST be:
   - Valid Markdown
   - A complete standalone `constitution.md`
   - No explanations, no analysis, no extra commentary
   - ONLY the final Markdown file content

BEGIN GENERATION NOW.

## RESPONSE_TEXT

A new constitution.md file has been created for the Todo Full-Stack Web Application (Phase II), replacing the previous Todo In-Memory Python Console App constitution. The update includes:

- Version change from 1.0.0 to 2.0.0
- Removal of in-memory storage, Python standard library only, and console menu loop principles
- Addition of full-stack modularity, persistent storage & security, multi-user authentication & authorization, and full-stack architecture principles
- Implementation of security rules requiring JWT authentication
- Definition of project structure for a monorepo with frontend, backend, and specs
- Technology stack including Next.js, FastAPI, SQLModel, Neon Serverless PostgreSQL, and Better Auth
- Core features rewritten for a multi-user authenticated web context