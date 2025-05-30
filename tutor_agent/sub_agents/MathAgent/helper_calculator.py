from sympy import (
    parse_expr, simplify, expand, factor, latex, Eq, solve, apart, together
)
from sympy.core.sympify import SympifyError
from sympy.core.evalf import PrecisionExhausted

def parse_equation(expr_str: str) -> dict:
    try:
        if '=' in expr_str:
            lhs_str, rhs_str = expr_str.split('=')
            lhs = parse_expr(lhs_str.strip(), evaluate=True)
            rhs = parse_expr(rhs_str.strip(), evaluate=True)
            expr = Eq(lhs, rhs)
        else:
            expr = parse_expr(expr_str, evaluate=True)

        simplified = simplify(expr)
        expanded = expand(expr)
        factored = factor(expr)

        rational_apart = apart(expr) if not isinstance(expr, Eq) else None
        rational_together = together(expr) if not isinstance(expr, Eq) else None

        free_vars = list(expr.free_symbols)
        try:
            solutions = solve(expr, free_vars) if free_vars else None
        except Exception as e:
            solutions = f"Could not solve: {e}"

        return {
            "original": str(expr),
            "simplified": str(simplified),
            "expanded": str(expanded),
            "factored": str(factored),
            "rational_apart": str(rational_apart),
            "rational_together": str(rational_together),
            "solutions": solutions,
            "variables": [str(v) for v in free_vars],
            "latex": latex(expr)
        }

    except SympifyError:
        return {"error": "Invalid mathematical expression."}
    except ZeroDivisionError:
        return {"error": "Division by zero."}
    except ValueError as ve:
        return {"error": f"Value Error: {ve}"}
    except PrecisionExhausted:
        return {"error": "Precision limit exceeded while evaluating expression."}
    except Exception as e:
        return {"error": f"Unexpected Error: {str(e)}"}
