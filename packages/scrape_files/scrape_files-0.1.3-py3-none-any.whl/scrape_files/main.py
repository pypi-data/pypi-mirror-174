"""
`scrape_files` is a tool to help scrape things online to your local machine.
Currently, it supports scraping images in a web page as well as scraping and converting htmls to well-formatted markdowns for easy reading.
"""

import os
import sys
import re
import time
import requests
import concurrent.futures
from threading import Lock
from lxml import etree
import urllib
from urllib.parse import urlparse, urljoin
# from functools import wraps
from fake_user_agent import user_agent


ua = user_agent()
headers = {"User-Agent": ua}

count = 0
total = 0 
ops = ["FETCHING", "RETRY FETCHING", "PARSING", "SAVING"]
base_page_text ="" 
base_page_url = ""


def fetch(url, session, stream=False):
    "Fetch a web page with retry mechanism."

    attempt = 0 
    proxies = requests.utils.getproxies()
    # requests.utils.get_environ_proxies("https://www.google.com")
    
    session.headers.update(headers)
    session.proxies = proxies

    while True:
        try:
            r = session.get(url, timeout=9.05, stream=stream)
        except requests.exceptions.HTTPError as e:
            attempt = call_on_error(e, url, attempt, ops[1])
            continue
        except requests.exceptions.ConnectTimeout as e:
            attempt = call_on_error(e, url, attempt, ops[1])
            continue
        except requests.exceptions.ConnectionError as e:
            attempt = call_on_error(e, url, attempt, ops[1])
            continue
        except requests.exceptions.ReadTimeout as e:
            attempt = call_on_error(e, url, attempt, ops[1])
            continue
        except requests.exceptions.ProxyError as e:
            attempt = call_on_error(e, url, attempt, ops[1])
            continue
        except Exception as e:
            attempt = call_on_error(e, url, attempt, ops[1])
            continue
        else:
            if r.status_code != 200:  # only a 200 response has a response body
                attempt = call_on_error(r.status_code, url, attempt, ops[1])
            return r


def call_on_error(error, url, attempt, op):
    attempt += 1

    logger.debug(f"{op} file from {url} {attempt} times")

    if attempt == 3:
        print(f"Maximum {op} reached: {error}")
        sys.exit()
    return attempt


"""
def fetch_js(url):
    "Fetch the web page with retry mechanism using selenium. 
    Needs to download chromedriver first.
    Only for special use."

    from selenium import webdriver

    attempt = 0 
    while True:
        try:
            driver = webdriver.Chrome()
            driver.get(url)
            page_source = driver.page_source
            driver.quit()
        except http.client.RemoteDisconnected as e:
            attempt = call_on_error(e, url, attempt, ops[1])
            continue
        except Exception as e:
            attempt = call_on_error(e, url, attempt, ops[1])
            continue
        else:
            return page_source 
"""

# Parse links with in <p> tag
def parse_links():
    tree = etree.HTML(base_page_text)

    link_nodes = tree.xpath("//p/a")
    links = []
    for l in link_nodes:
        loc = l.attrib["href"] 
        name = l.text
        if not loc.startswith("http"):
            loc = base_page_url + loc
        pair = (name, loc)
        links.append(pair) 
    return links


def parse_imgs(formats):
    img_list = []
    tree = etree.HTML(base_page_text)
    img_links = tree.xpath("//img/@src")
    if img_links:
        for link in img_links:
            if urlparse(link).path.split(".")[-1] in formats:
                img_list.append(link)
    a_links = tree.xpath("//a/@href | //a/@data-original")
    if a_links:
        for link in a_links:
            if urlparse(link).path.split(".")[-1] in formats:
                img_list.append(link)
    if img_list:
        for index, img in enumerate(img_list):
            img = img.strip()
            if re.match(r"^//.+", img):
                img_list[index] = "https:" + img
            if re.match(r"^/[^/].+", img):
                img_list[index] = urljoin(base_page_url, img)
        img_list = set(img_list) 
        return img_list
    else:
        print("No images found.")
        sys.exit()


def process_dir(dir):
    try:
        os.mkdir(dir)
    except FileExistsError:
        return
    except OSError as e:
        logger.error(str(e))
        sys.exit()


def process_img_path(dir, formats, link):
    process_dir(dir)

    img_name = "_".join(link.split("/")[-2:])
    if "?" in img_name:
        img_name = img_name.split("?")[0]
    if img_name.split(".")[-1] not in formats:
        img_name = img_name + ".jpg"
    img_path = os.path.join(dir, img_name)
    return img_path


def save_img(session, link, dir, formats):
    r = fetch(link, session, stream=True)
    path = process_img_path(dir, formats, link)

    try: 
        with open(path, "wb") as f:  # for stream=True, you have to use with open, otherwise it will generate "write to closed file" error
            for chunk in r:
                f.write(chunk)
        logger.debug("Saved file to %s", path)
    except Exception as e:
        logger.debug(str(e))


