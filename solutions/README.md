# How to Submit Your Solutions

Welcome to the challenge! This guide will walk you through the process of submitting your code for automated evaluation. Follow these steps carefully to ensure your submissions are tested correctly.

### The Workflow in 5 Steps

**Step 1: Clone the Repository**
If you haven't already, clone this repository to your local machine.
```bash
git clone https://github.com/YOUR_USERNAME/intern-challenge.git
```

**Step 2: Choose a Problem**
Navigate to the `/problems` directory. Each sub-folder (e.g., `/problems/1-two-sum/`) contains a `problem.md` file with the challenge description.

**Step 3: Create Your Solution File (Most Important Step!)**
This is the critical part. You must follow this structure **exactly**.

1.  Inside this `/solutions` directory, create a new folder with your exact GitHub username (e.g., `solutions/jane-doe/`).
2.  Inside your username folder, create your solution file. The filename **must match the problem's folder name exactly**, with the correct language extension.

For example, if your username is `jane-doe` and you are solving the `1-two-sum` problem in Python, your file path must be:
`solutions/jane-doe/1-two-sum.py`

**Supported Languages & Extensions:**
*   Python: `.py`
*   C++: `.cpp`
*   Java: `.java`
*   JavaScript: `.js`
*   C: `.c`

**Step 4: Write and Push Your Code**
Write your solution. When you are ready to submit, commit and push your file.

```bash
# Navigate to the repository root
git add solutions/jane-doe/1-two-sum.py
git commit -m "feat: Add solution for 1-two-sum"
git push
```

**Step 5: Check Your Results**
Pushing your code automatically triggers our testing system.

*   Go to the **"Actions"** tab of this repository on GitHub.
*   You will see your commit message listed as a workflow.
*   A ✅ means all tests passed! A ❌ means one or more tests failed.
*   Click on the workflow run to see a detailed log of which test cases passed or failed. This is your feedback!

### Crucial Rules
*   **One File Per Problem:** Do not put multiple solutions in one file.
*   **Standard I/O:** Your code **must** read from Standard Input (like `input()` in Python or `cin` in C++) and write to Standard Output (like `print()` or `cout`). Do not read from or write to files.
*   **File Naming:** The solution filename must match the problem folder name (e.g., `1-two-sum`), not the problem title ("Two Sum").

Good luck!
```
