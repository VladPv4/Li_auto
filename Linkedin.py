import csv
import parameters
from parsel import Selector
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys  

def validated_field(field):
    if field:
        pass
    else:
        field = ''
    return field

writer = csv.writer(open(parameters.file_name, 'w'))
writer.writerow(['Name','Job title','URL'])

driver = webdriver.Chrome('/Users/vladpivovarov/Documents/Python/Udemy-2/3.Scrapy/chromedriver')
driver.get('https://www.linkedin.com/login?trk=guest_homepage-basic_nav-header-signin')

username = driver.find_element_by_name('session_key')
username.send_keys(parameters.linkedin_username)
sleep(1)

password = driver.find_element_by_name('session_password') 
password.send_keys(parameters.linkedin_password)   
sleep(1)

sign_in = driver.find_element_by_xpath('//*[@id="app__container"]/main/div/form/div[3]/button') 
sign_in.click()
sleep(5)

driver.get('https://www.google.com')
sleep(3)

search_query = driver.find_element_by_name('q')
search_query.send_keys(parameters.search_query)
sleep(0.5)

search_query.send_keys(Keys.RETURN)
sleep(3)

linkedin_urls = driver.find_elements_by_tag_name('cite')
linkedin_urls = [url.text for url in linkedin_urls]
linkedin_urls = [url.replace(" › ","/in/")  for url in linkedin_urls]
sleep(0.5)

for linkedin_url in linkedin_urls:
    driver.get(linkedin_url)
    sleep(5)

    sel = Selector(text=driver.page_source)
    name = sel.xpath('//h1/text()').extract_first()  
    job_title = sel.xpath('//h2/text()').extract_first() 
    linkedin_link = driver.current_url

    name = validated_field(name)
    job_title = validated_field(job_title)
    linkedin_link = validated_field(linkedin_link)

    print('\n')
    print('Name: ' + name)
    print('Job title: ' + job_title)
    print('URL: ' + linkedin_link)
    print('\n')

    writer.writerow([name.encode('utf-8'),
                    job_title.encode('utf-8'),
                    linkedin_link.encode('utf-8')])

    try:
        driver.find_element_by_xpath('//span[text()="Connect"]').click() 
        sleep(3)
        driver.find_element_by_xpath('//*[@class="artdeco-button artdeco-button--3 ml1"]').click()        
        sleep(3)
        
    except:
        pass




driver.quit()



