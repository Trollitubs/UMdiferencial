from sympy import parse_expr, Symbol
from sympy.parsing.sympy_parser import (
    standard_transformations,
    implicit_multiplication_application,
    convert_xor,
    function_exponentiation
)

TRANSFORMATIONS = standard_transformations + (
    implicit_multiplication_application,
    convert_xor,
    function_exponentiation
)

def parse_user_expression(expression_str: str, var_name: str = "x" ):

    if (not expression_str) or (not expression_str.strip()):
        raise ValueError("La expresión matemática no puede estar vacia")
    
    var_symbol = Symbol(var_name)
    symbol_map = {var_name: var_symbol}

    try:
        parsed_expr = parse_expr(
            expression_str,
            local_dict=symbol_map,
            transformations=TRANSFORMATIONS
        )
        return parsed_expr, var_symbol
    except Exception as error:
        raise ValueError(f"Error al analizar la expresión: {str(error)}")