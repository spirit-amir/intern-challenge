# How to Submit Your Solutions

Welcome to your personal repository for the coding challenge! All your work will be done here.

---

## 🚀 The Workflow in 5 Steps

### **Step 1: Clone Your Personal Repository**
Clone this repository to your local machine using the URL from the "<> Code" button.

```bash
git clone https://github.com/YOUR_ORG/intern-jane-challenge.git
```

---

### **Step 2: Choose a Problem**
Navigate to the `/problems` directory. Each sub-folder (e.g., `/problems/s1/lec1/p1/`) contains a `problem.md` file with the challenge description.

---

### **Step 3: Create Your Solution File**
This step is now simpler! Inside the `/solutions` directory, create your solution file. The filename **must** match the problem's folder name exactly, with the correct language extension.

**Example:**
To solve the `p1` problem in Python, your file path must be:
```
solutions/s1_lec1_p1.py
```

**Supported Languages & Extensions:**
| Language  | Extension |
|-----------|-----------|
| Python    | `.py`     |
| C++       | `.cpp`    |
| Java      | `.java`   |
| JavaScript| `.js`     |

---

### **Step 4: Write and Push Your Code**
Write your solution. When ready, commit and push your file:

```bash
git add solutions/s1_lec1_p1.py
git commit -m "feat: Add solution for step 1, lec 1, p1"
git push
```

---

### **Step 5: Check Your Results**
Pushing your code automatically triggers the testing system. Go to the **"Actions"** tab of this repository to see your results:
- ✅ **All tests passed!**
- ❌ **One or more tests failed.**

Click on the workflow for a detailed log.

---

## 🔄 Getting New Problems or Updates
If new problems are added, pull them from the main template repository. You only need to set this up once:

```bash
# 1. Add the template repo as a remote called "upstream"
git remote add upstream https://github.com/YOUR_ORG/intern-challenge-template.git

# 2. Pull updates whenever needed
git pull upstream main --allow-unrelated-histories
```

---

**Good luck!** 🌟
```
