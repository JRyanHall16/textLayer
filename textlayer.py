# import webdriver to control the browser and import Keys specifically to send
# an enter key to submit any forms that can't be submitted with a click
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# import time to timestamp filenames so they are automatically sorted and
# import getpass to conceal password during entry
import time, getpass
# constants used for site navigation using XPath
# XPath seems to be the most direct and efficient way to navigate a website in
# this manner; however, any change to the website would probably be more likely
# to break functionality
siteUrl        = 'https://www.cengage.com'
signInLinkPath = '/html/body/header/div[1]/div[2]/ul/li[3]/a'
signInUserPath = '//*[@id="idp-discovery-username"]'
signInNextPath = '//*[@id="idp-discovery-submit"]'
signInPassPath = '//*[@id="okta-signin-password"]'
signInButnPath = '//*[@id="okta-signin-submit"]'
# titleOne is the title that links to the ebook that this
# is intended to download. in the future, functionality could be added to offer
# a selection of titles instead of only the one static title.
titleOnePath   = '/html/body/div[2]/div[2]/ng-include/div[1]/main/div[6]/section/ul/li[2]/a/div/div[1]/div[2]/div/button'
titleNinePath  = '/html/body/div[2]/div[2]/ng-include/div[1]/main/div[6]/section/ul/li[10]/a/div/div[1]/div[2]/div/button'
# this XPath is utilized to standardize the starting page for the script. This
# links to the first item in the navigation sidebar (presumably the first page)
firstPagePath  = '/html/body/div/span/ui-view/div/nav/reader-toc/div[2]/ul/li[1]/reader-toc-item/div/div'
# this is the iframe that links to the raw page, which is what we will access
# to have access to the page for screenshotting
iFramePath     = '//*[@id="iframe-page"]'
# this variable was originally used to access the next-page button, but didn't
# seem to work nearly as well as using the 'execute_script()' function
# nextPagePath   = '//*[@id="next-page"]'
# script used in 'execute_script()' call to click through to the next page
nextPageScript = 'document.getElementById("next-page").click()'
pageTitlePath  = '/html/body/div/span/ui-view/div/nav/go-to-page/div/form/input'
# path to the div that contains the content of the page, that is used for the
# screenshot and is the inspiration for the title of this project
textLayerPath  = 'html/body/div/div/div/div[2]'
# user-defined variables
siteUser  = None
sitePass  = None
pageCount = None
pageStart = None
userTitle = None
# used to login to site (intended specifically for cengage currently but could
# one day be extended to be used in other situations
def siteLogin(webdriver, username, password):
    signInLink = webdriver.find_element_by_xpath(signInLinkPath)
    signInLink.click()
    signInUser = webdriver.find_element_by_xpath(signInUserPath)
    signInUser.send_keys(username)
    signInNext = webdriver.find_element_by_xpath(signInNextPath)
    signInNext.click()
    signInPass = webdriver.find_element_by_xpath(signInPassPath)
    signInPass.send_keys(password)
    signInButn = webdriver.find_element_by_xpath(signInButnPath)
    signInButn.click()
# used to open and screenshot each page using the current time and the page
# title
def getPages(count):
    page = 0
    while page < count:
        iFrame = driver.find_element_by_xpath(iFramePath)
        pageUrl = iFrame.get_attribute('src')
        pageTitle = driver.find_element_by_xpath(pageTitlePath).get_attribute('value')
        pageName = str(time.time()).split('.')[0]+pageTitle+'.png'
        driver.switch_to.window(driver.window_handles[0])
        driver.get(pageUrl)
        textLayer = driver.find_element_by_xpath(textLayerPath)
        # if a screenshot is taken without each of the edges being visible,
        # the pages are transparent for some reason, so we must expand the
        # dimensions of the window to be outside of the height and width of
        # textLayer element itself
        screenWidth = str(int(textLayer.get_attribute('scrollWidth'))+100)
        screenHeight = str(int(textLayer.get_attribute('scrollHeight'))+100)
        driver.set_window_size(screenWidth, screenHeight)
        textLayer.screenshot(pageName)
        driver.switch_to.window(driver.window_handles[1])
        # this line was used to maximize the window because I thought that the
        # next-page element wasn't displaying because of the size of the window
        # but I decided on a different solution
#       driver.maximize_window()
        # this set of lines were replaced with the single 'execute_script()'
        # line below it because they weren't working for some reason and I
        # don't see any difference in performance or function
#       nextPage = driver.find_element_by_xpath(nextPagePath)
#       nextPage.click()
        driver.execute_script(nextPageScript)
        # obviously just incrementing the loop condition
        page += 1
        
def getLoginInfo():
    global siteUser, sitePass
    siteUser = input("Enter your username: ")
    # using getpass to conceal the password entry
    sitePass = getpass.getpass("Enter your password: ")
# not sure what this is for haha need to revisit this
# OH. I remember what this is for but I'm going to leave the line above:
# the purpose of this section was to extend the title selection once logged in
# however I haven't put any effort into that so far because it's not necessary
def getTitle():
    global userTitle
    userTitle = input("Enter the title number: ")
# ensures that input isn't empty, then sets it to pageStart as a string
def getPageCount():
    global pageCount, pageStart
    pageCount = int(input("Enter how many pages you would like to pull: "))
    pageStart = input("which page would you like to start on? ")
    if pageStart is not (None or ''):
        pageStart = str(pageStart)
# this section is the actual program flow starting with
getLoginInfo()
driver = webdriver.Firefox()
# using a higher implicit wait time allows my slow internet to fully load pages
driver.implicitly_wait(30)
driver.get(siteUrl)
siteLogin(driver, siteUser, sitePass)
# getTitle()
# titleOnePath for Microsoft Visual Basic 2015 RELOADED
# titleNinePath for Expert Delphi
selectedTitle = driver.find_element_by_xpath(titleNinePath)
selectedTitle.click()
# once the title is clicked and starts to load, the browser doesn't auto-
# matically change focus to the new tab so we do it ourselves
driver.switch_to.window(driver.window_handles[1])
# then we check to see if we are on the (presumably 'Cover' page and if not
# click the first element in the nav (this needs to be re-evaluated)
if driver.find_element_by_xpath(pageTitlePath).get_attribute('value') != 'Cover':
    firstPage = driver.find_element_by_xpath(firstPagePath)
    firstPage.click()
# this particular loop allows you to grab as many pages as you would like and
# continues to give you the option to get more as long as you enter explicitly
# 'y' in response to the input prompt. This is particularly useful if you only
# wanted to select specific selections of pages (or if, say, you were missing
# a few pages throughout the text book)
while True:
    getPageCount()
    # this statement checks the contents of the pageStart variable and if it is
    # not empty, uses it to load the starting page to work from
    if pageStart is not (None or ''):
        pageTitle = driver.find_element_by_xpath(pageTitlePath)
        pageTitle.clear()
        pageTitle.send_keys(pageStart + Keys.ENTER)
    getPages(pageCount)
    if input('Would you like to continue? [y/n] ') != 'y':
        break
time.sleep(120)
driver.quit()
