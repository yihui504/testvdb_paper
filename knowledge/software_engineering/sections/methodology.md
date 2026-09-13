# Writing a Good SE Approach/Methodology

## Core Principle
Someone should be able to reimplement your approach from the paper. Design > implementation details.

## What Makes It Good
### Architecture Overview First: Lead with a figure. Walk through workflow before details. Give readers a mental map.
### Component-by-Component: Each major component gets its own subsection. For each: WHAT, HOW, WHY. Use running examples.
### Design Justification: Explain WHY key decisions. "We chose X over Y because...". Acknowledge tradeoffs.
### Appropriate Abstraction: Focus on approach, not implementation. Pseudocode for complex algorithms. Save tool-specific details.

## Language Patterns
**Overview**: "Figure 1 shows the overall architecture of [TOOL]...", "Our approach consists of three phases: ..."
**Component description**: "The first component, X, is responsible for...", "The key challenge here is... We address this by..."
**Design decisions**: "We chose X over Y because...", "An alternative would be Z, but..."
**Running example**: "Consider the code snippet in Figure 2...", "Continuing our running example..."

## Common Pitfalls
- No overview figure (readers get lost)
- Too much implementation, too little insight
- Missing justification for design choices
- Assuming readers know your specific domain
