import ast
import os
import re
import sys
from typing import List, Tuple, Dict, Any

# -------------------------
# Student marks functionality
# -------------------------
def student_module():
    print("=== Software Security Module Marks Entry ===")
    
    coursework_marks = []
    total_coursework = 0
    
    # Input for 4 coursework
    for i in range(1, 5):
        while True:
            try:
                mark = float(input(f"Enter marks for Coursework {i} (out of 25): "))
                if 0 <= mark <= 25:
                    coursework_marks.append(mark)
                    total_coursework += mark
                    break
                else:
                    print(" Invalid input. Please enter a mark between 0 and 25.")
            except ValueError:
                print("Please enter a valid number.")
    
    # Input for exam
    while True:
        try:
            exam_mark = float(input("Enter marks for Exam (out of 100): "))
            if 0 <= exam_mark <= 100:
                break
            else:
                print("Invalid input. Please enter a mark between 0 and 100.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Calculations
    total_marks = total_coursework + exam_mark
    max_marks = (4 * 25) + 100  # 200 total
    percentage = (total_marks / max_marks) * 100
    
    # Output
    print("\n=== Results ===")
    for i, mark in enumerate(coursework_marks, start=1):
        print(f"Coursework {i}: {mark}/25")
    print(f"Exam: {exam_mark}/100")
    print(f"Total Marks: {total_marks}/{max_marks}")
    print(f"Percentage: {percentage:.2f}%")
    print("====================\n")

# -------------------------
# Basic SAST scanner
# -------------------------
# Issue dict format: {"file": str, "lineno": int, "message": str, "severity": "LOW|MEDIUM|HIGH", "rule": str}

def scan_python_source_for_issues(source: str, filename: str) -> List[Dict[str, Any]]:
    issues: List[Dict[str, Any]] = []
    try:
        tree = ast.parse(source, filename=filename)
    except SyntaxError as e:
        issues.append({
            "file": filename,
            "lineno": getattr(e, "lineno", 0),
            "message": f"SyntaxError when parsing file: {e}",
            "severity": "LOW",
            "rule": "parse-error"
        })
        return issues

    # Helper: Visit calls and names
    class Detector(ast.NodeVisitor):
        def visit_Call(self, node: ast.Call):
            # function name resolution (attr or name)
            func_name = ""
            if isinstance(node.func, ast.Name):
                func_name = node.func.id
            elif isinstance(node.func, ast.Attribute):
                # e.g., subprocess.call, cur.execute
                func_name = node.func.attr

                # also check for module.func by checking value.id if present
                if isinstance(node.func.value, ast.Name):
                    full = f"{node.func.value.id}.{node.func.attr}"
                    # Detect subprocess.run/call with shell=True
                    if node.func.value.id in ("subprocess",) and node.func.attr in ("call", "Popen", "run"):
                        # check keywords for shell=True
                        for kw in node.keywords:
                            if kw.arg == "shell" and isinstance(kw.value, ast.Constant) and kw.value.value is True:
                                issues.append({
                                    "file": filename,
                                    "lineno": node.lineno,
                                    "message": f"Use of subprocess.{node.func.attr} with shell=True (risky).",
                                    "severity": "HIGH",
                                    "rule": "subprocess-shell-true"
                                })

            # Detect direct eval/exec usage
            if func_name in ("eval", "exec"):
                issues.append({
                    "file": filename,
                    "lineno": node.lineno,
                    "message": f"Use of {func_name}() — executing dynamic code can lead to remote code execution.",
                    "severity": "HIGH",
                    "rule": f"use-{func_name}"
                })

            # Detect pickle loads/loads by name or attribute
            if func_name in ("loads", "load") and isinstance(node.func, ast.Attribute):
                # e.g., pickle.loads
                if isinstance(node.func.value, ast.Name) and node.func.value.id == "pickle":
                    issues.append({
                        "file": filename,
                        "lineno": node.lineno,
                        "message": "Use of pickle.load(s) — untrusted input deserialization can lead to remote code execution.",
                        "severity": "HIGH",
                        "rule": "pickle-deserialization"
                    })

            # Detect hashlib.md5 usage (weak hash)
            if isinstance(node.func, ast.Attribute):
                if isinstance(node.func.value, ast.Name) and node.func.value.id == "hashlib" and node.func.attr == "md5":
                    issues.append({
                        "file": filename,
                        "lineno": node.lineno,
                        "message": "Use of hashlib.md5 — MD5 is cryptographically broken/weak; prefer SHA-256 or better.",
                        "severity": "MEDIUM",
                        "rule": "weak-hash-md5"
                    })

            # Detect SQL execution where query is constructed via BinOp (string concatenation) or f-string/JoinedStr
            if isinstance(node.func, ast.Attribute):
                if node.func.attr in ("execute", "executemany"):
                    if node.args:
                        first_arg = node.args[0]
                        if isinstance(first_arg, ast.BinOp):  # string concatenation
                            issues.append({
                                "file": filename,
                                "lineno": node.lineno,
                                "message": "Possible SQL query built via string concatenation passed to execute(); risk of SQL injection.",
                                "severity": "HIGH",
                                "rule": "sql-concat-execute"
                            })
                        elif isinstance(first_arg, ast.JoinedStr):  # f-string
                            issues.append({
                                "file": filename,
                                "lineno": node.lineno,
                                "message": "f-string used to build SQL query passed to execute(); prefer parameterized queries.",
                                "severity": "HIGH",
                                "rule": "sql-fstring-execute"
                            })
                        elif isinstance(first_arg, ast.Call) and isinstance(first_arg.func, ast.Attribute) and getattr(first_arg.func, "attr", "") == "format":
                            issues.append({
                                "file": filename,
                                "lineno": node.lineno,
                                "message": "String.format used to build SQL queries passed to execute(); prefer parameterized queries.",
                                "severity": "HIGH",
                                "rule": "sql-format-execute"
                            })

            # Detect os.system usage when referenced as a call
            if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name) and node.func.value.id == "os" and node.func.attr == "system":
                issues.append({
                    "file": filename,
                    "lineno": node.lineno,
                    "message": "Use of os.system — prefer subprocess.run with arguments list and without shell=True.",
                    "severity": "MEDIUM",
                    "rule": "os-system-call"
                })

            # Detect subprocess.call/run with shell=True if called as Name (rare), e.g., from subprocess import run; run(..., shell=True)
            if isinstance(node.func, ast.Name) and node.func.id in ("run", "call", "Popen"):
                for kw in node.keywords:
                    if kw.arg == "shell" and isinstance(kw.value, ast.Constant) and kw.value.value is True:
                        issues.append({
                            "file": filename,
                            "lineno": node.lineno,
                            "message": f"Use of {node.func.id} with shell=True (risky).",
                            "severity": "HIGH",
                            "rule": "subprocess-shell-true"
                        })

            # Detect use of random.* where it's likely used for secrets (heuristic: variable names or function names)
            # Hard to be certain via AST call alone; flag calls to random.random(), random.randint, etc.
            if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name) and node.func.value.id == "random":
                if node.func.attr in ("random", "randint", "choice", "randrange"):
                    issues.append({
                        "file": filename,
                        "lineno": node.lineno,
                        "message": f"Use of random.{node.func.attr} — not suitable for cryptographic secrets. Use secrets module instead.",
                        "severity": "MEDIUM",
                        "rule": "insecure-random"
                    })

            self.generic_visit(node)

        def visit_Import(self, node: ast.Import):
            # Detect "import pickle" usage — if present, we may check calls above
            for alias in node.names:
                if alias.name == "pickle":
                    # low-level info; actual dangerous calls checked elsewhere
                    pass
            self.generic_visit(node)

        def visit_ImportFrom(self, node: ast.ImportFrom):
            # Detect from pickle import loads
            if node.module == "pickle":
                for alias in node.names:
                    if alias.name in ("load", "loads"):
                        issues.append({
                            "file": filename,
                            "lineno": node.lineno,
                            "message": f"Importing pickle.{alias.name} — deserializing untrusted data is risky.",
                            "severity": "HIGH",
                            "rule": "pickle-import"
                        })
            self.generic_visit(node)

    Detector().visit(tree)

    # Regex-based source checks (for hard-coded secrets, http usage, etc.)
    # Hard-coded credential heuristic: variable names containing password/secret/key/token assigned to string literal
    secret_pattern = re.compile(r'(?i)\b(password|passwd|pwd|secret|token|apikey|api_key|aws_secret|private_key)\b')
    assign_string_pattern = re.compile(r'(?P<var>\b[a-zA-Z_][a-zA-Z0-9_]*\b)\s*=\s*(?P<value>["\']{1}.*?["\']{1})')
    for m in assign_string_pattern.finditer(source):
        var = m.group("var")
        val = m.group("value")
        if secret_pattern.search(var):
            # Avoid false positives on small values like "", but still flag
            issues.append({
                "file": filename,
                "lineno": source[:m.start()].count("\n") + 1,
                "message": f"Hard-coded secret-like variable '{var}' assigned a string literal ({val}). Avoid hard-coding credentials; use environment variables or a secret manager.",
                "severity": "HIGH",
                "rule": "hardcoded-secret"
            })

    # Detect plaintext HTTP usage in obvious places
    for lineno, line in enumerate(source.splitlines(), start=1):
        if "http://" in line and "http://" in line:
            issues.append({
                "file": filename,
                "lineno": lineno,
                "message": "Plain HTTP URL found. Use HTTPS to protect data in transit.",
                "severity": "LOW",
                "rule": "insecure-transport-http"
            })

    return issues

