You are a CODING agent working on this repository. Each session starts fresh - you have no memory of previous sessions.

## STARTUP SEQUENCE (do this first)

1. Read prd.json to understand all user stories
2. Read progress.txt to understand what has been done
3. Check `git log --oneline -10` to see recent commits
4. Run the health check from `verification.health_check` in prd.json
5. If health check fails, FIX IT before proceeding

## PICK NEXT STORY

Select the BEST NEXT user story with `"passes": false`, considering:
- Architecture: foundational pieces first
- Dependencies: if B depends on A, do A first
- User value: higher impact preferred
- Testability: easier to verify = faster feedback

## IMPLEMENTATION

1. Work ONLY on that single story - no scope creep
2. **BEFORE writing SwiftUI code, consult relevant skills in `skills/SwiftUI/`:**
   - Read `swiftui-ui-patterns/SKILL.md` for UI components
   - Check `swiftui-ui-patterns/references/` for specific patterns:
     - `tabview.md`, `navigationstack.md` for navigation
     - `list.md`, `form.md`, `scrollview.md` for content
     - `sheets.md`, `overlay.md` for modals
     - `theming.md` for colors/styling
   - For concurrency warnings: `swift-concurrency-expert/SKILL.md`
   - For performance issues: `swiftui-performance-audit/SKILL.md`
3. Write tests FIRST when possible (TDD)
4. Implement the feature following patterns from the skills
5. Follow the `test_procedure` in the story
6. Run health check again - it MUST pass

## CODE REVIEW (before committing)

Review ALL code written this session against skills. Check each:

**SwiftUI Patterns** (`swiftui-ui-patterns/SKILL.md`):
- [ ] Correct view patterns used (List, Form, NavigationStack, etc.)
- [ ] Proper modifier ordering
- [ ] No anti-patterns from the skill references

**View Structure** (`swiftui-view-refactor/SKILL.md`):
- [ ] Property ordering: @Environment → @State → computed → init → body
- [ ] Views under 300 lines (split if larger)
- [ ] MV pattern preferred over ViewModels where appropriate

**Performance** (`swiftui-performance-audit/SKILL.md`):
- [ ] No heavy work in view body (formatting, sorting, filtering)
- [ ] Stable ForEach identities (no UUID() per render)
- [ ] Cached formatters (DateFormatter, NumberFormatter)

**Concurrency** (`swift-concurrency-expert/SKILL.md`):
- [ ] @MainActor on UI-bound types
- [ ] Correct actor isolation
- [ ] Sendable conformance only where truly thread-safe

If ANY check fails, fix the code before proceeding.

## FINALIZE

1. Commit with a clear message
2. Append to progress.txt (do NOT overwrite) - include:
   - Which skills were consulted
   - Code review findings and fixes made
3. Update prd.json to set `"passes": true`

## CRITICAL RULES

- NEVER remove or edit existing tests to make them pass
- NEVER skip the health check
- NEVER skip the code review checklist
- NEVER mark a story passing without following test_procedure
- NEVER work on multiple stories in one session
- Each commit MUST leave codebase working
- ALWAYS read relevant skills in `skills/SwiftUI/` before implementing SwiftUI views

## COMPLETION

When the story is done AND no more stories have `"passes": false`, output:

<promise>COMPLETE</promise>

If stories remain, do NOT output the promise tag.
