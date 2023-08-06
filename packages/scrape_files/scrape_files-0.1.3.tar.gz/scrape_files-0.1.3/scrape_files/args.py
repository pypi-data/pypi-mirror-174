"""Args parsing utilities"""

import sys
import re
import pathlib
import argparse
from urllib.parse import urlparse, unquote


def parse_args():
    parser = argparse.ArgumentParser(
        description="Scrape images in a web page. Save htmls as markdowns."
    )

    sub_parsers = parser.add_subparsers(dest='subparser_name')

    # Add sub-command image 
    parser_image = sub_parsers.add_parser("image", help="download images in a web page")

    # Add positional argument url 
    parser_image.add_argument(
        "url",
        help="a url for scraping",
    )

    # Add optional argument format
    parser_image.add_argument(
        "-f",
        "--format",
        nargs="*",
        default=["jpg", "png", "gif", "svg", "jpeg", "webp"],
        help="enter multiple image formats seperated with space; supported formats: jpg, png, gif, svg, jpeg, webp; defaults to all supported formats",
    )

    # TODO
    # parser_image.add_argument(
    #     "-w",
    #     "--width",
    #     type=int,
    #     default=-1,
    #     help="the height of images to download"
    # )

    # TODO
    # parser_image.add_argument(
    #     "-H",
    #     "--height",
    #     type=int,
    #     default=-1,
    #     help="the width of images to download"
    # )
 
    # Add optional argument dir
    parser_image.add_argument(
            "-d", 
            "--dir", 
            help="name for creating a new directory in current folder"
    )


    # Add sub-command html 
    parser_html = sub_parsers.add_parser("html", help="save one html or multiple htmls from links in <p> tags of a web page as markdown files")

    # Add positional argument url 
    parser_html.add_argument(
        "url",
        help="a url for scraping",
    )
    # Add optional argument level
    parser_html.add_argument(
        "-l",
        "--level",
        default = 1,
        type=int,
        choices=range(1, 3),
        help="1 by default for saving the current page; 2 for links in <p> tags in the current page",
    )
    # Add optional argument dir
    parser_html.add_argument(
            "-d", 
            "--dir", 
            help="name for creating a new directory in current folder"
    )

    if len(sys.argv)==1:
        parser.print_help()
        parser_image.print_help()
        parser_html.print_help()
        sys.exit()

    if sys.argv[1] == "image" and len(sys.argv) == 2:
        parser_image.print_help()
        sys.exit()

    if sys.argv[1] == "html" and len(sys.argv) == 2:
        parser_html.print_help()
        sys.exit()

    args = parser.parse_args()
    return args


def get_url(url):
    if re.match(r"^[a-zA-z]+://", url):
        return unquote(url) 
    else:
        return unquote("https://" + url)


def get_download_dir(url, dir_name):
    if dir_name:
        dir = pathlib.Path(dir_name) 
        return (True, dir)
    else:
        dir = pathlib.Path(urlparse(url).netloc)
        return (False, dir) 