def sast_scan_path(path: str) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    if os.path.isfile(path):
        if path.endswith(".py"):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    src = f.read()
                results.extend(scan_python_source_for_issues(src, path))
            except Exception as e:
                results.append({
                    "file": path,
                    "lineno": 0,
                    "message": f"Error reading file: {e}",
                    "severity": "LOW",
                    "rule": "io-error"
                })
        else:
            results.append({
                "file": path,
                "lineno": 0,
                "message": "Skipping non-Python file.",
                "severity": "LOW",
                "rule": "skip-nonpy"
            })
    elif os.path.isdir(path):
        for root, _, files in os.walk(path):
            for fname in files:
                if fname.endswith(".py"):
                    full = os.path.join(root, fname)
                    try:
                        with open(full, "r", encoding="utf-8") as f:
                            src = f.read()
                        results.extend(scan_python_source_for_issues(src, full))
                    except Exception as e:
                        results.append({
                            "file": full,
                            "lineno": 0,
                            "message": f"Error reading file: {e}",
                            "severity": "LOW",
                            "rule": "io-error"
                        })
    else:
        results.append({
            "file": path,
            "lineno": 0,
            "message": "Path does not exist.",
            "severity": "LOW",
            "rule": "path-not-exist"
        })
    return results

def print_sast_report(issues: List[Dict[str, Any]]):
    if not issues:
        print("No issues found by the basic SAST scanner.")
        return

    # Group by file
    issues_by_file: Dict[str, List[Dict[str, Any]]] = {}
    for it in issues:
        issues_by_file.setdefault(it["file"], []).append(it)

    print("\n=== SAST Scan Report ===")
    for fname, its in issues_by_file.items():
        print(f"\nFile: {fname}")
        for it in sorted(its, key=lambda x: x.get("lineno", 0)):
            lineno = it.get("lineno", "?")
            sev = it.get("severity", "LOW")
            rule = it.get("rule", "")
            msg = it.get("message", "")
            print(f"  [{sev}] line {lineno}: {msg}  (rule: {rule})")
    print("\nEnd of report.\n")

# -------------------------
# CLI wrapper
# -------------------------
def main_menu():
    while True:
        print("Choose an option:")
        print("1) Enter student marks")
        print("2) Run basic SAST scan on a Python file/directory")
        print("3) Exit")
        choice = input("Option: ").strip()
        if choice == "1":
            student_module()
        elif choice == "2":
            path = input("Enter Python file path or directory to scan: ").strip()
            if not path:
                print("Please provide a path.")
                continue
            issues = sast_scan_path(path)
            print_sast_report(issues)
        elif choice == "3":
            print("Goodbye.")
            break
        else:
            print("Invalid option. Choose 1, 2 or 3.")

if __name__ == "__main__":
    main_menu()
