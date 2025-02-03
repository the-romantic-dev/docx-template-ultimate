from sympy import Rational, Expr, Symbol, latex, pretty

from sympy_prettifier import rational_to_latex, rational_to_string


def _get_var_func(var: Symbol | str, is_latex: bool):
    if isinstance(var, str):
        return lambda x: x
    return latex if is_latex else pretty


def _rational_coeff_term(coeff: Rational, var: Symbol | str, is_latex: bool) -> str:
    var_func = _get_var_func(var, is_latex)
    if coeff == 0:
        return ""

    op = " + " if coeff > 0 else ""
    if abs(coeff) == 1:
        return f"{op} {var_func(var)}"
    dot = "·" if not is_latex else ""
    term = rational_to_latex(coeff) if is_latex else rational_to_string(coeff)
    return f"{op} {term}{dot}{var_func(var)}"


def _format_expression(coeffs: list[float | int | Rational | Expr], variables: list[Symbol | str], constant: Rational,
                       is_latex: bool) -> str:
    terms = []

    for coeff, var in zip(coeffs, variables):
        if isinstance(coeff, (Rational, float, int)):
            terms.append(_rational_coeff_term(Rational(coeff), var, is_latex))
        elif isinstance(coeff, Expr):
            var_func = _get_var_func(var, is_latex)
            dot = "·" if not is_latex else ""
            term = latex(coeff) if is_latex else str(coeff)
            terms.append(f"{term}{dot}{var_func(var)}")

    if constant != 0:
        constant_latex = rational_to_latex(constant)
        op = " + " if constant > 0 else ""
        terms.append(f"{op} {constant_latex}")

    return " ".join(terms).strip().lstrip("+").lstrip()


def expression_to_string(coeffs: list[float | int | Rational | Expr], variables: list[Symbol | str],
                      constant: Rational = Rational(0)):
    return _format_expression(coeffs, variables, constant, is_latex=False)


def expression_to_latex(coeffs: list[float | int | Rational | Expr], variables: list[Symbol | str],
                        constant: Rational = Rational(0)):
    return _format_expression(coeffs, variables, constant, is_latex=True)
