import re
import csv
quoter = re.compile(r"(«|»|“|”|``|')")
tokenizer = re.compile(r"[\w']+|[^\w ]")

def tokenize(s):
   return tokenizer.findall(quoter.sub('"', s))

ans = []
ans_orig = []

def write_trainig_tokenize():
    with open("training.txt", 'r') as f:
        for line in f:
            ans_orig.append(line)
            print(' '.join(tokenize(line)))
            ans.append(' '.join(tokenize(line)))
    print(ans[0])

    with open("trainig_tokenize.txt", 'w') as f:
        for line in ans:
            f.write(line)


write_trainig_tokenize()

with open('toloka_train_persons.tsv', "w") as file:
    writer = csv.writer(file, delimiter='\t')
    writer.writerow(['INPUT:orig', 'INPUT:input'])
    for index, line_orig in enumerate(ans_orig):
        writer.writerow([line_orig, ans[index]])


