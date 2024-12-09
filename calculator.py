# token types
# EOF is the end of file token, indicating that there is no more input for the lexical analysis


INTEGER, PLUS, EOF, MINUS, MULTIPLY, DIVIDE = "INTEGER", "PLUS", "EOF", "MINUS", "MULTIPLY", "DIVIDE"

class Token(object):
    def __init__(self, type, value):
        # token type: integer, plus, eof or minus
        self.type = type
        # token value = 0, 1,...,9 "+", "eof" or "-"
        self.value = value
    def __str__(self):
        '''string representation of the class instance
        examples:
            Token(INTEGER, 3)
            Token(PLUS, "+")'''
        return "Token({type}, {value})".format(type=self.type, value=self.value)
    
    def __repr__(self):
        return self.__str__()
    


class Interpreter(object):
    def __init__(self, text):
        # string input, e.g 3 + 5
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        # the current token instance
        self.current_token = None
        self.current_char = self.text[self.pos]
    def error(self):
        raise Exception("Error parsing input")
    
    def advance(self):
        ''''advnace the pos variable and set the current_char variable'''
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
    
    def integer(self):
        '''return a multidigit integer consumed from the inpus'''
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        '''lexical analyser, also known as a scanner or tokenizer
        This method breaks a sentence apart into tokens, one token at a time'''
        while self.current_char is not None:
            
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char == "+":
                self.advance()
                return Token(PLUS, "+")
            
            if self.current_char == "-":
                self.advance()
                return  Token(MINUS, "-")
            
            if self.current_char == "/":
                self.advance()
                return Token(DIVIDE, "/")
            
            if self.current_char == "*":
                self.advance()
                return Token(MULTIPLY, "*")
            
            self.error()
        
        return Token(EOF, None)
    
    
    def eat(self, token_type):
        '''compare the current token type with the passed token type and if the match then 
        eat the current token and assign the next token to the self.current_token, otherwise raise an exception'''

        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()
    
    def expr(self):
        '''parser/interpreter
        
           expr -> INTEGER PLUS INTEGER
           expr -> INTEGER MINUS INTEGER'''
        # set the current token to the first token taken from the input

        self.current_token = self.get_next_token()

        # we expect the current token to be an integer
        left = self.current_token
        self.eat(INTEGER)

        # we expect the current token to be "+" or "-"
        operator = self.current_token
        if operator.type == PLUS:
            self.eat(PLUS)
        
        elif operator.type == MINUS:
            self.eat(MINUS)

        elif operator.type == MULTIPLY:
            self.eat(MULTIPLY)
        
        elif operator.type == DIVIDE:
            self.eat(DIVIDE)
        
        else:
            self.error()

        # we expect the current token to be another integer
        right = self.current_token
        self.eat(INTEGER)



        if operator.type == MINUS:
            return left.value - right.value
        elif operator.type == PLUS:
            return left.value + right.value
        elif operator.type == MULTIPLY:
            return left.value * right.value
        elif operator.type == DIVIDE:
            return left.value / right.value
    
def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)

if __name__ == '__main__':
    main()