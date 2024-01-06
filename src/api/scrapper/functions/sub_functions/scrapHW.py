import math
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait,Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from functions.preprocess import getCleanText,getOccurences

def scrapHW(keywords,nb_docs):
    pages = math.ceil(nb_docs/30)
    source = "hellowork"
    rootLink = "https://www.hellowork.com"
    service = ChromeService("C:/Users/leogo/Documents/chromedriver-win64/chromedriver-win64/chromedriver.exe")
    driver = webdriver.Chrome(service=service) 
    corpus = list()
    
    try:
        for page in range(pages):    
            try:
                print(page)
                driver.get(f'{rootLink}/fr-fr/emploi/recherche.html?k={keywords}&k_autocomplete=&l=France&l_autocomplete=&p={page+1}')
                # Initial find of elements
                try:
                    accept_cookies_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button#hw-cc-notice-accept-btn'))
                    )

                    accept_cookies_button.click()

                    combobox = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "select[name='country']"))
                    )

                    select = Select(combobox)
                    # Select a specific item by visible text
                    select.select_by_value("FR")

                    form = driver.find_element(By.CSS_SELECTOR,"form[data-action*='service-adaptation']")
                    next_button = form.find_element(By.CSS_SELECTOR,"button")
                    next_button.click()
                except TimeoutException:
                    pass

                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-cy='seeOffer']"))
                )
                # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                # Getting docs left if last page to query
                if nb_docs%20 != 0 and page==pages-1: 
                    limit = nb_docs%20
                    div_elements_to_click_list = driver.find_elements(By.CSS_SELECTOR, "button[data-cy='seeOffer']")[:limit]
                else :
                    div_elements_to_click_list = driver.find_elements(By.CSS_SELECTOR, "button[data-cy='seeOffer']")
                    
                for index in range(len(div_elements_to_click_list)):
                    try:
                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-cy='seeOffer']"))
                        )

                        # Re-find elements after navigating back
                        div_elements_to_click_list = driver.find_elements(By.CSS_SELECTOR, "button[data-cy='seeOffer']")
                        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        # driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-cy='seeOffer']"))
                        )
                        # Check if the index is within the valid range

                        div_elements_to_click = div_elements_to_click_list[index]
                        # driver.execute_script("arguments[0].scrollIntoView(true);", div_elements_to_click)
                        # company = div_elements_to_click.find_element(By.CSS_SELECTOR, 'p.card-offer__company').text
                        # contract_type = div_elements_to_click.find_elements(By.CSS_SELECTOR, 'ul.important-list > li')[0].text
                        # workplace = div_elements_to_click.find_elements(By.CSS_SELECTOR, 'ul.important-list > li')[1].text
                        # published_date = div_elements_to_click.find_elements(By.CSS_SELECTOR, 'ul.important-list > li')[2].text
                        # Scroll into view

                        # actions = ActionChains(driver)
                        # actions.move_to_element(div_elements_to_click).click().perform()
                        #On remote de deux niveau du bouton "Voir offre" pour pouvoir récupérer les informations appropriées
                        div_offer = driver.execute_script("return arguments[0].parentNode.parentNode;", div_elements_to_click)
                        company_elem = div_offer.find_element(By.CSS_SELECTOR, "span[data-cy='companyName']")
                        company = company_elem.find_element(By.CSS_SELECTOR, "span").text
                        company_elem = div_offer.find_element(By.CSS_SELECTOR, "span[data-cy='companyName']")
                        contract_type = div_offer.find_element(By.CSS_SELECTOR, "span[data-cy='contract']").text
                        workplace = div_offer.find_elements(By.CSS_SELECTOR, "div[data-cy='loc']")[-1].text
                        published_date = div_offer.find_elements(By.CSS_SELECTOR, "span[data-cy='publishDate']")[-1].text

                        driver.execute_script("arguments[0].click();", div_elements_to_click)

                        # Wait for the child element to become present in the DOM
                        WebDriverWait(driver, 20).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "span[data-cy='jobTitle']"))
                        )
                        # Get the page source after the click
                        page_source = driver.page_source

                        # Use Beautiful Soup to parse the page source
                        soup = BeautifulSoup(page_source, 'html.parser')

                        # Example: Retrieve the text of a specific element
                        # desc = soup.select("h4:contains('Descriptif du poste') + p")
                        # descText = ["".join(elem.text) for elem in desc][0]

                        # profile = soup.select("h4:contains('Profil recherché') + p")
                        # profileText = ["".join(elem.text) for elem in profile][0]                  

                        position = soup.select_one("span[data-cy='jobTitle']").text
                        # position_type = soup.select_one('h4:contains("Secteur d’activité du poste")+span').text
                        long_infos = soup.select("section")
                        long_infos = getCleanText([item.text for item in long_infos])
                        long_infos = getOccurences(long_infos)
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