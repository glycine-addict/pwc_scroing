import requests
import time
from bs4 import BeautifulSoup


def read_inn_from_file(file_name):
    lst = []
    with open(file_name) as file_inn:
        for word in file_inn.readlines():
            lst.append(int(word))

    return lst


if __name__ == "__main__":
    INN_LIST = read_inn_from_file('unique_INN.txt')
    f = open('CEO.csv', 'a')
    index = 0
    for CURRENT_INN in INN_LIST:
        CURRENT_INN = str(CURRENT_INN)
        if len(CURRENT_INN) == 9:
            CURRENT_INN = '0' + CURRENT_INN
        url = 'http://online.igk-group.ru/ru/home?&inn={0}'.format(CURRENT_INN)
        r = requests.get(url)
        html = r.content
        soup = BeautifulSoup(html, 'html.parser')
        index += 1
        if index == 5:
            break
        try:
            main_div = soup.find('div', {"id": "tab1"})
            main_table = main_div.find_all("table")[1]
            # status = main_table.find_all("td")[1].text.split()
            # f.write('{0},{1},{2}\n'.format(CURRENT_INN, '"' +
            #                                ' '.join(map(str, status[2:])) + '"', '"' + status[1][:-1] + '"'))
            ceo_name = main_table.find_all("td")[3].text.split()
            f.write('{0},{1}\n'.format(CURRENT_INN,
                                       '"' + ' '.join(map(str, ceo_name)) + '"'))
            if index % 1000 == 0:
                print(index, 'processed')

            f.flush()
        except:
            f.write('{0},{1}\n'.format(CURRENT_INN, 'error'))
            f.flush()
    f.close()
    print("Finished parsing")
    f = open('finish.txt', 'w')
    f.close()
