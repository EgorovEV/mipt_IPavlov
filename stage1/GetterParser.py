from lxml import html
import requests

class GetParse():
    def get_parse(self, url, out_folder):
        with open(out_folder, 'a') as f:
            for page_number in range(1,50):
                print(page_number)
                cur_url = url + '?p=' + str(page_number)
                page = requests.get(cur_url)
                tree = html.fromstring(page.content)

                links = set(tree.xpath("//h3//a[@class='item-description-title-link']/@href"))

                for post_page in links:
                    cur_page = requests.get('https://www.avito.ru' + post_page)
                    cur_tree = html.fromstring(cur_page.content)
                    f.write(str(cur_tree.xpath('//div[@class="item-description-text"]//p/text()'))+'\n')

def textrefactor(filename):
    ans = []
    with open(filename, 'r') as var:
        for line in var:
            myline = ' '.join(line.split())
            ans.append(myline)

    with open('avitodata.txt', 'a') as f1:
        for s in ans:
            if ('[]' in s):
                continue
            f1.write(s + '\n')


if __name__ == "__main__":
    out_folder = "avitotest.txt"
    gp = GetParse()
    ans = gp.get_parse(url = 'http://www.avito.ru/moskva/nedvizhimost', out_folder= out_folder)
    textrefactor(filename = out_folder)
