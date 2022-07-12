from ply_3_11.ply.lex import lex

#* Analizador lexico usando ply del lenguaje parecido a C o conocido como simple C

class MiLexico():

    # * Palabras reservadas
    p_reservadas = {
        'if': 'IF',
        'else': 'ELSE',
        'do': 'DO',
        'while': 'WHILE',
        'void': 'VOID',
        'return': 'RETURN',
        'int': 'INT',
        'double': 'DOUBLE',
        'string': 'STRING',
        'boolean': 'BOOLEAN',
    }

    # * Lista de nombre de tokens

    tokens = [
        'PUNTOCOMA',
        'ASIGNACION',
        'PUNTO',
        'COMA',
        'SUMA',
        'RESTA',
        'MULTIPLICACION',
        'DIVISION',
        'RESTO',
        'IGUALACION',
        'DIFERENCIACION',
        'MAYORQUE',
        'MAYOR_IGUAL',
        'MENORQUE',
        'MENOR_IGUAL',
        'AND',
        'OR',
        'NOT',
        'PARA',
        'PARC',
        'CORA',
        'CORC',
        'CADENA',
        'CHAR',
        'ID'
    ] + list(p_reservadas.values())

    # * Regular expression rules for simple tokens
    t_PUNTOCOMA = r';'
    t_ASIGNACION = r'='
    t_PUNTO = r'\.'
    t_COMA = r','
    t_SUMA = r'\+'
    t_RESTA = r'-'
    t_MULTIPLICACION = r'\*'
    t_DIVISION = r'/'
    t_RESTO = r'%'
    t_NOT = r'!'
    t_PARA = r'\('
    t_PARC = r'\)'
    t_CORA = r'{'
    t_CORC = r'}'
    t_IGUALACION = r'=='
    t_DIFERENCIACION = r'!='
    t_MAYORQUE = r'>'
    t_MENORQUE = r'<'
    t_MAYOR_IGUAL = r'>='
    t_MENOR_IGUAL = r'<='
    t_AND = r'&&'
    t_OR = r'\|\|'

    # A regular expression rule with some action code
    # Note addition of self parameter since we're in a class
    def t_INT(self, t):
        r'\d+'
        try:
            t.value = int(t.value)
        except ValueError:
            print("Integer value too large %d", t.value)
            t.value = 0
            print("Integer value:", t.value)
        return t

    def t_DOUBLE(self, t):
        r'\d+\.\d+'
        try:
            t.value = float(t.value)
        except ValueError:
            print("Floaat value too large %d", t.value)
            t.value = 0
        return t

    def t_ID(self, t):  # * Check for reserved words
        r'[a-zA-Z_]+[a_zA-Z_0-9]*'
        t.type = self.p_reservadas.get(t.value.lower(), 'ID')
        return t

        # * A regular expresion rule for strings
    def t_CADENA(self, t):
        r'\".*?\"'
        t.value = t.value[1:-1]  # *Se remueven las comillas dobles
        return t

    # * Comentario de multiples lineas /*...*/
    def t_COMENTARIO_MULTILINEA(self, t):
        r'/\*(.|\n)*?\*/'
        t.lexer.lineno += t.value.count('\n')

    # * Comentario simple //...
    def t_COMENTARIO_SIMPLE(self, t):
        r'//.*\n'
        t.lexer.lineno += 1

    # * Define a rule so we can track line numbers
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")

    # * A string containing ignored characters (spaces and tabs)
    t_ignore = ' \t'

    # * Error handling rule
    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # * Build the lexer
    def build(self, **kwargs):
        self.lexer = lex(module=self, **kwargs)

    # Test it output
    def test(self, data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print(tok)

# * Build the lexer and try it out
"""
*t.type  -->Tipo de token
*t.value -->Lexema del token
*t.lineno -->Linea del token
*t.lexpos -->Columna del token
"""

m = MiLexico()
m.build()  # * Build the lexer
m.test("""
int _miIdentificador = 5;

if (_miIdentificador == 5) {
    _miIdentificador = _miIdentificador + 4;
} else {
    _miIdentificador = _miIdentificador * 50.25;
}

double valorDouble = 25.5;

if (valorDouble <= 27) {
    valorDouble = valorDouble - 25;
} else {
    valorDouble = valorDouble / 3;
}
""")  # *Test it
