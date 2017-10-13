import signal
import traceback
import pandas as pd
from selenium import webdriver
import ast

"""
This script crawls the scope, abstract and purpose for the ieee standards
"""




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


def fetchpage(url):
    error=''
    driver=''
    try:
        driver = webdriver.PhantomJS(
        executable_path=phantomjs_exec_path)
        driver.get(url)
        print 'got page'
        return driver

    except:
        error = traceback.format_exc()
        print error
        if driver!='':
            quitdriver(driver)
        return ''



df=pd.read_csv('IEEE-standards.csv',index_col=0)
df_text=pd.DataFrame(columns=['abstract_new','scope_new','purpose_new'])

ieee_new=open('ieee_new','w')
ieee_err=open('ieee_err','w')


for index, rows in df.iterrows():
    link=rows['PDF Link']
    driver=''
    try:
        driver=fetchpage(link)
    except:
        print 'cannot fecth site!'

    abstract=''
    try:
        abstract=driver.find_element_by_xpath('//div[@ng-bind-html="::vm.details.abstract"]')
        abstract=abstract.text
    except:
        print 'error'

    scope=''
    try:
        scope = driver.find_element_by_xpath('//div[@ng-bind-html="::vm.details.scope"]')
        scope = scope.text
    except:
        print 'error'

    purpose=''
    try:
        purpose = driver.find_element_by_xpath('//div[@ng-bind-html="::vm.details.purpose"]')
        purpose = purpose.text
    except:
        print 'error'

    quitdriver(driver)

    # print link
    # print abstract
    # print scope
    # print purpose

    try:
        ieee_new.write(str({'abstract_new':abstract.encode('utf-8'),'scope_new':scope.encode('utf-8'),'purpose_new':purpose.encode('utf-8')})+'\n')
        ieee_new.flush()

        df_text.append({'abstract_new':abstract.encode('utf-8'),'scope_new':scope.encode('utf-8'),'purpose_new':purpose.encode('utf-8')},ignore_index=True)
    except:
        error = traceback.format_exc()
        ieee_err.write(error)
        ieee_err.flush()

dff=open('ieee_new','r')
for line in dff:
    line=line.strip()
    jsn=ast.literal_eval(line)
    print jsn
    df_text=df_text.append(jsn,ignore_index=True)

print df_text.shape,df.shape
df.reset_index(inplace=True, drop=True)
df_text.reset_index(inplace=True, drop=True)

df_text=pd.concat([df,df_text],axis=1)
df_text.to_csv('IEEE-standards_rev1.csv')
