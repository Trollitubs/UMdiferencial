from sympy import Symbol, Expr, Mul, Add, Pow, Integer, Float, sin, cos, tan, log, exp, latex

def solve_derivative_step_by_step(expr: Expr, var_symbol: Symbol) -> list[dict]:
    steps = []
    var_str = str(var_symbol)

    def diff_op(target_latex: str) -> str:
        """Helper para envolver una expresión en el operador diferencial d/dx[...]."""
        return f"\\frac{{d}}{{d{var_str}}}\\left[{target_latex}\\right]"

    def add_step(rule_name: str, explanation: str, expression_latex: str):
        steps.append({
            "step_number": len(steps) + 1,
            "rule_name": rule_name,
            "explanation": explanation,
            "expression_latex": expression_latex
        })

    # Paso inicial
    add_step(
        "Expresión Inicial",
        f"Función a derivar con respecto a ${var_str}$.",
        diff_op(latex(expr))
    )

    def _differentiate(node: Expr) -> Expr:
        # 1. Constante
        if node.is_number:
            add_step(
                "Regla de la Constante",
                f"La derivada de una constante es $0$.",
                "0"
            )
            return Integer(0)

        # 2. Variable respecto a la cual se deriva
        if node == var_symbol:
            add_step(
                "Regla de la Variable",
                f"La derivada de ${var_str}$ respecto a ${var_str}$ es $1$.",
                "1"
            )
            return Integer(1)

        # 3. Regla de la Suma / Resta
        if isinstance(node, Add):
            terms_latex = " + ".join([diff_op(latex(arg)) for arg in node.args])
            add_step(
                "Regla de la Suma",
                f"Separamos la derivada de cada término.",
                terms_latex
            )
            return sum((_differentiate(arg) for arg in node.args), Integer(0))

        # 4. Multiplicación (Cociente, Factor Constante, Producto)
        if isinstance(node, Mul):
            # A. Regla del Cociente
            numer, denom = node.as_numer_denom()
            if denom != Integer(1):
                add_step(
                    "Regla del Cociente",
                    f"Aplicamos $\\left(\\frac{{u}}{{v}}\\right)' = \\frac{{u'v - uv'}}{{v^2}}$ a ${diff_op(latex(node))}$.",
                    f"\\frac{{{diff_op(latex(numer))} \\cdot \\left({latex(denom)}\\right) - \\left({latex(numer)}\\right) \\cdot {diff_op(latex(denom))}}}{{\\left({latex(denom)}\\right)^2}}"
                )
                du = _differentiate(numer)
                dv = _differentiate(denom)
                result = (du * denom - numer * dv) / (denom ** 2)
                return result

            # B. Factor Constante
            coeff, non_coeff = node.as_coeff_Mul()
            if coeff != 1:
                add_step(
                    "Factor Constante",
                    f"Extraemos la constante ${latex(coeff)}$ fuera del operador diferencial.",
                    f"{latex(coeff)} \\cdot {diff_op(latex(non_coeff))}"
                )
                result = coeff * _differentiate(non_coeff)
                return result

            # C. Regla del Producto
            if len(node.args) == 2:
                u, v = node.args
                add_step(
                    "Regla del Producto",
                    f"Aplicamos la regla del producto a ${diff_op(latex(node))}$.",
                    f"{diff_op(latex(u))} \\cdot \\left({latex(v)}\\right) + \\left({latex(u)}\\right) \\cdot {diff_op(latex(v))}"
                )
                du = _differentiate(u)
                dv = _differentiate(v)
                return du * v + u * dv

        # 5. Regla de la Potencia y Cadena
        if isinstance(node, Pow):
            base, exp_val = node.args
            if exp_val.is_number and base == var_symbol:
                res = exp_val * (base ** (exp_val - 1))
                add_step(
                    "Regla de la Potencia",
                    f"Bajamos el exponente ${latex(exp_val)}$ y le restamos $1$.",
                    latex(res)
                )
                return res
            elif exp_val.is_number:
                add_step(
                    "Regla de la Cadena (Potencia)",
                    f"Aplicamos regla de la potencia a la base compuesta.",
                    f"{latex(exp_val)} \\cdot \\left({latex(base)}\\right)^{{{latex(exp_val - 1)}}} \\cdot {diff_op(latex(base))}"
                )
                dbase = _differentiate(base)
                return exp_val * (base ** (exp_val - 1)) * dbase

        # 6. Derivada Directa de Funciones Trigonométricas/Otras
        diff_direct = node.diff(var_symbol)
        add_step(
            "Derivada Directa",
            f"Calculamos la derivada de ${latex(node)}$.",
            latex(diff_direct)
        )
        return diff_direct

    final_result = _differentiate(expr)

    # Paso final de simplificación
    add_step(
        "Resultado Final Simplificado",
        "Respuesta final obtenida tras operar las derivadas.",
        latex(final_result)
    )

    return steps