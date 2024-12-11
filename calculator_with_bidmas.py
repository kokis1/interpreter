'''my own intrpretation of making an interpreter for a simple calculator'''


# list of types
INTEGER = "INTEGER"
PLUS = "PLUS"
MINUS = "MINUS"
MULTIPLY = "MULTIPLY"
DIVIDE = "DIVIDE"
EOF = "EOF"
LEFT_PARENTHESIS = "LEFT_PARENTHESIS"
RIGHT_PARENTHESIS = "RIGHT_PARENTHESIS"


class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value
    def __str__(self):
        return "TOKEN({type}, {value})".format(type=self.type, value=self.value)
    
    def __repr__(self):
        return self.__str__()
    

class Lexer(object):

    def __init__(self, text):
        self.text = text

        self.pos = 0

        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception("Trouble lexing the text")

    def advance(self):
        '''advance the pos pointer and update the current_char variable'''
        self.pos += 1

        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
    
    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def tokeniser(self):
        while self.current_char is not None:

            if self.current_char.isspace():
                self.advance()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char == "+":
                self.advance()
                return Token(PLUS, "+")
            
            if self.current_char == "-":
                self.advance()
                return Token(MINUS, "-")
            
            if self.current_char == '*':
                self.advance()
                return Token(MULTIPLY, "*")
            
            if self.current_char == '/':
                self.advance()
                return Token(DIVIDE, "/")
            
            if self.current_char == "(":
                self.advance()
                return Token(LEFT_PARENTHESIS, "(")
            
            if self.current_char == ")":
                self.advance()
                return Token(RIGHT_PARENTHESIS, ")")
            
            self.error()
        return Token(EOF, None)

class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer

        self.current_token = self.lexer.tokeniser()
    def error(self):
        raise Exception("Error parsing")
    

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.tokeniser()
        else:
            self.error()

    def factor(self):
        """factor : INTEGER | LPAREN expr RPAREN"""
        token = self.current_token
        if token.type == INTEGER:
            self.eat(INTEGER)
            return token.value
        elif token.type == LEFT_PARENTHESIS:
            self.eat(LEFT_PARENTHESIS)
            result = self.expr()
            self.eat(RIGHT_PARENTHESIS)
            return result
    
    def term(self):
        result = self.factor()

        while self.current_token.type in (MULTIPLY, DIVIDE):
            token = self.current_token

            if token.type == MULTIPLY:
                self.eat(MULTIPLY)
                result = result * self.factor()
            elif token.type == DIVIDE:
                self.eat(DIVIDE)
                result = result / self.factor()
        return result
    
    def expr(self):
       result = self.term()

       while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
                result = result + self.term()
            elif token.type == MINUS:
                self.eat(MINUS)
                result = result - self.term()

       return result
    

def main():
    while True:
        try:
            text = input("calc> ")
        except EOFError:
            break
        if not text:
            continue
        lexer = Lexer(text)
        parser = Parser(lexer)
        result = parser.expr()
        print(result)


if __name__ == "__main__":
    main()