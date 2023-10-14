
import re, requests, urllib.parse, json, time
from datetime import date
import pandas as pd
from csv import reader
from multiprocessing.pool import ThreadPool 

zenrows_api = '*** PASTE YOUR ZENROWS API TOKEN HERE ***'
concurrency = 5

sitemap_txt_dir = './sitemap_txt/'
sitemap_xml_dir = './sitemap_xml/'
result_csv_dir = './output_csv/'
header_csv = ['Brand', 'Name', 'English name', 'Model']

today = date.today()
today = today.strftime("%d-%m-%Y")

def cleansitemap_txt():
    open(sitemap_txt_dir + 'sitemap_summary.txt','w')

def writesitemap_txt(list):
    with open(sitemap_txt_dir + 'sitemap_summary.txt', "a") as file:
        i = 1
        for line in list:
            file.write(str(line) + '\n')
            print(f'({i}/{len(list)}) url {str(line)} added to sitemap_txt file')
            i += 1

def downloadsitemap(filename):
    try:
        url = 'https://kream.co.kr/www/sitemap/products/' + str(filename)
        response = requests.get(f"https://api.zenrows.com/v1/?apikey={zenrows_api}&url={url}&block_resources=image%2Cmedia%2Cfont")
        if response.status_code == 404:
            return False
        result = response.text
        with open(sitemap_xml_dir + filename + '.xml', "w") as f:
            f.write(result)
        print(f'Download sitemap #{filename} success!')
        return True
    except:
        print(f'Error sitemap #{filename} download...')
        return False

def crawlsitemap(filename):
    try:
        urls = []
        regex = r'<loc>(.+)</loc>'
        with open(sitemap_xml_dir + filename + '.xml', "r") as file:
            for line in file:
                url = re.findall(regex, line)
                if len(url) > 0:
                    urls.append(url[0])
        
        writesitemap_txt(urls)
        print(f'Crawl sitemap #{filename} success!')
    except:
        print(f'Error sitemap #{filename} craw...!')

def scrapepage(url):
    global today

    url_raw = url
    url = urllib.parse.quote(url)
    result = {}

    while True:
        response = requests.get(f"https://api.zenrows.com/v1/?apikey={zenrows_api}&url={url}&css_extractor=%257B%2522brand%2522%253A%2522a.brand%2522%252C%2522name%2522%253A%2522p.sub_title%2522%252C%2522eng_name%2522%253A%2522div.main_title_box%2520p.title%2522%252C%2522model%2522%253A%2522div.model_num%2520dd.product_info%2522%257D&block_resources=image%2Cmedia%2Cfont")
        result = response.text
        if response.status_code == 404:
            result_list = [[url_raw, 'Page not found']]
            writeresult_csv(result_csv_dir + 'not-found-' + '-' + today + '.csv', result_list)
            print('Page not found: ' + str(url))
            break
        result = json.loads(result)
        if ('brand' in result.keys()) and ('name' in result.keys()) and ('eng_name' in result.keys()) and ('model' in result.keys()):
            if (result['brand'] != '') and (result['name'] != '') and (result['eng_name'] != '') and (result['model'] != ''):
                break
    
    result['sumtitle'] = str(result['brand']) + ' ' + str(result['name']) + ' ' + str(result['eng_name']) + ' ' + str(result['model'])
    result['url'] = url_raw
    result_list = []
    result_list.append(result)
    writeresult_csv(result_csv_dir + 'products.csv', result_list)
    writeresult_csv(result_csv_dir + 'newproducts-' + '-' + today + '.csv', result_list)
    print('New product collected: ' + str(url_raw))

def writeresult_csv(filename, data):
    try:
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False, header=False, mode='a')
        return True
    except:
        return False
    
def addnewproducts_csv(concurrency):
    exists_products = []
    open(result_csv_dir + 'products.csv','a+')
    with open(result_csv_dir + 'products.csv', 'r', encoding="utf8") as read_obj:
        csv_reader = reader(read_obj)
        for row in csv_reader:
            exists_products.append(row[-1])
    
    file = open(sitemap_txt_dir + 'sitemap_summary.txt', 'r')
    lines = file.readlines()
    urls = []
    for line in lines:
        url = line.replace('\n', '')
        if not url in exists_products:
            urls.append(url)  
    pool = ThreadPool(concurrency) 
    pool.map(scrapepage, urls) 
    pool.close() 
    pool.join()

def main():

    start_time = time.time()

    cleansitemap_txt()
    i = 1
    while True:
        if downloadsitemap(str(i)):
            crawlsitemap(str(i))
            i += 1
        else:
            break
        
    addnewproducts_csv(concurrency)    
    
    print('Completed, total time is: '+str(time.time() - start_time))    

if __name__ == "__main__":
    main()