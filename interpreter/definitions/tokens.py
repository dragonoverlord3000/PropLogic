from dataclasses import dataclass
from enum import Enum

# Note that if 'TokenType' didn't inherit from 'Enum', then the TokenType
# Would just be the number associated with the tokentype - so Enum just makes it more readable for us mere humans ;)
class TokenType(Enum):
    # Propositional constants
    TRUE                     = 0 # symbol: T
    FALSE                    = 1 # symbol: F

    # Propositional formulae/variables
    PROPVAR                  = 2 # symbol: often p,q,r,..., but the whole alphabet minus T and F is valid

    # Unary logical connectives
    NEGATION                 = 3 # symbol: ~

    # Binary logical connectives
    DISJUNCTION              = 4 # symbol: |
    CONJUNCTION              = 5 # symbol: &
    IMPLICATION              = 6 # symbol: >
    CONVERSEIMPLICATION      = 7 # symbol: <
    BICONDITIONAL            = 8 # symbol: <>

    # Auxillary symbols
    LPAREN                   = 9 # symbol: (
    RPAREN                   = 10 # symbol: )

    # Substitution symbol - only for internal reasons
    SUBSTVAR                 = 11 # symbol: None


@dataclass
class Token:
    type: TokenType
    # The value of a token can be w/e - the default is 'None'
    value: any = None

    def __repr__(self) -> str:
        return f"{self.type}" + (f": {self.value}" if self.value else "")




