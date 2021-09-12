from tokens import TokenType

operator_types = [TokenType.NEGATION, TokenType.CONJUNCTION, TokenType.DISJUNCTION, 
                  TokenType.IMPLICATION, TokenType.CONVERSEIMPLICATION,
                  TokenType.BICONDITIONAL]


class Interpreter:
    def __init__(self, RPN:list) -> None:
        self.RPN_input = RPN

    def calculate_truth_assignment(self, truth_assignment:dict) -> TokenType:
        pass

    def setup_truth_table(self):
        pass

    def create_parse_tree(self) -> str:
        pass

    def tableau_method(self) -> str:
        pass

    def check_tautology(self) -> bool:
        pass










