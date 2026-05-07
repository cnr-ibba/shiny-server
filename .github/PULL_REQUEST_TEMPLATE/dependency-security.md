## Dependency/Security Update Checklist

### Change Scope

- [ ] This PR updates only dependency files and lockfiles.
- [ ] The updated packages are listed in the PR description.
- [ ] Security relevance is documented (critical/high/other).

### Validation (required)

- [ ] Django lint workflow passed.
- [ ] Django tests workflow passed.
- [ ] Docker uwsgi image build workflow passed.

### Runtime and Risk Checks

- [ ] No database migration side effects were introduced unexpectedly.
- [ ] Authentication/authorization paths were sanity checked.
- [ ] If update is major, rollback plan is documented.

### Security Closure

- [ ] Linked Dependabot alert IDs are referenced.
- [ ] Critical alerts fixed by this PR are confirmed as resolved after merge.
