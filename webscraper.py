import requests
from bs4 import BeautifulSoup
import pandas as pd


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.9999.999 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
}
def Function():
    product = input("Enter product name = ")
    num = int(input("Number of Products you want to compare = "))
    product = product.replace(' ', '+') 
    url_snapdeal = "https://www.snapdeal.com/search?keyword="+product+"&sort=rlvncy"
    url_amazon = "https://www.amazon.in/s?k="+product+"&crid=L2JFQOIWU7YY&sprefix="+product+"%2Caps%2C247&ref=nb_sb_noss_2"
    url_flipkart = "https://www.flipkart.com/search?q="+product
    try :
        print("Searching Amazon....")
        r1 = requests.get(url_amazon, headers=headers)
        print("Searching Snapdeal....")
        r2 = requests.get(url_snapdeal,headers=headers)
        
        amazon_content = r1.content
        snapdeal_content = r2.content
    
        soup_amazon = BeautifulSoup(amazon_content,'html.parser')
        soup_snapdeal = BeautifulSoup(snapdeal_content,'html.parser')
    
    # ************ amazon scraping function *************** #
    
        def amazon_print():
            soup = soup_amazon
            product_name = soup.find_all('span' , attrs={'class':'a-text-normal'})
            product_price = soup.find_all('span', attrs={'class':'a-price'})
            anchors = soup.find_all('a',attrs = {'class' : 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
            data_amazon = {}
            name_list = []
            price_list = []
            link_list = []
            c = 1    
            for name,link in zip(product_name,anchors):
                name_list.append(name.text)
                link_list.append(link.get('href'))
                c = c+1
                if c==num+1:
                    c=1
                    break
            for price in product_price:
                if not("a-text-price" in price.get("class")):
                    pr = str(price.find('span').text)
                    price_list.append(pr)
                    c += 1
                    if c==num+1:
                        break
            data_amazon = {
                'Name':name_list,
                'Price':price_list,
                #'link':link_list
            }
            return data_amazon
    
    # ********************** snapdeal scraping function ************************* # 
            
        def snapdeal_print():
            soup2 = soup_snapdeal
            product_name = soup2.find_all('p' , attrs={'class':'product-title'})
            product_price = soup2.find_all('span', attrs={'class':'lfloat product-price'})
            anchors = soup2.find_all('a',attrs = {'class' : 'dp-widget-link noUdLine hashAdded'})
            data_snapdeal = {}
            name_list = []
            price_list = []
            link_list = []
            c = 1 
            for name in product_name:
                name_list.append(name.text)
                c += 1
                if c==num+1:
                    c=1
                    break
            for price in product_price:
                price_list.append(price.text)
                c += 1
                if c==num+1:
                    break
            data_snapdeal = {
                'Name':name_list,
                'Price':price_list,
                # 'link' : link_list
            }
            return data_snapdeal
        
    #*********** Flipkart Scraping ************#
    
        def flipkart_content():
            r3 = requests.get(url_flipkart,headers=headers)
            i=1
            #print("Trying to fetch information from flipkart......")
            while not(r3.status_code==200):
                r3 = requests.get(url,headers=headers)
                i += 1
                if i==20:
                    break
            if r3.status_code == 200:
                soup3 = BeautifulSoup(r3.content,'html.parser')
                product_name = soup3.find_all('div' , attrs={'class':'_4rR01T'})
                product_price = soup3.find_all('div', attrs={'class':'_30jeq3 _1_WHN1'})
                anchors = soup3.find_all('a',attrs = {'class' : '_1fQZEK'})
                data_snapdeal = {}
                name_list = []
                price_list = []
                link_list = []
                c = 1 
                for name in product_name:
                    name_list.append(name.text)
                    c += 1
                    if c==num+1:
                        c=1
                        break
                for price in product_price:
                    price_list.append(price.text)
                    c += 1
                    if c==num+1:
                        break
                for link in anchors:
                    link_list.append(link.get('href'))
                    c += 1
                    if c==num+1:
                        break
                data_snapdeal = {
                    'Name':name_list,
                    'Price':price_list,
                    # 'link' : link_list
                }
                return data_snapdeal
        
            else:
                print("Not able to connect to Flipkart servers!! :(")
        
    # ************** scraped data comparison ******************* #
    
    # ********* creating Data Frame using pandas ************** #
    
     
        df_amazon = pd.DataFrame(amazon_print())
        df_amazon.index = range(1, len(df_amazon) + 1)
    
        df_snapdeal = pd.DataFrame(snapdeal_print())
        df_snapdeal.index = range(1,len(df_snapdeal)+1)
    
    # *************** Display the DataFrame as a bordered table ************* #
    
        print()
        print("******Prices in Amazon*******")
        print(df_amazon)
        print()
        print("******Prices in Snapdeal******")
        print(df_snapdeal)
        print()
        check = int(input("Would you like to extend your search to FLIPKART as well? ('0'-no/'1'-yes) = "))
        if check==1:
            print("Fetching Information from Flipkart...")
            if flipkart_content():
                df_flip = pd.DataFrame(flipkart_content())
                df_flip.index = range(1,len(df_flip)+1)
                print()
                print("********Prices in FlipKart********")
                print(df_flip)

    except requests.exceptions.HTTPError as http_error:
        print("error connecting", http_error)
    except Exception as e:
        print("An error occurred ", e)
 


stop = 1
try :
    while stop == 1:
        Function()
        stop = int(input("Do you want to Continue/Stop? (0/1) = "))
except Exception as e:
    print("Error Occured")