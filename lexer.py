from tokens import Token, TokenType


##### VARIABLES #####
WHITESPACE = " \n\r\t"

# The whole alphabet, minus t and f, can be used as propositional varaiables
alphabet = "abcdeghijklmnopqrsuvxyz"
PROPOSITIONALVARS = alphabet + alphabet.upper()
PROPOSITIONALCONSTTRUE = "tT"
PROPOSITIONALCONSTFALSE = "fF"

##### LEXER #####
# Note: it should be pretty easy to add more token types which is ofc pretty nice

class Lexer:
    def __init__(self, text) -> None:
        self.text = text
        self.text_len = len(text)
        self.tokens = []
        self.idx = 0

    def generate_tokens(self):
        while self.idx < self.text_len and self.text[self.idx] != None:
            # Not really necessary, but might be nice later
            if self.text[self.idx] in WHITESPACE:
                self.idx += 1
                continue
            
            # Propositional variables
            elif self.text[self.idx] in PROPOSITIONALVARS:
                self.tokens.append(Token(TokenType.PROPVAR, self.text[self.idx]))
            
            # Tautology
            elif self.text[self.idx] in PROPOSITIONALCONSTTRUE:
                self.tokens.append(Token(TokenType.TRUE))
            
            # Contradiction
            elif self.text[self.idx] in PROPOSITIONALCONSTFALSE:
                self.tokens.append(Token(TokenType.FALSE))
            
            # Negation
            elif self.text[self.idx] == "~":
                self.tokens.append(Token(TokenType.NEGATION))

            # Disjunction
            elif self.text[self.idx] == "|":
                self.tokens.append(Token(TokenType.DISJUNCTION))

            # Conjunction
            elif self.text[self.idx] == "&":
                self.tokens.append(Token(TokenType.CONJUNCTION))

            # Implication
            elif self.text[self.idx] == ">":
                self.tokens.append(Token(TokenType.IMPLICATION))

            # Converse Implication
            elif self.text[self.idx] == "<":
                self.tokens.append(Token(TokenType.CONVERSEIMPLICATION))

            # Biconditional
            elif self.text[self.idx] == "<>":
                self.tokens.append(Token(TokenType.BICONDITIONAL))

            # Left parentheses
            elif self.text[self.idx] == "(":
                self.tokens.append(Token(TokenType.LPAREN))

            # Right parentheses
            elif self.text[self.idx] == ")":
                self.tokens.append(Token(TokenType.RPAREN))

            else:
                print(f"Error, character '{self.text[self.idx]}' not recognized")

            self.idx += 1

        return self.tokens








