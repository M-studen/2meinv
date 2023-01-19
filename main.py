# coding:utf-8

import requests_html
import requests
#导库

session=requests_html.HTMLSession()
def get_html_links(session):
    #获取最大页数
    max_page=int(session.get("https://2meinv.com").html.xpath("/html/body/div[4]/div[1]/div[2]/div/a[6]",clean=True)[0].search('https://www.2meinv.com/index-{}.html')[0])
    #获取每页的所有图片及其指向的地址并返回
    for page in range(1,max_page+1):
        res = session.get('https://www.2meinv.com/index-{}.html'.format(page))
        page+=1
        for link in res.html.find(".dl-pic"):
            yield link.attrs['href']
def get_img_links(html_links):
    for url in html_links:
        session=requests_html.HTMLSession()
        r=session.get(url)
        #获取页面中的描述及图片
        img_ele=r.html.xpath("/html/body/div[5]/a/img")[0]
        img_attr=img_ele.attrs
        img_link=img_attr['src']
        img_desc=img_attr['alt']
        img=(img_link,img_desc)
        yield img


def doweload_img(img):
    for i in img:
        res=requests.get(i[0]).content
        with open(file="dowe/{}.jpg".format(i[1]),mode="wb")as f:
            f.write(res)
            print(i[1])
def main():
    doweload_img(get_img_links(get_html_links(session)))

if __name__=="__main__":
    main()


