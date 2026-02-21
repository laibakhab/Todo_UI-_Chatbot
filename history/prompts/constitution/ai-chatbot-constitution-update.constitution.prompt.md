---
id: "PHR-0001"
title: "AI Chatbot Constitution Update"
stage: "constitution"
date: "2026-02-06"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "todo-ai-chatbot"
branch: "main"
user: "System"
command: "/sp.phr"
labels: ["constitution", "ai-chatbot", "todo-app", "spec-driven"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - ".specify/memory/constitution.md"
tests: []
---

## Prompt Text
```
You are an AI assistant following the SDD-RI (Spec-Driven Development with Rapid Iteration) framework from agentfactory.panaversity.org. Generate a 'constitution.md' file for Phase III of a TODO AI Chatbot project. This constitution acts as the governing document: It defines the project's objectives, rules, behaviors, architecture, success criteria, and implementation guidelines. Base it strictly on the provided Phase III specification document below. Integrate with existing Phase 2 (TODO UI + Neon DB app), meaning update the codebase instead of creating a new one – reuse DB connections, add to existing backend/frontend folders.

Key Principles from SDD-RI:
- Agentic Dev Stack: Spec → Plan → Tasks → Implement via AI (no manual coding).
- Checkpoints: Validate at each phase with success criteria.
- Constitution Structure: Use markdown with sections like Overview, Goals, Tech Stack, Architecture Diagram, Rules/Behaviors, Tasks Breakdown, Success Criteria, Checkpoints, Deliverables.
- Make it comprehensive but concise (aim for 1500-2000 words).
- Ensure stateless architecture, MCP tools, natural language handling.
- Add multilingual support (English + Roman Urdu) as an optional enhancement, since user prefers Roman Urdu.

Provided Phase III Specification Document:
[Paste the entire Phase III document here – from "Phase III: Todo AI Chatbot" to the end, including all sections like Basic Level Functionality, Requirements, Technology Stack, Architecture, Database Models, Chat API Endpoint, MCP Tools Specification, Agent Behavior Specification, Conversation Flow, Natural Language Commands, Deliverables, OpenAI ChatKit Setup & Deployment, Key Architecture Benefits.]

Output ONLY the constitution.md file content in markdown format. Do not add extra explanations.
```

## Response Text
Updated the existing constitution.md file to incorporate AI chatbot functionality into the Todo Full-Stack Web Application, including new principles for AI integration, natural language processing, and MCP tools.

## Outcome Impact
Successfully created a new version (3.0.0) of the project constitution that extends the existing Todo application to include AI chatbot capabilities while maintaining all previous functionality.

## Tests Summary
None

## Files Summary
- .specify/memory/constitution.md: Updated to version 3.0.0 with AI chatbot integration principles

## Next Prompts
- Create Phase III specification document for the AI chatbot functionality
- Generate implementation plan for integrating AI chatbot with existing application
- Create detailed tasks for implementing MCP tools and natural language processing

## Reflection Note
The constitution successfully balances maintaining the existing application architecture while introducing AI enhancements, ensuring backward compatibility and security requirements are preserved.

## Failure Modes Observed
None

## Next Experiment to Improve Prompt Quality
N/A