'''this uses reverse polish notation'''

# list of types
INTEGER = "INTEGER"
PLUS = "PLUS"
MINUS = "MINUS"
MULTIPLY = "MULTIPLY"
DIVIDE = "DIVIDE"
S_COLON = "S-_COLON"
EOF = "EOF"

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
        if current_char == ";":
            token_array.append(tok(S_COLON, 0))
            position += 1
            continue
        raise Exception("trouble lexing the text")
    token_array.append(tok(EOF, 0))
    return token_array


def parser(token_array):
    position = 0
    current_token = token_array[position]
    
    if current_token.type != INTEGER:
        raise Exception("expression must start with an INTEGER")
    
    values = []
    while position < len(token_array) and current_token.type == INTEGER:
            values.append(current_token.value)
            position += 1
            current_token = token_array[position]
    
    operator = current_token
    position += 1
    current_token = token_array[position]
    if current_token.type != S_COLON:
        raise Exception("a semi-colon must separate operations")
    
    
    result = values[0]
    values.remove(result)
    for value in values:
        print(result)
        if operator.type == PLUS:
            result += value
        elif operator.type == MINUS:
            result -= value
        elif operator.type == MULTIPLY:
            result *= value
        elif operator.type == DIVIDE:
            result /= value
    return result

def main():
    while True:
        text = input("calc> ")
        if text == "quit":
            break
        else:
            token_array = tokeniser(text)
            result = parser(token_array)
            print(result)
main()