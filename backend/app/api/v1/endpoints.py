from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.solvers.parser import parse_user_expression
from app.solvers.derivatives.engine import solve_derivative_step_by_step

router = APIRouter()

class DerivativeRequest(BaseModel):
    expression: str = Field(..., example="5x^2 / sin(x)", description="Expresión matemática a derivar")
    variable: str = Field(default="x", example="x", description="Variable respecto a la cual derivar")

class StepResponse(BaseModel):
    step_number: int
    rule_name: str
    explanation: str
    expression_latex: str

@router.post("/solve-derivative", response_model=list[StepResponse])
def solve_derivative(payload: DerivativeRequest):
    try:
        parsed_expr, var_symbol = parse_user_expression(payload.expression, payload.variable)
        steps = solve_derivative_step_by_step(parsed_expr, var_symbol)
        return steps
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno procesando la derivada: {str(e)}")