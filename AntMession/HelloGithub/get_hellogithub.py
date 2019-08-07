import requests
from lxml import etree
import better_exceptions
better_exceptions.MAX_LENGTH = None


"""
urls get to solve
"""
SERVER_JIANG = "https://sc.ftqq.com/SCU32752T6502483b771545702dac3da079b713c15ba846f60c8e8.send?"
base_url = "https://hellogithub.com"


def into_detail(value):
    """
    format value of each detail from elements into markdown content
    :prama: value: detail of github project
    :return: formatted content
    """
    return value + " "


def into_href(value, a_total):
    """
    format href and text of each "a" element into markdown content
    :prama: value: a tuple include text() and href() of "a" element
    :prama: a_total: a list of all "a" element arguements, including text and href
    :return: a list element of markdown content
    """
    if a_total.index(value) == 0:
        return  """
""" + str(a_total.index(value) + 1) + '. ' + '['+value[0] + '](' +value[1] + """)
"""
    else:
        return """
""" + str(a_total.index(value) + 1) + '. ' + '[' + value[0] + '](' + value[1] + """)
"""


def get_hello_github():
    """
    main function to get the html page from hello github,
    and send to my wechat through SERVER jiang,
    if the function get some Exception,
    catch the Exception as e, and send it to my wechat
    """
    try:
        # get the home page source and find the content url by xpath
        home_resp = requests.get(base_url)
        home_html = home_resp.text
        sel = etree.HTML(home_html)
        tar_xpath = "//a[@id='volume-button']/@href"
        # get the content url
        target_url = base_url + sel.xpath(tar_xpath)[0]
        num = target_url.split('/')[-2]

        # request the content page, create a selector
        tar_resp = requests.get(target_url)
        target_html = tar_resp.text
        tree = etree.HTML(target_html)

        detail_p_xpath = '//*[@id="main"]/div[4]/p'
        a_xpath = '//*[@id="github_url"]/@href'
        a_text_xpath = '//*[@id="github_url"]//text()'

        """
        get the "p" element and
        href of github project from "a" element as list through the html page
        """
        p_list = tree.xpath(detail_p_xpath)
        a_href = tree.xpath(a_xpath)
        a_text = tree.xpath(a_text_xpath)
        # zip href of "a" element and
        # content of "a" element into dict
        a_dic = dict(zip(a_text, a_href))

        # turn a_dic into a list including a tuple of content and
        # href of "a" element
        a_total = list(a_dic.items())

        detail_list = []
        for i in p_list:
            detail_li = i.xpath(".//text()")
            detail_list.append("".join(detail_li))

        # defind a base string to send to wechat
        content_to_send = ''
        for k, v in dict(zip(a_total, detail_list)).items():
            v = ''.join(v.split())
            v = v.replace('#', 'sharp')
            content_to_send = content_to_send + into_href(k, a_total) + into_detail(v)

        data = {
            'text': 'hello github 第{}期'.format(num),
            'desp': content_to_send
        }
        requests.post(SERVER_JIANG, data=data)
    except Exception as e:
        data = {
            'text': 'somthing wrong',
            'desp': e
        }
        requests.post(SERVER_JIANG, data=data)

if __name__ == "__main__":
    """
    run the main function and get the knowledge boom boom boom
    """
    get_hello_github()
