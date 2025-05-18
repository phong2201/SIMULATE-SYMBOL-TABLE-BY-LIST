# Assignment 3 - Simulate Symbol Table Using List

**Course**: Advanced Programming - CO2039  
**University**: HCMC University of Technology - VNU-HCM  
**Faculty**: Computer Science and Engineering  
**Authors**: MEng. Tran Ngoc Bao Duy, BEng. Thi Khac Quan  
**Date**: March 2025  
**Version**: 1.1

---

## 🎯 Assignment’s Outcome

Upon completion, students will:
- Apply functional programming concepts.
- Use higher-order functions effectively.
- Model data with list-based structures.

---

## 📚 Introduction

A **symbol table** is a crucial data structure used by compilers to store information about identifiers (name, type, scope...).

This assignment simulates a symbol table using lists, focusing on the **semantic analysis** phase, such as:
- Checking if a variable is declared before use.
- Type compatibility in assignments.
- Scope resolution.

---

## 📥 Input Format

Input is a **list of command strings**, each on a single line. Commands simulate interaction with the symbol table.

---

## 📌 Requirements

1. Download `initial.zip`, extract to get:
   - `main.py`
   - `Symbol.py`
   - `SymbolTable.py`
   - `TestSuite.py`
   - `TestUtils.py`
   
   🔴 **Do NOT rename these files.**

2. Modify **only** `SymbolTable.py`, ensuring:
   - Define function: `simulate(list_of_commands)`
   - Only these imports allowed:
     ```python
     from StaticError import *
     from Symbol import *
     from functools import *
     ```

3. Add **at least 50 test cases** in `TestSuite.py`.

---

## 🔠 Symbol Structure

Each symbol must store:
- Identifier name (string)
- Type: `number` or `string`

---

## ❗ Semantic Errors

Raise appropriate errors on invalid input or state:
- `Undeclared`
- `Redeclared`
- `UnclosedBlock` (with level)
- `UnknownBlock`
- `TypeMismatch`
- `InvalidInstruction`

Program must **stop immediately** on error.

---

## 🔣 Supported Commands

### `INSERT <identifier> <type>`

- Add symbol to current scope.
- Allowed types: `number`, `string`
- Example:
INSERT x number
INSERT y string
➤ Output:
success
success
