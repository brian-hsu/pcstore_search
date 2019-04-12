import requests
from requests.adapters import HTTPAdapter
from pyquery import PyQuery as pq


def main():
    obj = PCstoreSearch()
    search_keyword = input(u'輸入關鍵字搜索:')
    obj.post_pcstore(search_keyword)

    for item in obj.collect_item_list():
        print(item)


def request_post_session(URL, Headers, Data, Encode):
    s = requests.Session()
    s.mount(URL, HTTPAdapter(max_retries=3))

    try:
        resp = s.post(url=URL, timeout=10, headers=Headers, data=Data)

        if resp.status_code == 200:
            resp.encoding = Encode
        else:
            resp = None

    except Exception as ex:
        print(ex)
        resp = None

    return resp


class PCstoreSearch:
    def __init__(self):
        self.pq_pcstore = None
        self.result = list()

    def post_pcstore(self, k_word):
        url = 'https://www.pcstore.com.tw/adm/psearch.htm'

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                   'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
                   }

        data = {'store_k_word': k_word.encode('big5'),
                  'page_count': '20',
                  'slt_k_option': '1'
                }

        pcstore_response = request_post_session(url, headers, data, 'big5')

        if pcstore_response:
            self.pq_pcstore = pq(pcstore_response.text)
        else:
            print('Request pcstore page response error')
            exit(0)

    def collect_item_list(self):
        result = list()

        pic2_a = pq(self.pq_pcstore('#mainContent1').find('.pic2t.pic2t_bg>a'))
        if len(pic2_a) == 0:
            print(u'搜索不到此商品')
            exit(0)
        else:
            for i in range(len(pic2_a)):
                pic2_a_font = pic2_a.eq(i).find('font')

                for j in range(len(pic2_a_font)):
                    pic2_a_font.eq(j).before(pic2_a_font.eq(j).text())

                pic2_a_font.remove()
                result.append(pic2_a.eq(i).text())

            return result


if __name__ == '__main__':
    main()
