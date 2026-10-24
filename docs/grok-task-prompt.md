# Grok Build task prompt template

Use this template for each SWE-bench instance. Replace the bracketed fields with the task's issue statement and repository context. Do not provide reference patches or hidden tests.

---

You are solving one SWE-bench Lite software issue.

**Instance ID:** [instance_id]

**Issue statement:**
[issue text supplied by the benchmark]

**Instructions**
1. Inspect the existing repository and identify the smallest correct fix.
2. Read the relevant source and existing tests before editing.
3. Add a focused regression test when appropriate.
4. Make only changes needed for the issue. Do not create environment shims or unrelated files to work around missing dependencies unless the task genuinely requires them.
5. Run the most relevant available tests. If a test cannot run, state the exact reason; do not claim it passed.
6. Review the final diff for unrelated changes and whitespace errors.
7. Return the complete patch as a unified diff, plus a short summary of changed files and tests.
8. Do not access, request, search for, or infer benchmark reference solutions or hidden test patches.

**Tool-use discipline**
- If a tool call fails, inspect the actual error and correct the call schema before retrying.
- Do not repeat an identical failed call without changing the cause.
- Prefer a small number of targeted source/test reads over broad repository dumps.
- Stop when the patch and evidence are ready; do not spend turns on unrelated setup.

**Required final response**
- Patch (unified diff)
- Root cause and fix summary
- Tests run and exact outcomes
- Any remaining uncertainty
