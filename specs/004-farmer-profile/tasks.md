# Task List: Farmer Profile & Session Management

**Status**: Complete ✅

---

## Phase 1 — Session

- [x] T01: Generate sid via os.urandom(8).hex() on first visit *(15m)*
- [x] T02: Store sid in Flask session *(15m)*

## Phase 2 — Database

- [x] T03: Create queries table for knowledge base *(30m)*
- [x] T04: Implement log_query() *(20m)*
- [x] T05: Implement get_top_queries() *(20m)*
- [x] T06: Implement get_all_profiles() for admin view *(20m)*

## Phase 3 — Routes & UI

- [x] T07: Load profile on index() and pass to template *(20m)*
- [x] T08: Build /knowledge route and knowledge_base.html *(1h)*

## Phase 4 — Testing

- [x] T09: Test session persistence across page reloads
- [x] T10: Test knowledge base shows correct top queries
