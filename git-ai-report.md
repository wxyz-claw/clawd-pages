# Technical Report: git-ai Implementation & Perforce Porting Feasibility

## 1. git-ai Technical Implementation

### A. Interception Mechanism
`git-ai` does not passively watch files. It uses a dual-layer interception strategy to capture the "intent" and "source" of code changes before they are committed.

1.  **Editor Integration (The Trigger):**
    *   **Extensions:** `git-ai` installs extensions for VS Code (`git-ai.git-ai-vscode`), Cursor, and others.
    *   **Checkpoints:** These extensions explicitly trigger a `git-ai checkpoint` command when AI generation occurs. This snapshots the working directory state *before* the user manually commits.
    *   **Data Injection:** The extensions pass metadata (Model ID, Prompt text, Transcript) to the checkpoint command, which stores it in a local **Working Log** (located in `.git/git-ai/working_log`).

2.  **Git Shim (The Enforcer):**
    *   **Path Manipulation:** On installation, `git-ai` modifies the editor's configuration (e.g., `git.path` in VS Code) to point to a "shim" binary instead of the system `git`.
    *   **Command Interception:** When the user runs `git commit`, the shim intercepts the command. It triggers the `post-commit` process, which finalizes the data collection.

### B. Metadata Storage (Schema & Location)
The metadata is stored in two stages: transient (pre-commit) and persistent (post-commit).

1.  **Transient: Working Log**
    *   Stored in `.git/git-ai/working_log/`.
    *   Contains a sequence of "Checkpoints" (snapshots of file states after each AI generation but before commit).

2.  **Persistent: Git Notes**
    *   **Ref:** `refs/notes/ai` (not the default `refs/notes/commits`).
    *   **Format:** The "Authorship Log" is serialized as a JSON blob and attached to the commit SHA using `git notes add`.
    *   **Schema:** The JSON contains an `attestations` array mapping file paths to attribution data, including:
        *   `messages`: The prompt/response transcript.
        *   `agent_id`: Tool and model used (e.g., "cursor:claude-3.5-sonnet").
        *   `attributions`: A list of character ranges (start/end) linked to specific authors.

### C. Line Mapping & Diffing
`git-ai` uses a sophisticated custom tracking system, not standard `git blame`.

1.  **Attribution Tracker:**
    *   Implemented in `src/authorship/attribution_tracker.rs`.
    *   It maintains a persistent mapping of line ownership across multiple checkpoints.
    *   When a new checkpoint is created, it calculates the diff from the *previous checkpoint* (not just the HEAD).

2.  **Algorithm:**
    *   It uses the **Myers diff algorithm** (via the `imara-diff` Rust crate) to compute line changes (`Insert`, `Delete`, `Equal`).
    *   **Logic:**
        *   Lines unchanged from the previous state inherit their authorship.
        *   New lines introduced in an AI checkpoint are attributed to the AI agent.
        *   New lines introduced in a Human checkpoint are attributed to the user.

---

## 2. Perforce (Helix Core) Porting Strategy

Porting to Perforce is feasible but requires shifting from a "local repository" mindset to a "centralized server" mindset.

### A. Architectural Comparison

| Feature | Git Architecture | Perforce Equivalent |
| :--- | :--- | :--- |
| **Storage** | Distributed `.git` folder | Centralized Server (Depot) |
| **Metadata** | `git notes` (attached to commit) | `p4 attribute` (attached to file revision) |
| **Staging** | Index / Staging Area | Pending Changelist |
| **Checkpoints** | Local hidden commits | **Shelving** (`p4 shelve`) |
| **Blame** | `git blame` | `p4 annotate` |

### B. Implementation Strategy: "p4-ai"

#### 1. Storage: Attributes & Changelists
Instead of `git notes`, we will use **Perforce Attributes** to store the JSON metadata.
*   **Command:** `p4 attribute -n git-ai-data -v <JSON_BLOB> //depot/path/to/file@change`
*   **Why:** Attributes are versioned per file. This allows `p4-ai` to fetch the exact metadata for `//depot/file.c#5`.
*   **Fallback:** If attributes are restricted, store the JSON in the **Changelist Description** (wrapped in a delimiter like `===GIT-AI-DATA===`).

#### 2. Interception: The "Shelve-point"
Since Perforce has no local history, we must synthesize the "Checkpoint" concept using **Shelving**.
*   **Mechanism:** When the editor triggers a checkpoint (e.g., after AI generation), `p4-ai` will:
    1.  Create a hidden pending changelist.
    2.  `p4 shelve` the current files into that changelist.
    3.  Store the AI metadata (prompt, model) as an attribute on the shelved files or the changelist description.
*   **Finalization:** When the user submits the actual changelist, `p4-ai` (via a wrapper or trigger) will:
    1.  Fetch the sequence of shelved "checkpoints".
    2.  Compute the final attribution (collapsing the diffs).
    3.  Write the final JSON attribute to the submitted file revisions.

#### 3. Line Mapping: Client-Side Calculation
Perforce's server-side logic is too rigid for this. The logic must remain client-side (in Rust).
*   **Fetch:** `p4 print` to get file content of previous revisions.
*   **Diff:** Reuse the Rust `imara-diff` logic to compare the local file against the shelved checkpoints.
*   **Blame:** `p4-ai annotate <file>` will run `p4 annotate -q <file>`, parse the output to get revision numbers for each line, and then look up the `git-ai-data` attribute for those revisions to overlay the AI authorship.

### C. Migration Path
1.  **Build the CLI (`p4-ai`):**
    *   Implement `p4-ai checkpoint`: Wraps `p4 shelve`.
    *   Implement `p4-ai submit`: Wraps `p4 submit` to inject attributes.
2.  **Update Editor Extensions:**
    *   Modify `git-ai-vscode` to detect a Perforce workspace (presence of `P4PORT`/`P4CLIENT`).
    *   Switch command calls from `git-ai checkpoint` to `p4-ai checkpoint`.
3.  **Server Config:**
    *   Ensure `p4 attribute` permission is enabled for developers.

### Summary
The core logic of `git-ai` (diffing, attribution tracking, and schema) can be reused almost entirely. The primary effort is replacing the `git` plumbing (notes/commits) with `p4` plumbing (attributes/shelves). The "Shelve as Checkpoint" strategy provides a robust equivalent to Git's local object storage.
