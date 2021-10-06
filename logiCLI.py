from tokens import Token, TokenType
from lexer import Lexer
from parser_ import Parser
from interpreter import Interpreter

# truth_dict = {"T": True, "t": True, "F": False, "f": False}

# For quickly evaluating a propositional formula
def main():
    truth_dict = {"T": True, "t": True, "F": False, "f": False}

    while True:
        text = input("<3 :")

        # To create a truth assignment just write e.g. td{"a": True, "b": False, ..., "c": True}, then the truth assignment will be saved for the upcomming expression
        if text[:2] == "td":
            truth_dict = eval(text[2:])
            truth_dict["t"] = True; truth_dict["T"] = True; truth_dict["f"] = False; truth_dict["F"] = False;
            continue

        # From Text To Tokens
        tokens = Lexer(text).generate_tokens()
        print("Tokens: ", tokens)

        # From Infix to Postfix
        RPN = Parser(tokens).parse()
        print(f"\nParsed tokens: {RPN}")

        # From RPN to evaluated expression
        interpreted = Interpreter(RPN)
        # evaluated_expr = interpreted.calculate_truth_assignment(truth_dict)
        # print(f"\nEvaluated expression: ('{evaluated_expr}')\n")
        tt, tr = interpreted.setup_truth_table()
        print(f"\nTruth table: {tt}")
        # print(f"\nTruth table Latex: \n{interpreted.truth_table_converter(tt, tr)}")



if __name__ == "__main__":
    main()


