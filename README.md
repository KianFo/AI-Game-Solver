AI Game Solver – Search-Based Game Engine

This project implements an AI agent that plays and solves a game using a variety of classical search algorithms.
It was developed as part of the university Artificial Intelligence course and demonstrates how state-space search can be used to analyze, navigate, and complete a game environment.

The AI system models the game board, generates valid actions, evaluates states, and searches for the optimal (or valid) path to reach the goal.

Key Features

Fully automated solver for a custom game

Multiple search algorithms:

Breadth-First Search (BFS)

Depth-First Search (DFS)

Uniform Cost Search (UCS)

Greedy Best-First Search

A* Search with heuristics

Clean separation between the game engine and search logic

Support for reading game maps / levels

Step-by-step simulation of the AI’s decisions

Search result visualization (via notebook)

Game Mechanics

The game board is parsed from input files.

Each state corresponds to a specific configuration of the player, environment, and obstacles.

Successor functions generate allowed moves.

The AI explores the state space to find:

A valid solution

The optimal-cost solution

The shortest path (depending on algorithm)
