# ENSDF Change Tracking Process

## How to Ensure No Changes Are Missed

### 1. Pre-Work Setup
```powershell
# Always start with a clean git status
git status
git diff --name-only HEAD
```

### 2. During Work
- Keep track of which files you're modifying
- Make logical, atomic changes
- Test changes as you go

### 3. Change Detection (Multi-Tool Approach)
Use ALL of these tools to ensure comprehensive change detection:

#### A. Git Status and Diff
```powershell
# Check all modified files
git status

# Get list of changed files since last commit
git diff --name-only HEAD

# Check for detailed changes in specific files
git diff filename.ens
```

#### B. what-changed.ps1 Script
```powershell
# For specific ENSDF files
.\.vscode\what-changed.ps1 "finished\Ar35\new\Ar35_36ar_p_d.ens"
.\.vscode\what-changed.ps1 "finished\Ar35\new\Ar35_adopted.ens"
```

#### C. Untracked Files
```powershell
# Find new untracked files
git ls-files --others --exclude-standard
```

### 4. Systematic Change Documentation
1. **Run all detection tools** listed above
2. **Cross-verify results** - if git shows a change, use what-changed.ps1 for details
3. **Document in change.log** with specific line numbers and content changes
4. **Update commit message** with comprehensive summary

### 5. File Categories to Track
- **ENSDF source files**: *.ens files (most important)
- **Generated PDFs**: *.pdf files (expected to change when source changes)
- **Processing artifacts**: temp/*.* files (expected, document but don't commit)
- **Tools and scripts**: .vscode/*.* files (important for tooling changes)
- **Documentation**: README.md, change.log, etc.

### 6. Verification Checklist
Before finalizing any session:
- [ ] Run `git status` - check for all modified files
- [ ] Run `git diff --name-only HEAD` - get complete list
- [ ] Run `git ls-files --others --exclude-standard` - check untracked
- [ ] Use `what-changed.ps1` on each modified ENSDF file
- [ ] Update `change.log` with evidence-based entries
- [ ] Create comprehensive commit message
- [ ] Cross-check: did any ENSDF changes result in expected PDF updates?

### 7. Never Miss Changes Again
**The key is redundancy**: Use multiple detection methods and always cross-verify. If git shows a file changed, dig deeper with what-changed.ps1. If you modified an ENSDF file, expect to see corresponding PDF changes.

**Always ask**: "What files should have changed as a result of my work?" Then verify those expectations against the detection tools.

### 8. Evidence-Based Documentation
Every change log entry should be backed by:
- Specific file diffs from git or what-changed.ps1
- Line numbers where changes occurred
- Actual before/after content when significant
- Explanation of why the change was made

This process ensures comprehensive, systematic change tracking with multiple verification layers.
