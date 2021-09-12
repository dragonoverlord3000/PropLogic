from tokens import TokenType
from lexer import Lexer
from parser_ import Parser

def main():
    while True:
        text = input("<3 :")
        tokens = Lexer(text).generate_tokens()
        # print("Tokens: ", tokens)
        # print("Token types: ", [token.type == TokenType.PROPVAR for token in tokens])
        RPN = Parser(tokens).parse()
        print(f"\nParsed tokens: {RPN}")


if __name__ == "__main__":
    main()


