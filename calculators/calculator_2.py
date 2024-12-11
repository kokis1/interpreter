'''my own intrpretation of making an interpreter for a simple calculator'''


# list of types
INTEGER = "INTEGER"
PLUS = "PLUS"
MINUS = "MINUS"
MULTIPLY = "MULTIPLY"
DIVIDE = "DIVIDE"
EOF = "EOF"


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

        self.current_token = None

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
            
            self.error()
        return Token(EOF, None)


class Parser(object):

    def __init__(self, lexer):
        self.lexer = lexer
    
    def error(self):
        raise Exception("Error parsing")

    def eat(self, token_type):
        if self.lexer.current_token.type == token_type:
            self.lexer.current_token = self.lexer.tokeniser()
        else:
            self.error()

    def term(self):
        token = self.lexer.current_token
        self.eat(INTEGER)
        return token.value
    
    def expr(self):

        self.lexer.current_token = self.lexer.tokeniser()

        result = self.term()

        while self.lexer.current_token.type in (PLUS, MINUS, MULTIPLY, DIVIDE):
            token = self.lexer.current_token

            if token.type == MINUS:
                self.eat(MINUS)
                result = result - self.term()
            elif token.type == PLUS:
                self.eat(PLUS)
                result = result + self.term()
            elif token.type == MULTIPLY:
                self.eat(MULTIPLY)
                result = result * self.term()
            elif token.type == DIVIDE:
                self.eat(DIVIDE)
                result = result / self.term()
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