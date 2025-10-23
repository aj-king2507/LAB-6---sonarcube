# 🧠 Cognitive Complexity of Functions Should Not Be Too High (python:S3776)

## ⚙️ Adaptability Issue
**Status:** Not Focused

## 🧩 Maintainability
**Impact:** High

---

## ❓ Why Is This an Issue?

**Cognitive Complexity** measures how hard it is to understand the control flow of a unit of code. Code with high cognitive complexity is hard to **read, understand, test, and modify**.

> As a rule of thumb, high cognitive complexity is a sign that the code should be refactored into smaller, easier-to-manage pieces.

---

## 🔍 Which Syntax Impacts the Cognitive Complexity Score?

### Core Concepts

- Cognitive complexity is incremented each time the code **breaks normal linear reading flow**.
- This concerns, for example: **loops**, **conditionals**, **catches**, **switches**, **jumps to labels**, and **conditions mixing multiple operators**.
- **Each nesting level increases complexity.** The deeper you go, the harder it is to keep context in mind.
- **Method calls are free** (non-recursive). A well-picked method name summarizes multiple lines of code.
  - **Note:** Recursive calls **do** increment cognitive score.

📘 The computation method is detailed in SonarSource’s Cognitive Complexity spec.

---

## 📉 Potential Impact

Developers spend more time **reading and understanding** code than writing it. High cognitive complexity **slows down changes** and **increases maintenance cost**.

---

## 🛠️ How Can I Fix It?

### Parameters (SonarLint)
| Parameter | Description | Default |
|---|---|---|
| `threshold` | The maximum authorized complexity | **15** |

### Practical Refactors
- **Extract complex conditions** into a new function (especially when mixing operators).
- **Break down large functions** into smaller, single-responsibility functions.
- **Avoid deep nesting** by handling edge cases first and **returning early**.

---

## 🧩 Example 1 — Extract Complex Conditions

### ❌ Noncompliant Code
```python
def process_eligible_users(users):
    for user in users:             # +1 (for)
        if ((user.is_active and    # +1 (if) +1 (nested) +1 (multiple conditions)
            user.has_profile) or   # +1 (mixed operator)
            user.age > 18 ):
            user.process()
````

### ✅ Compliant Solution

Even if program-wide complexity doesn’t change, the **function’s** complexity is lower and easier to read.

```python
def process_eligible_users(users):
    for user in users:             # +1 (for)
        if is_eligible_user(user): # +1 (if) +1 (nested)
            user.process()

def is_eligible_user(user):
    return ((user.is_active and user.has_profile) or user.age > 18)  # +1 (multiple conditions) +1 (mixed operators)
```

---

## 🧩 Example 2 — Break Down Large Functions

### ❌ Noncompliant Code

```python
def process_user(user):
    if user.is_active():             # +1 (if)
        if user.has_profile():       # +1 (if) +1 (nested)
            ... # process active user with profile
        else:                        # +1 (else)
            ... # process active user without profile
    else:                            # +1 (else)
        if user.has_profile():       # +1 (if) +1 (nested)
            ... # process inactive user with profile
        else:                        # +1 (else)
            ... # process inactive user without profile
```

### ✅ Compliant Solution

```python
def process_user(user):
    if user.is_active():             # +1 (if)
        process_active_user(user)
    else:                            # +1 (else)
        process_inactive_user(user)

def process_active_user(user):
    if user.has_profile():           # +1 (if) +1 (nested)
        ... # process active user with profile
    else:                            # +1 (else)
        ... # process active user without profile

def process_inactive_user(user):
    if user.has_profile():           # +1 (if) +1 (nested)
        ... # process inactive user with profile
    else:                            # +1 (else)
        ... # process inactive user without profile
```

> Spreading logic across smaller functions removes deep nesting and lowers complexity per function.

---

## 🧩 Example 3 — Avoid Deep Nesting by Returning Early

### ❌ Noncompliant Code

```python
def calculate(data):
    if data is not None:  # +1 (if)
        total = 0
        for item in data: # +1 (for) +1 (nested)
            if item > 0:  # +1 (if) +2 (nested)
                total += item * 2
        return total
```

### ✅ Compliant Solution

```python
def calculate(data):
    if data is None:      # +1 (if)
        return None
    total = 0
    for item in data:     # +1 (for)
        if item > 0:      # +1 (if) +1 (nested)
            total += item * 2
    return total
```

> Returning early flattens control flow and reduces cognitive load.

---

## ⚠️ Pitfalls

* Ensure **unit tests** cover behavior before refactoring.
* Keep **business logic** unchanged; focus on structure and readability.


---

## 🧩 **2. S1481 — Unused Local Variables Should Be Removed**

# 🗑️ Unused Local Variables Should Be Removed (python:S1481)

## 🧭 Intentionality Issue
**Status:** Not Clear

## 🧩 Maintainability
**Impact:** High

---

## ❓ Why Is This an Issue?
An **unused local variable** is declared but never used in its scope. It’s dead code that adds noise and confusion, and can hint at **bugs** or **incomplete implementations**.

### Potential Impact
- **Decreased readability** and unnecessary complexity  
- **Misunderstanding** by other readers  
- **Bug potential** (forgotten usage)  
- **Maintenance burden**  
- Possible **memory waste** on some runtimes/compilers

### Exceptions
The underscore `_` is allowed for intentionally unused variables, e.g.:
```python
for _ in range(10):
    do_something()

