import string

def getgoodurls(page_source):
    #Once on a new page, need to find the page's URLs amidst all on the page
    soup = BS(page_source)
    #Find all forward links
    links = soup.find_all('a')
    urls = []
    #Remove JS formatting from the URLs
    for link in links:
        if link.has_attr('href'):
            urls.append(link['href'])
    #Looking at 10 profiles at a time, we take direct profiles as follows        
    goodurls = urls[74:114:4]
    return goodurls

def pagecycle(n):
    #Pattern for interfacing with inc5000 list
    #Can't directly access the arrow for next page or page index
    #Instead, we lock onto the go button then navigate to the number input
    element = browser.find_element_by_class_name('goButton')
    #use an action chain to move from the go button and enter the number 'n'
    actions = ActionChains(browser)
    actions.key_down(Keys.SHIFT)
    actions.send_keys(Keys.TAB)
    actions.key_up(Keys.SHIFT)
    actions.send_keys(Keys.BACKSPACE)
    actions.send_keys(Keys.BACKSPACE)
    actions.send_keys(Keys.BACKSPACE)
    actions.send_keys(str(n))
    actions.send_keys(Keys.RETURN)
    actions.perform()
    #Finally, return to the go button to go to the next page
    element = browser.find_element_by_class_name('goButton')
    element.click()


def urlcleaner(url):
    #quick function for removing formatiing from url
    name = url[23::]
    return name

def extractpage(browser,pageurl):
    #function for taking information from inc profile
    browser.get(pageurl)
    #Use a dictionary to store information from the page
    #Collecting dictionaries will allow us to quickly build a DataFrame
    datadict = {}
    datadict['Company'] = browser.title
    soup = BS(browser.page_source)
    divs = soup.find_all('div')
    data = []
    #Information will be in divs tagged 'dtdd'
    for div in divs:
        if div.has_attr('class'):
            if div['class'] == ['dtdd']:
                data.append(div)
    #Take all individual information snippets
    for point in data:
        string = str(point.find_all('dt'))
        string2 = str(point.find_all('dd'))
        datadict[string[5:-6]] = string2[5:-6]
    return datadict

def numclean(entry):
    #Remove all punctuation from the dollar amounts, keeping decimals
    punct = string.punctuation
    punct = punct.replace('.','')
    c = ''
    for digit in entry:
        if digit not in set(punct):
            c += digit
    return(float(c))


def dollarclean(entry):
    #strings are not mutable, need to turn dollar strings into numbers
    newentry = entry
    digits = ''
    for digit in entry:
        if digit in '0123456789':
            digits += digit
    newentry = digits + ('.' not in entry)*'0' + ('M' in entry)*'00000' \
               + ('B' in entry)*'00000000'
    return(newentry)
    
