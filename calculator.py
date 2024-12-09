# token types
# EOF is the end of file token, indicating that there is no more input for the lexical analysis


INTEGER, PLUS, EOF, WHITESPACE = "INTEGER", "PLUS", "EOF", "WHITESPACE"

class Token(object):
    def __init__(self, type, value):
        # token type: integer, plus or eof
        self.type = type
        # token value = 0, 1,...,9 "+" or "eof"
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
    def error(self):
        raise Exception("Error parsing input")
    
    def get_next_token(self):
        '''lexical analyser, also known as a scanner or tokenizer
        This method breaks a sentence apart into tokens, one token at a time'''

        text = self.text


        # is self.pos index is past the end of the self.text?
        # if so, then return EOF token because there is no more
        # input left to convert into tokens
        if self.pos > len(text) - 1:
            return Token(EOF, None)
        # get a character at the position self.pos and decide what token to create based on the character
        current_char = text[self.pos]

        if current_char.isdigit():
            token = Token(INTEGER, int(current_char))
            self.pos += 1
            return token

        if current_char == "+":
            token = Token(PLUS, current_char)
            self.pos += 1
            return token
        
        
        if current_char == " ":
            token = Token(WHITESPACE, current_char)
            self.pos += 1
            return token
        
        self.error()
    
    def eat(self, token_type):
        '''compare the current token type with the passed token type and if the match then 
        eat the current token and assign the next token to the self.current_token, otherwise raise an exception'''

        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()
    
    def expr(self):
        '''expr -> INTEGER PLUS INTEGER'''
        # set the current token to the first token taken from the input

        self.current_token = self.get_next_token()

        '''# we expect the current token to be a single digit integer
        left = self.current_token
        self.eat(INTEGER)

        # we expect the current token to be a "+"
        op = self.current_token
        self.eat(PLUS)

        # we expect the current token to be a single digit integer
        right = self.current_token
        self.eat(INTEGER)'''

        

        # using a simple stack memory to allow integers of many digits to be added together, and allowing multiple additions
        stack = []
        while True:
            if self.current_token.type == INTEGER and stack == []:
                stack.append(self.current_token)
                self.eat(INTEGER)
            
            elif self.current_token.type == INTEGER and stack != []:
                integer = stack.pop()
                next_digit = self.current_token
                new_number = 10*integer.value + next_digit.value
                token = Token(INTEGER, new_number)
                stack.append(token)
                self.eat(INTEGER)
            
            elif self.current_token.type == PLUS and stack != []:
                stack.append(Token(INTEGER, 0))
                self.eat(PLUS)
            
            elif self.current_token.type == WHITESPACE:
                self.eat(WHITESPACE)
            
            elif self.current_token.type == EOF:
                break
        # after the above call the self.current_token is set to
        # EOF token

        # at this point INTEGER PLUS INTEGER sequence of tokens
        # has been successfully found and the method can just
        # return the result of adding two integers, thus
        # effectively interpreting client input


        # we are only working with addition, so adding up the stack and returnning the result will be good
        total = 0
        for index in range(0, len(stack)):
            total += stack[index].value
        return total
    
def main():
    while True:
        try:
            text = input('calc>')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)

if __name__ == '__main__':
    main()