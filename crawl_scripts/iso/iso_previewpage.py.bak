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
        # print 'driver quit successfully!'
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
        driver.set_page_load_timeout(5)  # seconds

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
    driver=''
    try:
        driver = webdriver.PhantomJS(
        executable_path=phantomjs_exec_path)
        # driver=webdriver.Chrome(executable_path='/Users/asitangm/Desktop/current/chromedriver')
        # driver.set_page_load_timeout(20)
        driver.get(url)
        # print 'got page'
        return driver

    except:
        error = traceback.format_exc()
        print error
        if driver!='':
            quitdriver(driver)
        return ''

def getFields(standardurl):

    fields = ['id', 'title', 'introduction', 'scope', 'scope_init']
    fields = map(unicode, fields)
    allinfo = dict(zip(fields, ['','','','','']))


    errors=[]
    driver = fetchpage(standardurl)

    if driver == '':
        errors.append('can\'t get the standard page!')
        return errors, allinfo

    id=''
    title=''
    url=''

    try:
        heading = driver.find_element_by_xpath(
            '//div[@class="heading-condensed"]')

        id=heading.find_element_by_xpath(
            '//*[@itemprop="name"]').text

        allinfo['id']=id

        title=heading.find_element_by_xpath(
            '//*[@itemprop="description"]').text

        allinfo['title']=title

        preview=heading.find_element_by_xpath(
            '//a[@class="btn btn-default"]')

        url = preview.get_attribute("href")

        generalinfo=driver.find_element_by_xpath(
            '//div[@class="col-md-7"]')

        scope_init=generalinfo.find_element_by_xpath(
            '//div[@itemprop="description"]').text

        allinfo['scope_init']=scope_init
        generalinfo = generalinfo.find_element_by_xpath(
            '//ul[@class="refine"]').text

        generalinfo={info.split(':')[0]:info.split(':')[1]  for info in generalinfo.split('\n')}
        allinfo.update(generalinfo)


    except:
        quitdriver(driver)
        errors.append('no preview page found')
        if url=='':
            return errors,allinfo


    quitdriver(driver)

    # fecthing the preview page
    driver = fetchpage(url)

    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="v-label v-widget h2 v-label-h2 v-label-undef-w"]'))
        )
    except:
        quitdriver(driver)
        errors.append('preview page did not load')
        return errors,allinfo


    # ele=driver.find_element_by_xpath('//div[@class="v-slot v-slot-toggle"]')
    # ele.click()

    try:
        if id=='':
            ele = driver.find_element_by_xpath('//div[@class="v-label v-widget h2 v-label-h2 v-label-undef-w"]')
            id = ele.text
            allinfo['id']=id
        if title=='':
            ele = driver.find_element_by_xpath('//div[@class="v-label v-widget std-title v-label-std-title v-has-width"]')
            title = ele.text
            allinfo['title'] = title
    except:
        error = traceback.format_exc()
        print error

    try:
        soup = BeautifulSoup(driver.page_source, "lxml")
    except:
        error = traceback.format_exc()
        errors.append(error)

        quitdriver(driver)
        return errors,allinfo



    try:
        children = soup.find('div', {'class': 'sts-standard'}).findChildren(recursive=False)

        for i in range(3):
            if 'intro' in children[i]['id']:
                introduction = children[i].text
                allinfo['introduction']=introduction

            elif children[i]['id'][-1] == '1':
                scope = children[i].text
                allinfo['scope']=scope


    except:
        error = traceback.format_exc()
        errors.append(error)


    quitdriver(driver)
    return errors,allinfo



# test example
# errors,fileds= getFields('https://www.iso.org/standard/51765.html')
# print fileds
# print errors

df=pd.read_csv('strds.csv',index_col=0)

urls=set(df['url'])
print len(urls)


tempwrite=open('gt_write','w')
errorwrite=open('refetch','w')

for i,url in enumerate(list(urls)):
    try:
        errors,fields=getFields(url)
        print str(i), url
        errorwrite.write(str(i)+' '+ url+' '+str(errors)+'\n')
        errorwrite.flush()
    except:
        print i, url, traceback.format_exc()
        errorwrite.write('FATAL: '+str(i)+' '+ url+' '+traceback.format_exc()+'\n')
        errorwrite.flush()



    tempwrite.write(url+' '+str(fields)+'\n')
    tempwrite.flush()


