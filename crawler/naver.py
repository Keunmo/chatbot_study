
import requests
from bs4 import BeautifulSoup

def get_page_detail(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            'accept-encoding': 'gzip',
            'accept-language': 'ko,en-US;q=0.9,en;q=0.8,ko-KR;q=0.7,fr;q=0.6,zh-TW;q=0.5,zh;q=0.4,ja;q=0.3',
        }
        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            print(f'failed, {r.status_code}')
            return None
        with open('naver_detail.html', 'w', -1, 'utf-8') as f:
            f.write(r.text)
        return r.text
    except Exception as e:
        print (e)

def get_list_page(start_dt, end_dt, keyword, start):
    start_dt_s = start_dt.replace('.', '')
    end_dt_s = end_dt.replace('.', '')
    p = f'from{start_dt_s}to{end_dt_s}' 
    try:
        url = f'https://search.naver.com/search.naver?&where=news&query={keyword}&sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=3&ds={start_dt}&de={end_dt}&docid=&nso=so:r,p:{p},a:all&mynews=0&cluster_rank=31&start={start}&refresh_start=0'
        r = requests.get(url)
        if r.status_code != 200:
            print(f'failed, {r.status_code}')
            return None
        with open('naver.html', 'w', -1, 'utf-8') as f:
            f.write(r.text)
        return r.text
    except Exception as e:
        print(e)

def crawl(target_dt, keyword):
    start_dt = f'{target_dt}.01'
    end_dt = f'{target_dt}.31'
    start = 1
    scraped_count = 0
    filename = start_dt.replace('.', '') + '.txt'
    with open(filename, 'w') as f:
        pass
    while True:
        if scraped_count > 100:
            break

        text = get_list_page(start_dt, end_dt, keyword, start)
        soup = BeautifulSoup(text, 'html.parser')

        # 마지막 페이징 버튼이 활성화 되어있다면 마지막 페이지다
        elements = soup.select('.sc_page .sc_page_inner a.btn')
        last_el = elements[-1]
        pressed = last_el.get('aria-pressed')
        if pressed == 'true':
            break

        urls = []
        # news
        elements = soup.select('.list_news a.info')
        for el in elements:
            href = el.get('href')
            if href.find('news.naver.com/main/read.nhn') >= 0:
                urls.append(href)

        # sub_news
        elements = soup.select('.list_news a.sub_txt')
        for el in elements:
            href = el.get('href')
            if href.find('news.naver.com/main/read.nhn') >= 0:
                urls.append(href)

        for (index, url) in enumerate(urls):
            print (index, url)
            text = get_page_detail(url)
            soup = BeautifulSoup(text, 'html.parser')
            elements = soup.select('#articleTitle')
            if not elements:
                continue
            title = elements[0].text

            elements = soup.select('#articleBodyContents')
            if not elements:
                continue
            content = elements[0].text.strip()
            with open(filename, 'a', -1, 'utf-8') as f:
                f.write(content+'\n')
            scraped_count += 1

        print ('start: ', start)
        print ('scraped_count: ', scraped_count)
        start += 10

if __name__ == '__main__':
    crawl('2020.12', '코로나')