import requests
import time
import re
from bs4 import BeautifulSoup


https_prox = [
    # 'https://xwczv2:Xx1et0@185.233.81.243:9519'
    # 'https://D0tCNM:zQ95vG@217.29.53.133:45002'
    # 'https://D0tCNM:zQ95vG@217.29.53.133:45001'
    # 'https://D0tCNM:zQ95vG@217.29.62.211:54130'
    # 'https://TM6BqF:HQwNBy@176.107.176.76:36789'
]


def read_inn_from_file(file_name):
    lst = []
    with open(file_name) as file_inn:
        for word in file_inn.readlines():
            lst.append(int(word))

    return lst


def get_url_by_INN(current_INN):
    url = 'https://www.list-org.com/search?type=inn&val={0}'.format(
        current_INN)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'cookies': '_ga=GA1.2.900760651.1582061484; _gid=GA1.2.726897021.1582061484; _gat_gtag_UA_114579997_1=1'
    }
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'cache-control': 'max-age=0',
        'cookie': 'user=5d13c5741a95e45a4ba4; _ga=GA1.2.1060280942.1575472420; _gid=GA1.2.1465796156.1582044594; compare=21_2125853_1978054_2225323_2276727_6039218_1895726_2089525_1760220; PHPSESSID=unobe4niua396akv2l8cjdovu3; _gat_gtag_UA_114579997_1=1',
        'dnt': '1',
        'referer': 'https://www.list-org.com/search?type=inn&val=2536295744',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    }
    r = requests.get(url, headers=headers, timeout=10)
    html = r.content
    soup = BeautifulSoup(html, 'html.parser')
    # try:
    list = soup.find('div', class_='org_list')
    if list is None:
        # exit(0)
        return 'BAN'
    first_p = list.find_all('p')[0]
    a = first_p.find('a')
    # except:
    #     return None

    return a['href']


def get_status_by_url(current_url):
    url = 'https://www.list-org.com{0}'.format(current_url)
    global index
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'cookies': f'_ga=GA1.2.900760651.1582061484; _gid=GA1.2.726897021.1582061484; _gat_gtag_UA_114579997_1=1; user=5e4c57ce9e2489236b{index}'
    }
    r = requests.get(url, headers=headers, timeout=10)
    html = r.content
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', class_='tt')
    if table is None:
        return 'banned'
    regex = re.compile('.*status.*')
    td = table.find('td', class_=regex)
    if td is None:
        return 'no_td'

    return td.text


index = 0


def main():
    INN_LIST = read_inn_from_file('INN_LIST.txt')
    url_file = open('urls.txt', 'w')
    f = open('status_2016.csv', 'a')
    for current_INN in INN_LIST:
        # time.sleep(20)
        global index
        index += 1
        if index == 30:
            break

        new_url = get_url_by_INN(current_INN)
        if new_url == 'BAN':
            print("BAN")
            break
            # exit(0)

        if new_url is None:
            f.write('{0},{1}\n'.format(current_INN, 'no_data'))
            url_file.write('no_url\n')
            url_file.flush()
            continue

        url_file.write(new_url + '\n')
        url_file.flush()
        status = get_status_by_url(new_url)
        f.write('{0},{1}\n'.format(current_INN, '"' + status + '"'))
        f.flush()
        print(str(current_INN) + ' has been processed ' + str(index))
        # time.sleep(2)

    f.close()
    print("Finished parsing")


if __name__ == "__main__":
    main()
