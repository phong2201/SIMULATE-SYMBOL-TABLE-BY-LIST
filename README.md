# Assignment 3 - Simulate Symbol Table Using List

**Course**: Advanced Programming - CO2039
**University**: HCMC University of Technology - VNU-HCM
**Faculty**: Computer Science and Engineering
**Authors**: MEng. Tran Ngoc Bao Duy, BEng. Thi Khac Quan
**Date**: March 2025
**Version**: 1.1

---

## \:dart: Assignment’s Outcome

Upon completion, students will:

* Apply functional programming concepts.
* Use higher-order functions effectively.
* Model data with list-based structures.

---

## \:book: Introduction

A **symbol table** is a crucial data structure used by compilers to store information about identifiers (name, type, scope...).

This assignment simulates a symbol table using lists, focusing on the **semantic analysis** phase, such as:

* Checking if a variable is declared before use.
* Type compatibility in assignments.
* Scope resolution.

---

## \:inbox\_tray: Input Format

Input is a **list of command strings**, each on a single line. Commands simulate interaction with the symbol table.

---

## \:clipboard: Requirements

1. Download `initial.zip`, extract to get:

   * `main.py`
   * `Symbol.py`
   * `SymbolTable.py`
   * `TestSuite.py`
   * `TestUtils.py`

   \:no\_entry: **Do NOT rename these files.**

2. Modify **only** `SymbolTable.py`, ensuring:

   * Define function: `simulate(list_of_commands)`
   * Only these imports allowed:

     ```python
     from StaticError import *
     from Symbol import *
     from functools import *
     ```

3. Add **at least 50 test cases** in `TestSuite.py`.

---

## \:label: Symbol Structure

Each symbol must store:

* Identifier name (string)
* Type: `number` or `string`

---

## \:warning: Semantic Errors

Raise appropriate errors on invalid input or state:

* `Undeclared`
* `Redeclared`
* `UnclosedBlock` (with level)
* `UnknownBlock`
* `TypeMismatch`
* `InvalidInstruction`

Program must **stop immediately** on error.

---

## \:keyboard: Supported Commands

### `INSERT <identifier> <type>`

* Add symbol to current scope.
* Allowed types: `number`, `string`
* Example:

  ```
  INSERT x number
  INSERT y string
  ```

  Output:

  ```
  success
  success
  ```
* Error:

  ```
  INSERT x number
  INSERT x string
  ```

  Output:

  ```
  success
  Redeclared: INSERT x string
  ```

### `ASSIGN <identifier> <value>`

* Assign value to variable.
* `<value>` can be:

  * number constant: `123`
  * string constant: `'abc'`
  * another identifier
* Errors:

  * `Undeclared`
  * `TypeMismatch`
* Example:

  ```
  INSERT x number
  ASSIGN x 15
  ASSIGN x 'abc'
  ```

  Output:

  ```
  success
  success
  TypeMismatch: ASSIGN x 'abc'
  ```

### `BEGIN` / `END`

* Open and close a new block (like `{}` in C/C++).
* You can **redeclare** symbols in inner blocks.
* Errors:

  * `UnclosedBlock: <level>`
  * `UnknownBlock`
* Example:

  ```
  INSERT x number
  BEGIN
  INSERT x string
  END
  ```

  Output:

  ```
  success
  success
  ```

If missing END:

```
INSERT x number
BEGIN
INSERT x string
```

Output:

```
success
success
UnclosedBlock: 1
```

### `LOOKUP <identifier>`

* Search identifier from inner to outer block.
* Output: level of identifier if found.
* Error: `Undeclared`
* Example:

  ```
  INSERT x number
  BEGIN
  INSERT y string
  LOOKUP x
  LOOKUP y
  END
  ```

  Output:

  ```
  success
  success
  0
  1
  ```

### `PRINT`

* Print all **active** identifiers in the current scope in **forward order**.
* Format: `<name>//<level>`
* Example:

  ```
  INSERT x number
  BEGIN
  INSERT y number
  PRINT
  END
  ```

  Output:

  ```
  success
  success
  x//0 y//1
  ```

### `RPRINT`

* Like `PRINT` but in **reverse order**.
* Example:

  ```
  INSERT x number
  BEGIN
  INSERT y number
  RPRINT
  END
  ```

  Output:

  ```
  success
  success
  y//1 x//0
  ```

---

## \:lock: Coding Rules

* \:white\_check\_mark: Only `def` functions.
* \:no\_entry\_sign: No `class`, `global`, `for`, `while`, or mutation.
* \:white\_check\_mark: Use list comprehensions and higher-order functions.
* \:white\_check\_mark: Each variable must be assigned **once only**.

---

## \:outbox\_tray: Submission

Submit **ONLY**:

* `SymbolTable.py`
* `TestSuite.py`

Submit via the Assignment 3 portal. No late submissions accepted.

---

## \:scroll: Academic Regulations

* Do your own work.
* Do not copy or share code.
* Plagiarism will result in penalties.
* No test case disclosure after grading.

---

## \:calendar: Changelog

* Version 1.1 - March 2025 - Initial release

---
