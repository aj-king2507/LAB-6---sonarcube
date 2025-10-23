# 🧠 Cognitive Complexity (Rule: python:S3776)

## ⚠️ Issue Summary
**Cognitive Complexity of functions should not be too high**

| Category | Impact Level |
|-----------|---------------|
| Adaptability | ❌ Not Focused |
| Maintainability | 🔺 High |

---

## 🧩 Why is this an Issue?

**Cognitive Complexity** measures how hard it is to understand a unit of code’s control flow.  
High complexity makes code **difficult to read, test, and maintain** — increasing long-term costs.

> 🧠 *“High cognitive complexity is a sign the code should be refactored into smaller, easier-to-manage pieces.”*

---

## 🧮 How the Score Works

Cognitive complexity increases whenever code **breaks the normal linear reading flow**.

| Structure | Effect on Complexity |
|------------|----------------------|
| `if`, `for`, `while`, `try`, `catch`, `switch`, etc. | +1 each |
| Nesting inside other structures | +1 per level |
| Multiple logical operators in conditions (`and`, `or`) | +1 |
| Recursive function calls | +1 |
| Method calls (non-recursive) | Free (no penalty) |

The deeper the nesting, the harder the mental load.

---

## 📉 Potential Impact

- Developers spend more time **understanding** than writing code.  
- Slower debugging, harder refactoring.  
- Higher **maintenance cost** over time.

---

## 🛠️ How to Fix It

### 1️⃣ Extract Complex Conditions

**Problem**
```python
def process_eligible_users(users):
    for user in users:  # +1 (for)
        if ((user.is_active and    # +1 (if) +1 (nested) +1 (multiple conditions)
            user.has_profile) or   # +1 (mixed operator)
            user.age > 18):
            user.process()