def save_to_markdown(session, link, dir=None, level=1, title=None):
    if level == 1:
        text = base_page_text
    else:
        r = fetch(link, session)
        text = r.text

    # This line is only for texts that have html characters as below: 
    # text = text.replace("\n", " ").replace("  ", " ").replace("&nbsp;", "").replace("&#146;", "'").replace("&#151;", "-").replace("&#133;", "...").replace("&#145;", "'")
    
    # Create file path
    if not title:
        match = re.search(r'<title[^>]*>(.*?)(?=</title>)', text, re.S)
        if match:
            title_raw = match.group().split(">")[1]
        else:
            title = "untitled"
  
    # Transform Chiness punctuation marks to english ones, for better file naming and terminal displaying
    # The syntax only allows the key in the dictionary to be one character long
    trans_pattern = str.maketrans({"’": "'", "—": "-", "…": "...", "‘": "'", "：": ":", "，": ",", "？": "?"})
    title = title_raw.translate(trans_pattern)

    # Get rid of symbols from title
    title = title.replace(",", "").replace(" ", "_").replace("__", "_").replace(".", "").split("?")[0].split(":")[0].strip('"').strip("'").title()
    
    path = title + ".md"

    if dir:
        process_dir(dir)
        path = os.path.join(dir, path)

    # Narrow down to article node if any
    article = re.search(r'<article(.*?)</article>', text, re.S)
    if article:
        tree = etree.HTML(article.group())
    else:
        tree = etree.HTML(text)

    # Write to file
    try:
        with open(path, "w") as f:

            if title != "untitled":
                f.write(title_raw)
                f.write("\n---\n\n")

            # Xpath will sort the returned list according the order in the source
            sentences = tree.xpath("//p[not(img) and not(parent::blockquote) and not(ancestor::aside)] | //h1 | //h2 | //h3 | //blockquote[not(parent::aside)] | //img[not(parent::noscript) and not(ancestor::aside) and not(ancestor::span)] | //hr")
            for s in sentences:
                tag = s.tag
                if tag == "p": 
                    text = list(s.itertext())
                    if text[0][0] == " ":
                        text[0] = text[0][1:]
                    if not text:
                        continue
                    else:
                        for i in text:
                            f.write(i)
                        f.write("\n\n")
                if tag == "h1": 
                    f.write("# ")
                    for i in s.itertext():
                        f.write(i)
                    f.write("\n\n")
                if tag == "h2":
                    f.write("## ")
                    for i in s.itertext():
                        f.write(i)
                    f.write("\n")
                if tag == "h3":
                    f.write("### ")
                    for i in s.itertext():
                        f.write(i)
                    f.write("\n")
                if tag == "blockquote":
                    f.write("> ")
                    for i in s.itertext():
                        if i != " ":
                            f.write(i)
                    f.write("\n\n")
                if tag == "img":
                    if "data-original" in s.keys():
                        f.write("![image]" + "(" + s.attrib["data-original"] + ")" + "\n\n")
                    elif "src" in s.keys():
                        if "data-actualsrc" in s.keys():
                            loc = s.attrib["data-actualsrc"]
                        else:
                            loc = s.attrib["src"]

                        if loc.startswith("http"):
                            f.write("![image]" + "(" + loc + ")" + "\n\n")
                        else:
                            f.write("![image]" + "(" + link + loc + ")" + "\n\n")
                if tag == "hr":
                    f.write("---\n\n")

            f.write("\n---\nSource: " + link)
        logger.debug("Saved file to %s", path)
    except Exception as e:
        logger.debug(str(e))


def download():
    args = parse_args()
    url = get_url(args.url)

    lock = Lock()
    global base_page_text
    global base_page_url
    global total
    global count

    with requests.Session() as session:

        print(f"{ops[0]} {url} ...")
        response = fetch(url, session)
        base_page_text = response.text
        base_page_url = url

        if args.subparser_name == "image":
            formats = args.format
            _, dir = get_download_dir(url, args.dir)

            print(f"{ops[2]} {url} ...")
            
            img_list = parse_imgs(formats)
            total = len(img_list)
            print(f"FOUND {total} files")
            print(f"{ops[3]} files ...")
            update(count, total)
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                for link in img_list:
                    executor.submit(save_img, session, link, dir, formats)
                    lock.acquire()
                    count += 1
                    lock.release()
                    update(count, total)

        if args.subparser_name == "html":
            level = args.level
            check, dir = get_download_dir(url, args.dir)

            if level == 1:
                print(f"{ops[2]} {url} ...")
                total += 1 
                print(f"FOUND {total} files")
                print(f"{ops[3]} files ...")
                update(count, total)
                if check:
                    save_to_markdown(session, base_page_url, dir)
                else:
                    save_to_markdown(session, base_page_url)
                count += 1
                update(count, total)

            if level == 2:
                print(f"{ops[2]} {url} ...")
                link_list = parse_links()
                total = len(link_list)
                print(f"FOUND {total} files")
                print(f"{ops[3]} files ...")
                update(count, total)
                with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                    for i in link_list:
                        title = i[0]
                        link = i[1]
                        executor.submit(save_to_markdown, session, link, dir, level, title)
                        lock.acquire()
                        count += 1
                        lock.release()
                        update(count, total)

    print("DONE!")
    print(f"DOWNLOADED {count} files")
    print(f"FAILED: {total - count}")


def timer(func):
    # @wraps(func)
    def wrapper(*args, **kwargs):
        start_at = time.time()
        f = func(*args, **kwargs)
        time_taken = time.time() - start_at
        print(f"Time taken: {round(time_taken, 2)} seconds")
        return f

    return wrapper


@timer
def main():
    try:
        download()
    except KeyboardInterrupt:
        print("\nCancelled out by user.")


if __name__ == "__main__":
    import os
    import sys

    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    from scrape_files.args import parse_args, get_url, get_download_dir
    from scrape_files.progressbar import update
    from scrape_files.log import logger

    main()

else:
    from .args import parse_args, get_url, get_download_dir
    from .progressbar import update
    from .log import logger

