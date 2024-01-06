import math
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait,Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException,NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from functions.preprocess import getCleanText,getOccurences
from datetime import datetime

def scrapWTTJ(keywords,nb_docs):
    source = "welcometothejungle"
    rootLink = "https://www.welcometothejungle.com"
    service = ChromeService("C:/Users/leogo/Documents/chromedriver-win64/chromedriver-win64/chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    pages = math.ceil(nb_docs/30)
    corpus = list()
    
    try:
        for page in range(1,pages+1):    
            try:
                driver.get(f'{rootLink}/fr/jobs?query={keywords}&aroundQuery=France&page={page}')
                # Initial find of elements
                try:
                    accept_cookies_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button#axeptio_btn_acceptAll'))
                    )

                    accept_cookies_button.click()
                except TimeoutException:
                    pass
                    
                offers = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "ol[data-testid='search-results']"))
                )
                
                # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                # Getting docs left if last page to query
                if nb_docs%30 != 0 and page==pages: 
                    limit = nb_docs%30
                    div_elements_to_click_list = offers.find_elements(By.CSS_SELECTOR, "li")[:limit]
                else :
                    div_elements_to_click_list = offers.find_elements(By.CSS_SELECTOR, "li")

                for index in range(len(div_elements_to_click_list)):
                    try:
                        offers = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "ol[data-testid='search-results']"))
                        )
                        
                        div_elements_to_click_list = offers.find_elements(By.CSS_SELECTOR, "li")
                        div_elements_to_click = div_elements_to_click_list[index]
                        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        # driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
                        # Check if the index is within the valid range
                        div_offer = div_elements_to_click.find_element(By.CSS_SELECTOR,"div")

                        position_elem = div_offer.find_element(By.CSS_SELECTOR,"h4")
                        position = position_elem.text
                        workplace = position_elem.find_elements(By.XPATH, "./following::*//span")[1].text
                        contract_type_icon = div_offer.find_element(By.CSS_SELECTOR,"i[name='contract']")
                        main_contract_div = driver.execute_script("return arguments[0].parentNode;", contract_type_icon)
                        contract_type = main_contract_div.find_element(By.CSS_SELECTOR,"span").text
                        published_date = div_offer.find_element(By.CSS_SELECTOR,"time").get_attribute("datetime").split("T")[0]
                        published_date = datetime.strptime(published_date, '%Y-%m-%d')
                        published_date = published_date.strftime('%d/%m/%Y')
                        # driver.execute_script("arguments[0].scrollIntoView(true);", div_elements_to_click)
                        # company = div_elements_to_click.find_element(By.CSS_SELECTOR, 'p.card-offer__company').text
                        # contract_type = div_elements_to_click.find_elements(By.CSS_SELECTOR, 'ul.important-list > li')[0].text
                        # workplace = div_elements_to_click.find_elements(By.CSS_SELECTOR, 'ul.important-list > li')[1].text
                        # published_date = div_elements_to_click.find_elements(By.CSS_SELECTOR, 'ul.important-list > li')[2].text
                        # Scroll into view
                        # actions = ActionChains(driver)
                        # actions.move_to_element(div_elements_to_click).click().perform()
                        #On remote de deux niveau du bouton "Voir offre" pour pouvoir récupérer les informations appropriées
                        # div_offer = driver.execute_script("return arguments[0].parentNode.parentNode;", div_elements_to_click)
                        # company_elem = div_offer.find_element(By.CSS_SELECTOR, "span[data-cy='companyName']")
                        # company = company_elem.find_element(By.CSS_SELECTOR, "span").text
                        # company_elem = div_offer.find_element(By.CSS_SELECTOR, "span[data-cy='companyName']")
                        # contract_type = div_offer.find_element(By.CSS_SELECTOR, "span[data-cy='contract']").text
                        # workplace = div_offer.find_elements(By.CSS_SELECTOR, "div[data-cy='loc']")[-1].text
                        # published_date = div_offer.find_elements(By.CSS_SELECTOR, "span[data-cy='publishDate']")[-1].text

                        driver.execute_script("arguments[0].click();", div_offer)
                        WebDriverWait(driver, 20).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid='job-section-description']"))
                        )
                        description_elem = driver.find_element(By.CSS_SELECTOR,"div[data-testid='job-section-description']")

                        # driver.execute_script("arguments[0].click();",description_elem.find_elements(By.CSS_SELECTOR,"div")[-1].find_element(By.CSS_SELECTOR,"span"))
                        
                        WebDriverWait(driver, 3)

                        try:
                            profile_elem = driver.find_element(By.CSS_SELECTOR, "div[data-testid='job-section-experience']")
                            profile_html = profile_elem.find_elements(By.CSS_SELECTOR, "div")[-2].get_attribute("innerHTML")
                            profile = BeautifulSoup(profile_html, 'html.parser').get_text()
                        except NoSuchElementException:
                            # If profile element is not found, set it to "NULL"
                            profile = "NULL"
                        # driver.execute_script("arguments[0].click();",profile_elem.find_elements(By.CSS_SELECTOR,"div")[-1].find_element(By.CSS_SELECTOR,"span"))

                        description = description_elem.find_elements(By.CSS_SELECTOR,"div")[-2].get_attribute("innerHTML")
                        # profile = profile_elem.find_elements(By.CSS_SELECTOR,"div")[-2].get_attribute("innerHTML")
                        
                        #parsing tags
                        description = BeautifulSoup(description, 'html.parser').get_text()
                        company_elem = driver.find_element(By.CSS_SELECTOR,"a[href*='/fr/companies/']")
                        company = company_elem.find_element(By.CSS_SELECTOR,"img").get_attribute("alt")
                        long_infos = "".join([description,profile]) if profile != "NULL" else description
                        long_infos = getCleanText([item for item in long_infos.split()])
                        long_infos = getOccurences(long_infos)

                        # print(long_infos)
                        # Wait for the child element to become present in the DOM

                        # # Get the page source after the click
                        # page_source = driver.page_source

                        # Use Beautiful Soup to parse the page source
                        # soup = BeautifulSoup(page_source, 'html.parser')

                        # Example: Retrieve the text of a specific element
                        # desc = soup.select("h4:contains('Descriptif du poste') + p")
                        # descText = ["".join(elem.text) for elem in desc][0]

                        # profile = soup.select("h4:contains('Profil recherché') + p")
                        # profileText = ["".join(elem.text) for elem in profile][0]                  

                        # position = soup.select_one("span[data-cy='jobTitle']").text
                        # position_type = soup.select_one('h4:contains("Secteur d’activité du poste")+span').text
                        # long_infos = soup.select("section")
                        # infos = [item.text.replace("\n"," ").strip() for item in long_infos]
                        # infos = [re.sub(r'\s+', ' ',item) for item in infos]
                        # infos = " ".join([item for item in infos if item != ''])
                        # infos = [item for item in infos if '' not in item]
                        corpus.append({"source":source,"link":rootLink,"position":position,"position_type":"NULL","company":company,"workplace":workplace,"published_date":published_date,"contract_type":contract_type,"description":long_infos})
                    except Exception as e:
                        # Print the exception for debugging purposes
                        print(f"Error: {e}")

                    finally:
                        # Navigate back to the main page
                        driver.execute_script("window.history.go(-1);")

            except Exception as e:
                # Print the exception for debugging purposes
                print(f"Error: {e}")
    finally:
        driver.quit()
