# MiniLang Compiler

A BTech CSE 2nd-year System Programming PBL project: **Design and Implementation of a Mini Compiler for a Custom Programming Language**.

The project demonstrates these compiler phases:

1. Lexical analysis
2. Syntax analysis (recursive-descent parser)
3. Abstract Syntax Tree (AST) construction
4. Semantic analysis
5. Symbol table generation
6. Error detection and reporting
7. Three-Address Code (TAC) generation
8. Interactive web interface using Flask

## Features

- `int`, `float`, and `bool` data types
- Variable declarations
- Assignments
- Arithmetic expressions: `+ - * / %`
- Relational operators: `> < >= <= == !=`
- Logical operators: `&& || !`
- `if` / `else`
- `while`
- `print(...)`
- `true` / `false`
- `//` comments and `/* ... */` block comments
- Line/column-aware lexical, syntax, and semantic errors
- Symbol table
- AST visualization as JSON/tree text
- Three-Address Code generation with labels for control flow

## Project structure

```text
MiniLang-Compiler/
├── app.py
├── requirements.txt
├── README.md
├── compiler/
│   ├── __init__.py
│   ├── tokens.py
│   ├── errors.py
│   ├── lexer.py
│   ├── ast_nodes.py
│   ├── parser.py
│   ├── symbol_table.py
│   ├── semantic.py
│   └── tac.py
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── script.js
└── tests/
    ├── test_compiler.py
    ├── valid_programs/
    │   ├── basic.minilang
    │   └── control_flow.minilang
    └── invalid_programs/
        ├── lexical_error.minilang
        ├── syntax_error.minilang
        └── semantic_error.minilang
```

## MiniLang example

```text
program Demo {
    int a;
    int b;
    int result;

    a = 10;
    b = 20;
    result = a + b * 5;

    print(result);
}
```

## Run the web application

### Windows

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open the URL shown by Flask, normally:

`http://127.0.0.1:5000`

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Notes for PBL presentation

The application is intentionally educational. It implements a small language and stops at intermediate code generation rather than machine-code generation. It is suitable for demonstrating compiler phases in a college viva/project presentation.
