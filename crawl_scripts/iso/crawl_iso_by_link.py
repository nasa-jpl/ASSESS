import signal
import traceback
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup



phantomjs_exec_path='/usr/local/bin/phantomjs'

def quitdriver(driver):
    try:
        driver.service.process.send_signal(signal.SIGTERM)
        driver.quit()
        print 'driver quit successfully!'
        return 'done'
    except:
        error = traceback.format_exc()
        print 'error quitting',error
        return 'error: quitting the driver ' + str(error)

def featchtext(url):
    error = ''
    driver=''
    try:
        driver = webdriver.PhantomJS(
            executable_path=phantomjs_exec_path)  # or add to your PATH
        driver.set_page_load_timeout(15)  # seconds

        driver.maximize_window()
        driver.get(url)
        driver.page_source
        elm = driver.find_element_by_xpath('./*')
        text = elm.text
        quitdriver(driver)
        return text,error

    except:
        error = traceback.format_exc()
        if driver!='':
            quitdriver(driver)
        return '',error


def fetchpage(url):
    error=''
    driver=''
    try:
        driver = webdriver.PhantomJS(
        executable_path=phantomjs_exec_path)
        # driver=webdriver.Chrome(executable_path='/Users/asitangm/Desktop/current/chromedriver')
        # driver.set_page_load_timeout(20)
        driver.get(url)
        print 'got page'
        return driver

    except:
        error = traceback.format_exc()
        print error
        if driver!='':
            quitdriver(driver)
        return ''


df=pd.read_csv('iso-gt.csv',index_col=0)
df_gt=pd.DataFrame(columns=['SoW','title','Standards','introduction','scope','id'])
tempwrite=open('tempwrite','w')

for index, rows in df.iterrows():
    standards=rows['Standards']
    standards=standards.strip()
    standards=standards.split('\r')

    sow=rows['SoW']
    for standardurl in standards:
        print standardurl
        driver=fetchpage(standardurl)

        if driver=='':
            continue

        url=''
        try:
            ele = driver.find_element_by_xpath(
            '//div[@class="heading-condensed"]').find_element_by_xpath(
            '//a[@class="btn btn-default"]')
            url=ele.get_attribute("href")
            quitdriver(driver)

        except:
            print 'no preview'
            quitdriver(driver)
            continue

        driver=fetchpage(url)

        try:
            ele = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="v-label v-widget h2 v-label-h2 v-label-undef-w"]'))
            )
        except:
            print standardurl,url,'no good!'
            quitdriver(driver)
            continue


        # ele=driver.find_element_by_xpath('//div[@class="v-slot v-slot-toggle"]')
        # ele.click()
        try:
            ele = driver.find_element_by_xpath('//div[@class="v-label v-widget h2 v-label-h2 v-label-undef-w"]')
            id=ele.text
            ele = driver.find_element_by_xpath('//div[@class="v-label v-widget std-title v-label-std-title v-has-width"]')
            title=ele.text
        except:
            error = traceback.format_exc()
            print error

        try:
            soup = BeautifulSoup(driver.page_source)
        except:
            error = traceback.format_exc()
            print error
            quitdriver(driver)
            continue

        tempwrite.write(id.encode('utf-8'))
        tempwrite.flush()
        tempwrite.write(title.encode('utf-8'))
        tempwrite.flush()

        introduction=''
        scope=''
        try:
            children=soup.find('div', {'class': 'sts-standard'}).findChildren(recursive=False)

            for i in range(3):
                if 'intro' in children[i]['id']:
                    introduction=children[i].text
                    print 'intro found'
                elif children[i]['id'][-1]=='1':
                    scope=children[i].text
                    print 'scope found'

        except:
            error = traceback.format_exc()
            print error
            print 'missing intro or scope!',standardurl,url

        tempwrite.write(introduction.encode('utf-8'))
        tempwrite.flush()
        tempwrite.write(scope.encode('utf-8'))
        tempwrite.flush()
        tempwrite.write(sow)
        tempwrite.flush()
        tempwrite.write(url.encode('utf-8'))
        tempwrite.flush()

        try:
            df_gt=df_gt.append({'title':title.encode('utf-8'),'SoW':sow,'Standards':url.encode('utf-8'),'introduction':introduction.encode('utf-8'),'scope':scope.encode('utf-8'),'id':id.encode('utf-8')},ignore_index=True)

        except:
            error = traceback.format_exc()
            print error




        quitdriver(driver)


df_gt.to_csv('gt_iso_fetched.csv',columns=['SoW','title','Standards','introduction','scope','id'])
