import os
import json
import base64
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from PyPDF2 import PdfMerger

def filename_from_url(url):
    """Extracts a valid filename from a URL."""
    if url.endswith('/'):
        url = url[:-1]  # Remove trailing slash if present
    return url.split('/')[-1]  # Use the last part of the URL as filename

def extract_article_links(url, driver):
    """Extracts article links from a webpage."""
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    article_links = [urljoin(url, a['href']) for a in soup.find_all('a', href=True) if '/article/' in a['href']]
    return article_links

def save_article(url, output_folder, driver):
    """Saves the webpage content after removing specified elements and formatting."""
    try:
        driver.get(url)

        # JavaScript for DOM manipulation
        js_script = """
        document.querySelectorAll(
          'script, .header, footer, head, iframe, .related-articles, .comment-callout, .article-author, .article-subscribe, .article-sidebar, .sub-nav, .skip-navigation, .articleRatings, aside'
        ).forEach(el => el.remove());
        """
        driver.execute_script(js_script)

        # Fetch the modified page source
        content = driver.page_source

        # Parse the content with BeautifulSoup
        soup = BeautifulSoup(content, 'html.parser')

        # Update image URLs to be full URLs
        for img in soup.find_all('img', src=True):
            img['src'] = urljoin(url, img['src'])

        # Ensure the output folder exists
        os.makedirs(output_folder, exist_ok=True)

        # File path creation for HTML
        filename = filename_from_url(url) + '.html'
        file_path = os.path.join(output_folder, filename)

        # Writing HTML content to file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(str(soup))
        print(f"Successfully saved HTML: {file_path}")

        # Save as PDF
        pdf_file_path = os.path.join(output_folder, filename + '.pdf')
        save_pdf(driver, pdf_file_path)

        # Save as plain text
        text_file_path = os.path.join(output_folder, filename + '.txt')
        save_plain_text(str(soup), text_file_path)

        return file_path, pdf_file_path, text_file_path

    except Exception as e:
        print(f"Failed to save {url}: {str(e)}")
        return None, None, None

def save_pdf(driver, path):
    """Saves the current page as PDF using the PDF options."""
    pdf_options = {
        'printBackground': True,
        'displayHeaderFooter': False,
        'pageRanges': '1-5',  # Adjust as necessary
        'format': 'A4'
    }
    result = driver.execute_cdp_cmd("Page.printToPDF", pdf_options)
    
    # Decode the Base64 encoded PDF and save to file
    data = base64.b64decode(result['data'])
    with open(path, 'wb') as f:
        f.write(data)
    print("PDF successfully saved.")

def save_plain_text(html_content, path):
    """Extracts and saves plain text from HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text()
    with open(path, 'w', encoding='utf-8') as file:
        file.write(text)
    print(f"Plain text successfully saved: {path}")

def setup_driver():
    """Configures and returns a Selenium WebDriver with specified options."""
    driver = uc.Chrome()
    return driver

def main(urls, output_folder):
    """Main function to process each category URL and save articles."""
    driver = setup_driver()
    article_data = {}
    combined_html = ""
    combined_text = ""
    combined_pdf_paths = []

    for url in urls:
        # Extract article links for each category URL
        article_links = extract_article_links(url, driver)
        article_data[url] = article_links

        # Save each article
        for article_url in article_links:
            html_path, pdf_path, text_path = save_article(article_url, output_folder, driver)
            if html_path and text_path:
                with open(html_path, 'r', encoding='utf-8') as file:
                    combined_html += file.read()
                with open(text_path, 'r', encoding='utf-8') as file:
                    combined_text += file.read()
                combined_pdf_paths.append(pdf_path)

    # Save combined HTML
    combined_html_path = os.path.join(output_folder, 'combined.html')
    with open(combined_html_path, 'w', encoding='utf-8') as file:
        file.write(combined_html)
    print(f"Combined HTML successfully saved: {combined_html_path}")

    # Save combined plain text
    combined_text_path = os.path.join(output_folder, 'combined.txt')
    with open(combined_text_path, 'w', encoding='utf-8') as file:
        file.write(combined_text)
    print(f"Combined plain text successfully saved: {combined_text_path}")

    
    merger = PdfMerger()
    for pdf_path in combined_pdf_paths:
        merger.append(pdf_path)
    combined_pdf_path = os.path.join(output_folder, 'combined.pdf')
    merger.write(combined_pdf_path)
    merger.close()
    print(f"Combined PDF successfully saved: {combined_pdf_path}")

    # Save JSON to file
    json_file_path = os.path.join(output_folder, 'articles.json')
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(article_data, json_file, indent=4)
    print(f"Successfully saved JSON: {json_file_path}")

    driver.quit()
if __name__ == "__main__":
    urls = [
        "https://docs.userpilot.com/category/4-getting-started-with-userpilot",
        "https://docs.userpilot.com/category/5-examples-of-use-cases",
        "https://docs.userpilot.com/category/7-installing-userpilot",
        "https://docs.userpilot.com/category/222-account-and-team",
        "https://docs.userpilot.com/category/245-users-companies",
        "https://docs.userpilot.com/category/13-developer",
        "https://docs.userpilot.com/category/284-dashboards",
        "https://docs.userpilot.com/category/10-building-experiences",
        "https://docs.userpilot.com/category/29-trigger-an-experience-conditionally",
        "https://docs.userpilot.com/category/268-surveys",
        "https://docs.userpilot.com/category/175-native-tooltips",
        "https://docs.userpilot.com/category/12-checklists",
        "https://docs.userpilot.com/category/277-analysis",
        "https://docs.userpilot.com/category/184-resource-center",
        "https://docs.userpilot.com/category/69-net-promoter-score-nps",
        "https://docs.userpilot.com/category/156-integrations",
        "https://docs.userpilot.com/category/205-features",
        "https://docs.userpilot.com/category/192-experimentation",
        "https://docs.userpilot.com/category/261-pages",
        "https://docs.userpilot.com/category/77-faq",
        "https://docs.userpilot.com/category/275-troubleshooting",
        "https://docs.userpilot.com/category/10-building-experiences/2?sort=custom",
    ]
    output_folder = 'output'
    main(urls, output_folder)
