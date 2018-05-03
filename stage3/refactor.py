import re

ans = []
with open ('training_expr.txt', 'r') as f:
    for line in f:
        line = re.sub(' O\n|B-LOC|I-ORG|B-ORG|B-PER|I-PER|\n', '', line)
        if '.' in line:
            ans.append(line + '\n')
        if line != ' ':
            ans.append(line)
to_file = ' '.join(ans)
print(to_file)