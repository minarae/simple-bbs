from bs4 import BeautifulSoup

def remove_html_tags(html):
    # BeautifulSoup 객체를 생성하여 HTML 파싱
    soup = BeautifulSoup(html, 'html.parser')

    # 모든 HTML 태그를 삭제하고 텍스트만 추출
    text = soup.get_text()

    return text
