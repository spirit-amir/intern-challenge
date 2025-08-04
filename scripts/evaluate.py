import os
import sys
import requests
import json
import time
import base64

# --- Configuration ---
# Passed from the GitHub Actions workflow
# The solution file to be tested, e.g., "solutions/intern-username/1-two-sum.py"
SOLUTION_FILE_PATH = sys.argv[1] 
# The directory where the private testcases are checked out
TESTCASES_DIR = "private-repo/testcases"
JUDGE0_API_KEY = os.environ.get("JUDGE0_API_KEY")
JUDGE0_API_HOST = "judge0-ce.p.rapidapi.com"

# Mapping from file extension to Judge0 Language ID
# You can find more IDs here: https://judge0.com/
LANGUAGE_IDS = {
    ".py": 71,   # Python 3.8
    ".js": 63,   # JavaScript (Node.js)
    ".java": 62, # Java (OpenJDK 13)
    ".cpp": 54,  # C++ (GCC 9.2.0)
}

# --- Helper Functions ---

def get_problem_name_and_lang(solution_path):
    """Extracts problem name and language ID from the file path."""
    parts = solution_path.split(os.sep)
    filename = parts[-1]
    problem_name = os.path.splitext(filename)[0]
    file_ext = os.path.splitext(filename)[1]
    
    if file_ext not in LANGUAGE_IDS:
        print(f"!! Error: Unsupported file extension '{file_ext}'.")
        sys.exit(1)
        
    return problem_name, LANGUAGE_IDS[file_ext]

def get_test_cases(problem_name):
    """Finds all input/output file pairs for a given problem."""
    problem_test_dir = os.path.join(TESTCASES_DIR, problem_name)
    if not os.path.isdir(problem_test_dir):
        print(f"!! Error: Cannot find test case directory for problem '{problem_name}'.")
        print(f"!! Searched in: {problem_test_dir}")
        sys.exit(1)
    
    test_cases = []
    files = sorted(os.listdir(problem_test_dir))
    inputs = [f for f in files if f.startswith('input') and f.endswith('.txt')]
    
    for input_file in inputs:
        output_file = input_file.replace('input', 'output')
        if output_file in files:
            test_cases.append({
                "input": os.path.join(problem_test_dir, input_file),
                "output": os.path.join(problem_test_dir, output_file)
            })
    return test_cases

def submit_to_judge0(source_code, language_id, stdin):
    """Submits the code and input to the Judge0 API and returns a submission token."""
    url = f"https://{JUDGE0_API_HOST}/submissions?base64_encoded=true&wait=false"
    
    payload = {
        "language_id": language_id,
        "source_code": base64.b64encode(source_code.encode()).decode(),
        "stdin": base64.b64encode(stdin.encode()).decode(),
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": JUDGE0_API_KEY,
        "X-RapidAPI-Host": JUDGE0_API_HOST
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()['token']
    except requests.exceptions.RequestException as e:
        print(f"!! API Error during submission: {e}")
        print(f"!! Response body: {response.text}")
        return None

def get_judge0_result(token):
    """Polls the Judge0 API for the result using the submission token."""
    url = f"https://{JUDGE0_API_HOST}/submissions/{token}?base64_encoded=true"
    headers = {
        "X-RapidAPI-Key": JUDGE0_API_KEY,
        "X-RapidAPI-Host": JUDGE0_API_HOST
    }
    
    # Poll for the result
    for _ in range(10): # Poll for a maximum of 10 seconds
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            result = response.json()
            if result['status']['id'] > 2: # Status 1: In Queue, Status 2: Processing
                return result
            time.sleep(1)
        except requests.exceptions.RequestException as e:
            print(f"!! API Error during result fetching: {e}")
            return None
    
    print("!! Error: Judge0 polling timed out.")
    return None

# --- Main Execution Logic ---

if __name__ == "__main__":
    print(f"--- Starting Evaluation for: {SOLUTION_FILE_PATH} ---")

    # 1. Get Problem Info
    problem_name, lang_id = get_problem_name_and_lang(SOLUTION_FILE_PATH)
    print(f"Problem: {problem_name}, Language ID: {lang_id}")

    # 2. Get Test Cases
    test_cases = get_test_cases(problem_name)
    if not test_cases:
        print(f"!! No test cases found for '{problem_name}'. Aborting.")
        sys.exit(1)
    print(f"Found {len(test_cases)} test cases.")

    # 3. Read the intern's source code
    with open(SOLUTION_FILE_PATH, 'r') as f:
        source_code = f.read()

    # 4. Run evaluation loop
    passed_count = 0
    total_count = len(test_cases)
    
    for i, case in enumerate(test_cases):
        print(f"\n-> Running Test Case #{i}...")
        with open(case['input'], 'r') as f:
            stdin_data = f.read()
        with open(case['output'], 'r') as f:
            expected_stdout = f.read().strip()

        # Submit to Judge0
        token = submit_to_judge0(source_code, lang_id, stdin_data)
        if not token:
            print("!! Failed to submit to Judge0. Skipping test case.")
            continue
            
        # Get result from Judge0
        result = get_judge0_result(token)
        if not result:
            print("!! Failed to get result from Judge0. Skipping test case.")
            continue

        # 5. Check the result
        status = result['status']['description']
        print(f"   Status: {status}")

        if status == "Accepted":
            actual_stdout = base64.b64decode(result.get('stdout', b'')).decode().strip()
            if actual_stdout == expected_stdout:
                print("   ✅ Result: PASSED")
                passed_count += 1
            else:
                print("   ❌ Result: FAILED (Wrong Answer)")
                # To avoid leaking test cases, don't print the diff in the main log
                # print(f"      Expected: '{expected_stdout}'")
                # print(f"      Got:      '{actual_stdout}'")
        else:
            print(f"   ❌ Result: FAILED ({status})")
            stderr = base64.b64decode(result.get('stderr', b'')).decode()
            if stderr:
                print(f"      Error Output: {stderr.strip()}")

    # 6. Final Summary
    print("\n--- Evaluation Summary ---")
    print(f"File: {SOLUTION_FILE_PATH}")
    print(f"Passed: {passed_count} / {total_count}")
    print("--------------------------")

    if passed_count != total_count:
        sys.exit(1) # Exit with a non-zero code to make the GitHub Action fail
