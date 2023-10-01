import re

# Seu código HTML de entrada
html_input = """
<html>
    <head>
        <title> Compiladores </title>
    </head>
    <body>
        <p style="color:red;background:blue;" id="abc"> Unipinhal </p>
        <br>
    </body>
</html>
"""

# Expressões regulares para reconhecer tags, atributos e conteúdo
tag_pattern = r'<([a-zA-Z0-9]+)(\s[^>]*)?>'
end_tag_pattern = r'</([a-zA-Z0-9]+)>'
attribute_pattern = r'(\w+)="([^"]*)"'
content_pattern = r'>([^<]+)<'

# Função para imprimir o resultado
def print_result(tag, level, attribute=None, value=None, content=None):
    indentation = "    " * level
    if attribute and value:
        print(f"{indentation}Atributo de Tag: {attribute}")
        print(f"{indentation}Valor do Atributo: {value}")
    if content:
        print(f"{indentation}Conteúdo da Tag: {content}")
    print(f"{indentation}Tag de {'abertura' if level % 2 == 0 else 'fechamento'}: {tag}, Nível {level // 2}")

# Analisar o HTML usando expressões regulares
stack = []
level = 0

for line in html_input.split('\n'):
    for match in re.finditer(tag_pattern, line):
        tag, attributes = match.group(1), match.group(2)
        attribute_matches = re.findall(attribute_pattern, str(attributes))
        for attribute, value in attribute_matches:
            print_result(tag, level, attribute, value)
        stack.append((tag, level))
        level += 1

    for match in re.finditer(end_tag_pattern, line):
        tag = match.group(1)
        while stack:
            popped_tag, popped_level = stack.pop()
            print_result(popped_tag, popped_level)
            level -= 1

    for match in re.finditer(content_pattern, line):
        content = match.group(1)
        if content.strip():
            print_result(len(stack), level, content=content.strip())