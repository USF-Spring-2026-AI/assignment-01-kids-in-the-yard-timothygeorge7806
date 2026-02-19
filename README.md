# AI Assignment 01 - Kids in the Yard

See assignment details on Canvas.

# Answers for Comparison Section

## 1. Which tool(s) did you use? 

I used Claude Code, which ran on Anthropic's latest reasoning model Opus 4.6.

## 2. If you used an LLM, what was your prompt to the LLM? 

First I ran /init, which allow Claude Code to analyze the assignment document and CSV files to understand the context of the assignment. Then, I gave Claude the following prompt: 

“Read the Assignment 1 PDF in the working directory. Implement all aspects of the project according to all requirements in the document, including the requirements for CS 562. Ensure that the output of your solution matches the format of the example given in the document. The relevant data files are present in the working directory.”

## 3. What differences are there between your implementation and the LLM?

The LLM’s implementation is organized differently; The LLM’s class ‘family_tree’ contains the tree building logic, file reading, and command line interaction. My implementation has the tree building logic and file reading in the PersonFactory class, with FamilyTree functioning as the driver. The LLM also iteratively constructed the tree via BFS while I used a recursive DFS-like algorithm. 

## 4. What changes would you make to your implementation in general based on suggestions from the LLM?

I would use a Set instead of a List to store visited nodes in my BFS traversals. I would also restructure my data storage structures to use dictionaries pointing to tuples instead of nested dictionaries. 

## 5. What changes would you refuse to make?

The LLM suggested I change my logic for determining the number of people in a tree by a given decade such that instead of rounding every year up to the nearest decade, I round down. This would be incorrect and would break my implementation of the logic.
