# Workflow Engine

A lightweight, production-ready workflow orchestration engine built with FastAPI. Execute multi-step workflows with automatic state management, conditional branching, and iterative loops—all through clean REST APIs.

## Overview

This workflow engine enables you to build and execute agent-like workflows where each step is a Python function that reads from and writes to a shared state. The engine handles execution flow, state transitions, and conditional routing automatically.

**Key Capabilities:**
- Define workflows as directed graphs of Python functions
- Automatic state propagation between nodes
- Conditional branching based on state values
- Iterative loops with termination conditions
- Async execution with FastAPI
- RESTful API for workflow management and execution

## Features

### Core Functionality
- **Node-based Architecture**: Each workflow step is an isolated Python function (node) that operates on shared state
- **State Management**: Centralized state object that flows through the workflow, with automatic updates
- **Conditional Routing**: Branch execution paths based on state values or custom logic
- **Loop Support**: Continue workflow execution until specified conditions are met
- **Async Processing**: Built on FastAPI for high-performance async request handling

### API Design
- Create and manage workflow definitions
- Execute workflows with initial input state
- Query execution status and retrieve results
- Clean REST endpoints with proper HTTP semantics

## Technology Stack

- **Framework**: FastAPI
- **Language**: Python 3.8+
- **API Style**: RESTful
- **Execution Model**: Asynchronous


## Installation

```bash
# Clone the repository
git clone <repository-url>
cd workflow-engine

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

```bash
# Run the application
uvicorn app.main:app --reload

# The API will be available at http://localhost:8000
```

## API Endpoints

### Workflow Management

**Create Graph**
```http
POST /graph/create
Content-Type: application/json

{
  "graph_name": "code_review_agent",
  "nodes": {
    "extract": { "name": "extract", "func": "extract_functions" },
    "complexity": { "name": "complexity", "func": "check_complexity" },
    "issues": { "name": "issues", "func": "detect_issues" },
    "improve": { "name": "improve", "func": "suggest_improvements" }
  },
  "edges": {
    "extract": "complexity",
    "complexity": "issues",
    "issues": "improve"
  },
  "entrypoint": "extract"
}

```

**Run Graph**
```http
POST /graph/run
Content-Type: application/json

{
  "graph_id": "generated_graph_id",
  "initial_state": {
    "code": "def add(a,b): return a+b"
  }
}


```

**Get Run Status**
```http
GET /graph/state/{run_id}
```

## Example: Code Review Mini-Agent

The project includes a complete example workflow that demonstrates the engine's capabilities. This Code Review Agent analyzes code quality through multiple steps:

1. **Extract Functions**: Parse code and identify function definitions
2. **Check Complexity**: Calculate cyclomatic complexity for each function
3. **Detect Issues**: Identify code smells and potential problems
4. **Generate Suggestions**: Produce actionable improvement recommendations
5. **Calculate Score**: Compute overall quality score
6. **Loop Condition**: Continue refinement until quality threshold is reached

The workflow showcases:
- Multi-step processing with state accumulation
- Conditional branching based on quality metrics
- Iterative loops with termination criteria
- Real-world agent-like behavior



## Use Cases

This workflow engine is suitable for:

- **Data Processing Pipelines**: Multi-step data transformation workflows
- **Business Process Automation**: Automated decision-making workflows
- **Code Analysis Tools**: Static analysis and quality checking pipelines
- **Content Processing**: Document analysis and enrichment workflows
- **Integration Workflows**: Orchestrating multiple API calls with conditional logic
