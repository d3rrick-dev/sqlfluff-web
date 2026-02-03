
### Lint and fix sql
Based off [SQLFluff](https://www.sqlfluff.com/)

Writing SQL is easy; writing maintainable, standardized, and bug-free SQL is hard. This tool bridges the gap between raw queries and production-ready code by providing an instant, visual feedback loop.

#### Key Benefits
- *Enforce Unified Standards*: Stop debates in Pull Requests about "Uppercase vs. Lowercase." Automatically align your team to a single source of truth across 20+ dialects.

- *Reduce Technical Debt*: Identify "code smells" like SELECT * (Rule AM04) or ordinal sorting (ORDER BY 1) before they cause performance issues in production.

- *Instant Onboarding*: New developers don't need to memorize your company's SQL style guide—the linter teaches it to them in real-time as they type.

- *Safe Transformations*: The "Auto-Fix" engine handles the tedious work of re-indenting and re-casing, allowing engineers to focus on the logic rather than the formatting.


### Backend (dev)
```bash
uvicorn main:app --reload
uvicorn main:app --reload --log-level debug
python -m uvicorn main:app --reload --log-level debug
```

### Testing
```bash
pytest test_main.py -v 
```

### Frontend
```bash
npm run dev
```

### Demo
- Parsing and fix
![landing](./img/01.png)

- Supported dialects
![languages](./img/02.png)