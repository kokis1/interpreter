'''this is a simpler version of the calculator interpreter that can handle bidmas'''

# list of types
INTEGER = "INTEGER"
PLUS = "PLUS"
MINUS = "MINUS"
MULTIPLY = "MULTIPLY"
DIVIDE = "DIVIDE"
EOF = "EOF"
LEFT_PARENTHESIS = "LEFT_PARENTHESIS"
RIGHT_PARENTHESIS = "RIGHT_PARENTHESIS"
WORD = "WORD"

class tok:
    '''basically a struct holding a type and a value for each token'''
    def __init__(self, type, value):
        self.type = type
        self.value = value
    def __str__(self):
        return "TOKEN({type}, {value})".format(type=self.type, value=self.value)
    
    def __repr__(self):
        return self.__str__()


def integer(text, position):
    result = ""
    while position < len(text):
        current_char = text[position]
        if current_char.isdigit():
            result += current_char
            position += 1
        else:
            break
    return int(result), position - 1

def word(text, position):
    result = ""
    current_char = "a"
    while position < len(text):
        current_char = text[position]
        if current_char.isalpha():
            result += current_char
            position += 1
        else:
            break
    return result, position - 1


def tokeniser(text):
    position = 0
    token_array = []
    current_char = text[position]
    while position < len(text):
        current_char = text[position]
        if current_char == " ":
            position += 1
            continue
        if current_char.isdigit():
            result, position = integer(text, position)
            token_array.append(tok(INTEGER, result))
            position += 1
            continue
        if current_char.isalpha():
            result, position = word(text, position)
            token_array.append(tok(WORD, result))
            position += 1
            continue
        if current_char == "+":
            token_array.append(tok(PLUS, 0))
            position += 1
            continue
        if current_char == "-":
            token_array.append(tok(MINUS,0))
            position += 1
            continue
        if current_char == "*":
            token_array.append(tok(MULTIPLY, 0))
            position += 1
            continue
        if current_char == "/":
            token_array.append(tok(DIVIDE, 0))
            position += 1
            continue
        if current_char == "(":
            token_array.append(tok(LEFT_PARENTHESIS, 0))
            position += 1
            continue
        if current_char == ")":
            token_array.append(tok(RIGHT_PARENTHESIS, 0))
            position += 1
            continue
        raise Exception("trouble lexing the text")
    token_array.append(tok(EOF, 0))
    return token_array

def factor(token_array, position):
    current_token = token_array[position]
    if current_token.type == INTEGER:
        result = current_token.value
        position += 1
        current_token = token_array[position]
        return result
    elif current_token.type == LEFT_PARENTHESIS:
        position += 1
        current_token = token_array[position]
        result = expr(token_array, position)
        position += 1
        current_token = token_array[position]
        if current_token.type == RIGHT_PARENTHESIS:
            return result
        else:
            raise Exception("expected a parenthesis")
    
def term(token_array, position):
    result = factor(token_array, position)
    current_token = token_array[position]
    while current_token.type in (MULTIPLY, DIVIDE) and position < len(token_array):
        if current_token.type == MULTIPLY:
            position += 1
            current_token = token_array[position]
            result = result * factor(token_array, position)
        elif current_token.type == DIVIDE:
            position += 1
            current_token = token_array[position]
            result = result / factor(token_array, position)
    return result

def expr(token_array, position):
    result = term(token_array, position)
    current_token = token_array[position]
    while current_token.type in (PLUS, MINUS) and position < len(token_array):
        if current_token.type == PLUS:
            position += 1
            current_token = token_array[position]
            result = result + term(token_array, position)
        elif current_token.type == MINUS:
            position += 1
            current_token = token_array[position]
            result = result - term(token_array, position)
    return result

def parser(token_array):
    position = 0
    return expr(token_array, position)

def main():
    while True:
        text = input("calc> ")
        if text != "quit":
            token_array = tokeniser(text)
            result = parser(token_array)
            print(result)
        else:
            print("exiting the lexer")
            break
main()