# Astropy smoke test

- **Instance:** `astropy__astropy-12907`
- **Outcome:** Resolved by the official SWE-bench evaluator.
- **Completed:** 1
- **Resolved:** 1
- **Unresolved:** 0
- **Infrastructure failures:** 0
- **Evaluation run ID:** `astropy-grok-fix`
- **Reported model identifier:** `sofie-think-0`
- **Local evaluator report:** `~/swebench-work/sofie-think-0.astropy-grok-fix.json`
- **Full benchmark status:** Not started.

The patch preserves the right-hand submodel's separability matrix in Astropy's `_cstack` instead of replacing the nested matrix with ones, and adds a regression test for a nested compound model. The focused test file was also run in the task image and reported 12 passing tests.

This note is a summary of the run output available in the project workflow; the raw local evaluator report has not been uploaded to this repository yet. The smoke test is not representative of a 300-task aggregate score.