username, login, _ = auth
do_something_else(username, login)
````

---

## 🛠️ How Can I Fix It?

### Parameters (SonarLint)

| Parameter | Description                                | Default          |       |        |           |
| --------- | ------------------------------------------ | ---------------- | ----- | ------ | --------- |
| `regex`   | Regex to identify variable names to ignore | `(*[a-zA-Z0-9*]* | dummy | unused | ignored)` |

### Fix

* Verify the variable **isn’t needed** (no incomplete implementation).
* **Remove** the variable or **use** it meaningfully.
* For intentional discards, **rename to `_`** (or match the ignore regex).

---

## 🧩 Examples

### ❌ Noncompliant

```python
def hello(name):
    message = "Hello " + name  # Noncompliant - message is unused
    print(name)

for i in range(10):  # Noncompliant - i is unused
    foo()
```

### ✅ Compliant

```python
def hello(name):
    message = "Hello " + name
    print(message)

for _ in range(10):
    foo()
```

---

## 🧩 **3. S6396 — Superfluous Curly Brace Quantifiers Should Be Avoided**

# 🧱 Superfluous Curly Brace Quantifiers Should Be Avoided (python:S6396)

## 🧭 Intentionality Issue
**Status:** Not Clear

## 🧩 Maintainability
**Impact:** High

---

## ❓ Why Is This an Issue?
Curly brace quantifiers control how many times a preceding token occurs: `{n}`, `{n,m}`, `{n,}`.  
Sometimes they are **superfluous**, and removing them **improves readability** without changing behavior.

### Flagged Cases
- `{1,1}` or `{1}` — matches exactly once (same as omitting the quantifier).  
- `{0,0}` or `{0}` — matches zero times (same as **removing** the token).

---

## 🧩 Examples

### ❌ Noncompliant
```python
r"ab{1,1}c"
r"ab{1}c"
r"ab{0,0}c"
r"ab{0}c"
````

### ✅ Compliant

```python
r"abc"
r"ac"
```

---

## 🧩 **4. S6353 — Regular Expression Quantifiers and Character Classes Should Be Used Concisely**

# ✂️ Regular Expression Quantifiers and Character Classes Should Be Used Concisely (python:S6353)

## 🧭 Intentionality Issue
**Status:** Not Clear

## 🧩 Maintainability
**Impact:** High

---

## ❓ Why Is This an Issue?
Regex offers **shortcuts** for common classes and quantifiers. Using concise forms makes patterns **shorter and easier to maintain**.

### Prefer These Shortcuts
- `\\d` for `[0-9]`, `\\D` for `[^0-9]`
- `\\w` for `[A-Za-z0-9_]`, `\\W` for `[^A-Za-z0-9_]`
- `.` for “any char” (instead of `[\\w\\W]`, `[\\d\\D]`, `[\\s\\S]` with `s` flag)
- `x?` for `x{0,1}`, `x*` for `x{0,}`, `x+` for `x{1,}`, `x{N}` for `x{N,N}`

---

## 🧩 Examples

### ❌ Noncompliant
```python
r"[0-9]"        # same as r"\\d"
r"[^0-9]"       # same as r"\\D"
r"[A-Za-z0-9_]" # same as r"\\w"
r"[\\w\\W]"     # same as r"\\."
r"a{0,}"        # same as r"a*"
````

### ✅ Compliant

```python
r"\\d"
r"\\D"
r"\\w"
r"."
r"a*"
```

---

## 🧩 **5. S1764 — Identical Expressions Should Not Be Used on Both Sides of a Binary Operator**


# ♻️ Identical Expressions Should Not Be Used on Both Sides of a Binary Operator (python:S1764)

## 🧭 Intentionality Issue
**Status:** Not Logical

## ✅ Reliability
**Impact:** High

---

## ❓ Why Is This an Issue?
Using the **same value** on both sides of a binary operator is almost always a **mistake** or **wasteful**.  
It can mask copy/paste errors or yield predictable, pointless results.

> For `NaN` checks, use `math.isnan(x)` instead of `x != x`.

### ❌ Noncompliant
```python
if a == a:
    work()

if a != a:
    work()

if a == b and a == b:
    work()

if a == b or a == b:
    work()

j = 5 / 5
k = 5 - 5
```

### ✅ Exceptions

* Bit shifting literal: `1 << 1`

---

## ✅ What To Do

* Remove duplicated comparisons.
* Compare different operands or **simplify** the expression.
* Replace `x != x` with **proper NaN detection**.

