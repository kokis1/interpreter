typedef struct {
    char * type;
    float value;
} tok;

char * INTEGER = "INTEGER";
char * PLUS = "PLUS";
char * MINUS = "MINUS";
char * MULTIPLY = "MULTIPLY";
char * DIVIDE = "DIVIDE";
char * LPAREN = "LPAREN";
char * RPAREN = "RPAREN";
char * EOF = "EOF";

static int pos = 0;
int * p_pos = &pos;

tok token_array[];