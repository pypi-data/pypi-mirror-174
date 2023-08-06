`scrape_files` is a tool to help scrape things online to your local machine.
Currently, it supports scraping and converting htmls to well-formatted markdowns for easy reading as well as scraping and downloading images of various formats in a web page. 

### Scraping htmls to your local machine
The html parsing logic is similar to a browser's easyread extension's, which trims off all the unnecessary decorations from a web page, only keeping the title and the article content. The main difference is that the file is downloaded as pretty formatted markdown.

Also support scraping links under the `<p>` tag in the current page concurrently.

Terminal usage:
```bash
scrape html <url>     # specify a url for scraping
scrape html <url> -d  # specify a directory name for saving files in current folder
scrape html <url> -l  # specify a level: 1 by default for the current page; 2 for links in the current page
```

### Scraping images to your local machine
Images are scraped and downloaded concurrently. Supported formats: jpg, png, gif, svg, jpeg, webp; defaults to all supported formats.

Terminal usage:
```bash
scrape image <url>     # specify a url for scraping
scrape image <url> -d  # specify a diretory name for saving files in current folder 
scrape image <url> -f  # specify image formats separated with space 
```

# Installation
```python
pip install scrape_files
```
