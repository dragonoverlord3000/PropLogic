from interpreter.definitions.tokens import Token, TokenType

# The important part is the `truth_table_dict` at the bottom


"""
These functions take TokenType.TRUE and TokenType.FALSE as input and returns a new 
Token of either type TRUE or type FALSE, depending on the input.
"""

# Negation '~'
def negation_truth_table(a:TokenType) -> TokenType:
    if a.type == TokenType.TRUE:
        return Token(TokenType.FALSE)
    elif a.type == TokenType.FALSE:
        return Token(TokenType.TRUE)
    else:
        print(f"Error, token type ('{a.type}') is not boolean")


# Conjunction '&'
def conjunction_truth_table(a:TokenType, b:TokenType) -> TokenType:
    if a.type == TokenType.TRUE and b.type == TokenType.TRUE:
        return Token(TokenType.TRUE)
    elif a.type == TokenType.TRUE and b.type == TokenType.FALSE:
        return Token(TokenType.FALSE)
    elif a.type == TokenType.FALSE and b.type == TokenType.TRUE:
        return Token(TokenType.FALSE)
    elif a.type == TokenType.FALSE and b.type == TokenType.FALSE:
        return Token(TokenType.FALSE)
    else:
        print(f"Error, either token type ('{a.type}') or ;) token type ('{b.type}') is not boolean")

# Disjunction '|'
def disjunction_truth_table(a:TokenType,b:TokenType) -> TokenType:
    if a.type == TokenType.TRUE and b.type == TokenType.TRUE:
        return Token(TokenType.TRUE)
    elif a.type == TokenType.TRUE and b.type == TokenType.FALSE:
        return Token(TokenType.TRUE)
    elif a.type == TokenType.FALSE and b.type == TokenType.TRUE:
        return Token(TokenType.TRUE)
    elif a.type == TokenType.FALSE and b.type == TokenType.FALSE:
        return Token(TokenType.FALSE)
    else:
        print(f"Error, either token type ('{a.type}') or ;) token type ('{b.type}') is not boolean")


# Implication '>'
def implication_truth_table(a:TokenType, b:TokenType) -> TokenType:
    if a.type == TokenType.TRUE and b.type == TokenType.TRUE:
        return Token(TokenType.TRUE)
    elif a.type == TokenType.TRUE and b.type == TokenType.FALSE:
        return Token(TokenType.FALSE)
    elif a.type == TokenType.FALSE and b.type == TokenType.TRUE:
        return Token(TokenType.TRUE)
    elif a.type == TokenType.FALSE and b.type == TokenType.FALSE:
        return Token(TokenType.TRUE)
    else:
        print(f"Error, either token type ('{a.type}') or ;) token type ('{b.type}') is not boolean")

# Converse Implication '<'
def converse_implication_truth_table(a:TokenType, b:TokenType) -> TokenType:
    if a.type == TokenType.TRUE and b.type == TokenType.TRUE:
        return Token(TokenType.TRUE)
    elif a.type == TokenType.TRUE and b.type == TokenType.FALSE:
        return Token(TokenType.TRUE)
    elif a.type == TokenType.FALSE and b.type == TokenType.TRUE:
        return Token(TokenType.FALSE)
    elif a.type == TokenType.FALSE and b.type == TokenType.FALSE:
        return Token(TokenType.TRUE)
    else:
        print(f"Error, either token type ('{a.type}') or ;) token type ('{b.type}') is not boolean")

# Biconditional '<>'
def biconditional_truth_table(a:TokenType, b:TokenType) -> TokenType:
    if a.type == TokenType.TRUE and b.type == TokenType.TRUE:
        return Token(TokenType.TRUE)
    elif a.type == TokenType.TRUE and b.type == TokenType.FALSE:
        return Token(TokenType.FALSE)
    elif a.type == TokenType.FALSE and b.type == TokenType.TRUE:
        return Token(TokenType.FALSE)
    elif a.type == TokenType.FALSE and b.type == TokenType.FALSE:
        return Token(TokenType.TRUE)
    else:
        print(f"Error, either token type ('{a.type}') or ;) token type ('{b.type}') is not boolean")

# Relate operator type to their truth table
truth_table_dict = {
    TokenType.NEGATION: negation_truth_table,
    TokenType.CONJUNCTION: conjunction_truth_table,
    TokenType.DISJUNCTION: disjunction_truth_table,
    TokenType.IMPLICATION: implication_truth_table,
    TokenType.CONVERSEIMPLICATION: converse_implication_truth_table,
    TokenType.BICONDITIONAL: biconditional_truth_table
}








