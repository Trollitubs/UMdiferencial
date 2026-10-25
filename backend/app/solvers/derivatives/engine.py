from sympy import Symbol, Expr, Add, Mul, Pow, diff, latex, Integer

def solve_derivative_step_by_step(expr: Expr, var_symbol: Symbol):
    steps = []
    step_counter = 0

    def add_step(rule_name: str, explanation: str, current_expr):
        nonlocal step_counter
        step_counter += 1
        steps.append({
            "step_number": step_counter,
            "rule_name": rule_name,
            "explanation": explanation,
            "expression_latex": latex(current_expr)
        })

    def _differentiate(node):
        # 1. Regla Constante
        if not node.has(var_symbol):
            add_step(
                "Regla de la Constante",
                f"La derivada de la constante ${latex(node)}$ es $0$.",
                Integer(0)
            )
            return Integer(0)

        # 2. Variable Identidad
        if node == var_symbol:
            add_step(
                "Regla de la Variable",  # Corregido typo "Varibale"
                f"La derivada de ${var_symbol.name}$ respecto a ${var_symbol.name}$ es $1$.",
                Integer(1)
            )
            return Integer(1)

        # 3. Regla de la suma
        if isinstance(node, Add):
            add_step(
                "Regla de la Suma",
                f"Separamos la expresión ${latex(node)}$ en derivadas independientes.",
                node
            )
            terms_derived = [_differentiate(arg) for arg in node.args]
            result = Add(*terms_derived)
            add_step(
                "Resultado Parcial de la Suma",
                "Unimos los términos derivados.",
                result
            )
            return result

        # 4. Factores constantes y regla del producto
        if isinstance(node, Mul):
            coeff, non_coeff = node.as_coeff_Mul()
            if coeff != 1:
                add_step(
                    "Factor Constante",
                    f"Extraemos la constante ${latex(coeff)}$ fuera de la derivada.",
                    node
                )
                result = coeff * _differentiate(non_coeff)
                return result

            if len(node.args) == 2:
                u, v = node.args
                add_step(
                    "Regla del Producto",
                    f"Aplicamos $(u \\cdot v)' = u'v + uv'$ a la expresión ${latex(node)}$.",
                    node
                )
                du = _differentiate(u)
                dv = _differentiate(v)
                result = du * v + u * dv
                add_step(
                    "Ensamblaje del Producto",
                    "Resultado de la regla del producto.",
                    result
                )
                return result

        # 5. Regla de la potencia
        if isinstance(node, Pow):
            base, exp = node.args
            if not exp.has(var_symbol):
                add_step(
                    "Regla de la Potencia",
                    f"Para ${latex(node)}$, bajamos el exponente ${latex(exp)}$ y restamos $1$ al exponente.",
                    node
                )
                dbase = _differentiate(base)
                result = exp * (base ** (exp - 1)) * dbase
                return result

        # 6. Regla General / Derivación directa
        add_step(
            "Regla General / Cadena",
            f"Derivamos la función ${latex(node)}$.",
            node
        )
        derived_node = diff(node, var_symbol)
        add_step(
            "Resultado de Derivación Directa",
            "Obtenemos la derivada de la función.",
            derived_node
        )
        return derived_node


    add_step(
        "Expresión Inicial",
        f"Función a derivar con respecto a ${var_symbol.name}$.",
        expr
    )

    _differentiate(expr)


    final_derived = diff(expr, var_symbol)
    add_step(
        "Resultado Final Simplificado",
        "Resultado final de la derivada completa.",
        final_derived
    )

    return steps