from sympy import Rational, latex, primefactors


def is_finite_decimal(rational: Rational):
    return set(primefactors(rational.q)) <= {2, 5}


def _format_rational(rational: Rational, frac_str: str):
    if rational.q == 1 or is_finite_decimal(rational):
        return str(f"{float(rational):.10f}").rstrip('0').rstrip('.')
    return frac_str


def rational_to_string(rational: Rational):
    return _format_rational(rational, frac_str=str(rational))


def rational_to_latex(rational: Rational):
    return _format_rational(rational, frac_str=latex(rational))
