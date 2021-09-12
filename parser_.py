# Note: the '_' in filename is because python has an inbuilt library called 'parser' - so this is to avoid messing with that
# This is an attempt at implementing the shunting-yard algorithm 
# Inspiration from: https://en.wikipedia.org/wiki/Shunting-yard_algorithm       ### Especially the 'graphical illustration'
# And from: http://mathcenter.oxford.emory.edu/site/cs171/shuntingYardAlgorithm/

##### IMPORTS #####
from tokens import TokenType

##### PRECEDENCE TABLE #####

precedence_table = {TokenType.NEGATION: 1, TokenType.CONJUNCTION: 2, TokenType.DISJUNCTION: 2, 
                    TokenType.IMPLICATION: 3, TokenType.CONVERSEIMPLICATION: 3, TokenType.BICONDITIONAL: 4,
                    TokenType.LPAREN: 5, TokenType.RPAREN: 5}

##### VARIABLES #####
symbol_types = [TokenType.PROPVAR, TokenType.TRUE, TokenType.FALSE]
operator_types = [TokenType.NEGATION, TokenType.CONJUNCTION, TokenType.DISJUNCTION, TokenType.IMPLICATION,
             TokenType.CONVERSEIMPLICATION, TokenType.BICONDITIONAL]
aux_types = [TokenType.LPAREN, TokenType.RPAREN]

##### PARSER #####

class Parser:
    def __init__(self, tokens:list) -> None:
        self.INFIX_input = tokens
        self.operator_stack = []
        self.POSTFIX_output = []

    def parse(self) -> list:
        # Turn the given list of tokens into an equivalent list in RPN using 'shunting-yard algorithm' - making it interpretable
        while len(self.INFIX_input) > 0:
            t = self.INFIX_input.pop(0)
            if t.type in symbol_types:
                self.POSTFIX_output.append(t)
                continue
            elif t.type in operator_types:
                self.handle_operators(t)
                continue
            elif t.type in aux_types:
                if t.type == TokenType.LPAREN:
                    self.operator_stack.append(t)
                elif t.type == TokenType.RPAREN:
                    self.handle_RPAREN()
                continue
            else:
                print(f"Error, unknown Token ('{t}')")
            continue # Yes, a bit redundant, but w/e

        # Push the rest of the operators
        self.POSTFIX_output += list(reversed(self.operator_stack))
        return self.POSTFIX_output


    def handle_operators(self, t) -> None:
        while len(self.operator_stack) and (precedence_table[self.operator_stack[-1].type] < precedence_table[t.type]):
            to_push = self.operator_stack.pop()
            self.POSTFIX_output.append(to_push)
        self.operator_stack.append(t)
    
    def handle_RPAREN(self) -> None:
        while self.operator_stack[-1].type != TokenType.LPAREN:
            to_push = self.operator_stack.pop()
            self.POSTFIX_output.append(to_push)
        self.operator_stack.pop()
            
        
    







