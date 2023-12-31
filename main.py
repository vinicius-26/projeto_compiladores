import re
from collections import deque

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
    print(f"{indentation}Tag de {'abertura' if level % 2 == 0 else 'fechamento'}: {tag}, Nível {level}")

# Imprimir a tag HTML de abertura antes de entrar no loop
print_result("html", 0)
print_result("head", 1)  # Adicione esta linha para imprimir a tag <head>

# Analisar o HTML usando expressões regulares
stack = []
level = 2  # Inicia em 2 para refletir o nível correto da tag <body>

# Usando uma fila para armazenar as tags de fechamento na ordem correta
closing_tags_queue = deque()

for line in html_input.split('\n'):
    for match in re.finditer(tag_pattern, line):
        tag, attributes = match.group(1), match.group(2)
        attribute_matches = re.findall(attribute_pattern, str(attributes))
        is_opening_tag = not tag.startswith('/')

        if is_opening_tag:
            print_result(tag, level, attribute=None, value=None)
            stack.append((tag, level))
            level += 1

    for match in re.finditer(end_tag_pattern, line):
        tag = match.group(1)
        is_closing_tag = tag.startswith('/')

        if is_closing_tag:
            closing_tags_queue.append(tag)

    for match in re.finditer(content_pattern, line):
        content = match.group(1)
        if content.strip():
            print_result(len(stack), level, content=content.strip())

# Imprimir as tags de fechamento na ordem correta
while closing_tags_queue:
    tag = closing_tags_queue.popleft()
    print_result(tag, level - 1)  # Nível diminuído para corresponder à tag de fechamento
    level -= 1