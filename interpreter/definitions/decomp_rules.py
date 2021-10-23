from interpreter.definitions.tokens import Token, TokenType

# The important part is the `decomp_rule_dict` at the bottom ???

"""
These functions take a boolean as input and returns [(0, bool)] for unary connectives
and returns [(0, BN, BN), (1, BN, BN)] or [(0, BN, BN)] for binary ones, where BN is an abreviation for
the union of bool and None (None meaning that the truth of subformula x can't be determined by this decomp rule).

- 0 means left (default)
- 1 means right

Not all logical connectives are commutative, so the order of 'BN' and the order of (0) and (1) matters!
"""

# Negation '~'
def negation_decomp(truth:bool) -> list:
    if truth:
        return [(0, False)]
    else:
        return [(0, True)]


# Conjunction '&'
def conjunction_decomp(truth:bool) -> list:
    if truth:
        return [(0, True, True)]
    else:
        return [(0, False, None), (1, None, False)]

# Disjunction '|'
def disjunstion_decomp(truth:bool) -> list:
    if truth:
        return [(0, True, None), (1, None, True)]
    else:
        return [(0, False, False)]

# Implication '>'
def implication_decomp(truth:bool) -> list:
    if truth:
        return [(0, False, None), (1, None, True)]
    else:
        return [(0, True, False)]

# Converse Implication '<'
def converse_implication_decomp(truth:bool) -> list:
    if truth:
        return [(0, True, None), (1, None, False)]
    else:
        return [(0, False, True)]

# Biconditional
def biconditional_decomp(truth:bool) -> list:
    if truth:
        return [(0, True, True), (1, False, False)]
    else:
        return [(0, True, False), (1, False, True)]



# Relate operator type to their decomposition rules
decomp_rule_dict = {
    TokenType.NEGATION: negation_decomp,
    TokenType.CONJUNCTION: conjunction_decomp,
    TokenType.DISJUNCTION: disjunstion_decomp,
    TokenType.IMPLICATION: implication_decomp,
    TokenType.CONVERSEIMPLICATION: converse_implication_decomp,
    TokenType.BICONDITIONAL: biconditional_decomp
}











