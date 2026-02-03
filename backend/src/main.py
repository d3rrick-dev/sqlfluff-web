from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel, Field
from sqlfluff.core import Linter, FluffConfig

from .utils import clean_sql_input

app = FastAPI(title="SQLFluff Web Linter", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # on dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LintRequest(BaseModel):
    sql: str = Field(..., min_length=1)
    dialect: str = "postgres"

class Violation(BaseModel):
    code: str
    description: str
    line: int | None = None
    position: int | None = None

class LintResponse(BaseModel):
    success: bool
    violations: list[Violation]
    fixed_sql: str | None = None


@app.post("/lint", response_model=LintResponse)
def lint(req: LintRequest):
    try:
        config = FluffConfig(overrides={"dialect": req.dialect})
        linter = Linter(config=config)
        
        linted_result = linter.lint_string(clean_sql_input(req.sql), fix=True)
    
        violations = [
            Violation(
                code=v.rule_code(),
                description=v.description,
                line=v.line_no,
                position=v.line_pos,
            )
            for v in linted_result.get_violations()
        ]

        fixed_sql, _ = linted_result.fix_string()
        
        return LintResponse(
            success=len(violations) == 0,
            violations=violations,
            fixed_sql=fixed_sql if len(violations) > 0 else None
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SQLFluff Error: {str(e)}")
    

@app.get("/health")
def health():
    return {"status": "ok"}
