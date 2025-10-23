# 🧠 Cognitive Complexity of Functions Should Not Be Too High (python:S3776)

---

## ⚙️ Adaptability Issue
**Status:** Not Focused

## 🧩 Maintainability
**Impact:** High

---

## ❓ Why Is This an Issue?

**Cognitive Complexity** measures how difficult it is to understand the control flow of a unit of code.  
Functions with high cognitive complexity are **hard to read, test, and modify**.

> As a rule of thumb, high cognitive complexity is a sign that the code should be refactored into smaller, easier-to-manage pieces.

---

## 🔍 Which Syntax Impacts the Cognitive Complexity Score?

### Core Concepts

- **Cognitive Complexity increases** each time code breaks normal linear reading flow.
- This includes:
  - Loop structures (`for`, `while`)
  - Conditionals (`if`, `else`)
  - Exception handlers (`try`, `catch`)
  - Switches or case structures
  - Jumps to labels
  - Conditions mixing multiple logical operators (`and`, `or`)
- **Each nesting level** adds extra complexity.
- The deeper the nesting, the harder it becomes to track context.

### Method Calls
- **Method calls are free.**
- A well-named method summarizes logic clearly, improving readability.
- Recursive calls **do** increase complexity.

📘 *For the full computation method, refer to the official PDF linked in the resources.*

---

## 📉 What Is the Potential Impact?

Developers spend **more time reading and understanding code** than writing it.  
High cognitive complexity:
- Slows down code comprehension  
- Increases maintenance costs  
- Makes testing and debugging more difficult  

---

## 🛠️ How Can I Fix It?

**Default Parameter Setting**

| Parameter | Description | Default |
|------------|-------------|----------|
| `threshold` | The maximum authorized complexity | **15** |

---

### 💡 Reducing Cognitive Complexity

Refactoring for lower complexity can be challenging — here are some practical tips:

1. **Extract complex conditions into new functions**  
   - Mixed operators in conditions increase complexity.  
   - Moving them into a helper function with a clear name reduces cognitive load.

2. **Break down large functions**  
   - Large functions are hard to read and maintain.  
   - Each function should handle a **single responsibility**.

3. **Avoid deep nesting by returning early**  
   - Handle exceptional cases first.  
   - Use early returns to simplify flow.

---

## 🧩 Example 1 — Extract Complex Conditions into a New Function

#### ❌ Noncompliant Code
```python
def process_eligible_users(users):
    for user in users:             # +1 (for)
        if ((user.is_active and    # +1 (if) +1 (nested) +1 (multiple conditions)
            user.has_profile) or   # +1 (mixed operator)
            user.age > 18 ):
            user.process()
```

#### ✅ Compliant Solution

Even though the total program complexity remains similar, this version is **easier to read and maintain**.

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

#### ❌ Noncompliant Code

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

#### ✅ Compliant Solution

This version spreads the complexity across smaller functions — no deep nesting required.

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

> Breaking large functions into smaller ones spreads complexity and makes each function easier to reason about.

---

## 🧩 Example 3 — Avoid Deep Nesting by Returning Early

#### ❌ Noncompliant Code

```python
def calculate(data):
    if data is not None:  # +1 (if)
        total = 0
        for item in data: # +1 (for) +1 (nested)
            if item > 0:  # +1 (if) +2 (nested)
                total += item * 2
        return total
```

#### ✅ Compliant Solution

Flattening the condition reduces cognitive complexity from **6 → 4**.

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

> Returning early simplifies control flow and improves readability.

---

## ⚠️ Pitfalls

Before refactoring:

* Ensure **unit tests** fully cover existing logic.
* Keep the **business logic unchanged** — focus on structural improvements.

---

## 🧾 Configuration in SonarLint

| Parameter   | Description                             | Default |
| ----------- | --------------------------------------- | ------- |
| `threshold` | Maximum authorized cognitive complexity | **15**  |

> You can modify this in VS Code under **Settings → SonarLint: Rules → python:S3776 → Threshold**.
> *(In connected mode, server-side configuration overrides local settings.)*

---

## 📚 More Info

* [SonarQube Cognitive Complexity Specification (PDF)](https://www.sonarsource.com/docs/CognitiveComplexity.pdf)
* [SonarLint for VS Code Documentation](https://docs.sonarsource.com/sonarlint/vscode/)
* [Python Rule python:S3776 – Cognitive Complexity](https://rules.sonarsource.com/python/RSPEC-3776/)


