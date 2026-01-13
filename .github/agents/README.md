# GitHub Copilot Agents

This directory contains custom agent configurations for GitHub Copilot. Each agent is specialized for specific tasks and workflows.

## Available Agents

### Plan Agent (`plan.agent.md`)

A specialized planning agent that researches codebases and creates actionable plans without implementing changes.

**Purpose**: 
- Research and analyze code/requirements using read-only tools
- Create concise, actionable plans for tasks
- Iterate on plans based on user feedback
- Hand off to implementation agents

**Key Features**:
- **Stopping Rules**: Prevents the agent from switching to implementation mode
- **Iterative Workflow**: Research → Draft Plan → Gather Feedback → Refine
- **Context Gathering**: Uses `runSubagent` for autonomous research
- **Structured Output**: Follows consistent plan template with steps and considerations

**When to Use**:
- Breaking down complex tasks into actionable steps
- Understanding codebases before making changes
- Creating architectural plans
- Researching implementation options

**Handoffs**:
- **Start Implementation**: Transfers to implementation agent to execute the plan
- **Open in Editor**: Creates an editable plan file for refinement

## Agent File Format

All agent files use YAML frontmatter with Markdown content:

```yaml
---
name: AgentName
description: Brief description of agent purpose
argument-hint: Hint for what arguments the agent expects
tools: ['tool1', 'tool2', ...]
handoffs:
  - label: Handoff Label
    agent: target_agent
    prompt: Handoff prompt
---

Agent instructions in Markdown...
```

## Creating New Agents

1. Create a new `.agent.md` file in this directory
2. Add YAML frontmatter with metadata (name, description, tools, handoffs)
3. Write clear agent instructions using XML-style tags for sections:
   - `<stopping_rules>` - Define what the agent should NOT do
   - `<workflow>` - Define the agent's operational process
   - `<guidelines>` - Provide specific instructions for the agent's role
4. Test the agent configuration with sample tasks
5. Document the agent in this README

## Best Practices

- **Single Responsibility**: Each agent should have one clear purpose
- **Explicit Boundaries**: Use stopping rules to prevent scope creep
- **Clear Handoffs**: Define how the agent transfers control to others
- **Structured Workflows**: Break down agent processes into numbered steps
- **Read-Only Research**: Planning agents should use non-destructive tools
- **User Feedback**: Build in checkpoints for user review and iteration
