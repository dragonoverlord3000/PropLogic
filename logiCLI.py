from interpreter.definitions.tokens import Token, TokenType
from interpreter.lexer import Lexer
from interpreter.parser_ import Parser
from interpreter.interpreter import Interpreter
from convert.from_truth_table import to_latex


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
        tt = interpreted.setup_truth_table()
        print(f"\nTruth table: {tt}")
        print(f"\nLatex truth table: \n{to_latex(tt)}")
        # print(f"\nTruth table Latex: \n{interpreted.truth_table_converter(tt, tr)}")



if __name__ == "__main__":
    main()


