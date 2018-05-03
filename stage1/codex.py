from lxml import html
import requests
import re
import csv

def get_parse(in_folder, out_folder):
    i = 1677
    j=0
    parse_test = []
    with open(in_folder, 'r') as f:
        for line in f:
            i-=1
            if i == 0:
                break

            if 'class="s0 aJ bG"' not in line:
                continue
            beginPos = line.find('style="text-indent: 27pt;')
            #if (beginPos == -1 or line == "\n"):
            #    continue
            #beginPos += 28
            endPos = line.find("</div>")
            text = line[beginPos:endPos]

            text = re.sub('<[^>]*>', '', text)
            text = re.sub('style="text-indent:[^>]*>', '', text)
            text = re.sub('.введена\sФедеральным\sзаконом\sот\s[^\s]*\sN\s.*', '', text)
            text = re.sub('.в\sред.\sФедерального\sзакона\sот\s[^\s]*\sN\s.*', '', text)
            text = re.sub('&quot;','', text)
            text = re.sub('1.\s','',text)
            if text == "":
                continue

            j+=1
            #print(text)
            parse_test.append(text)
            #if (',' in parse_test.pop()):
            #    print("!!!")
    print(j)

    with open('codex.csv', "a") as file:
        writer = csv.writer(file, delimiter='\n')
        writer.writerow(parse_test)
    file.close()


if __name__ == "__main__":
    out_folder = "codexparce.txt"
    ans = get_parse(in_folder = 'codexF.html', out_folder= out_folder)
