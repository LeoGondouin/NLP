import math
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait,Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from functions.preprocess.getCleanText import getCleanText
from functions.preprocess.getOccurences import getOccurences
from functions.preprocess.getOccurences import getOccurences

def scrapApec(keywords,nb_docs):
        pages = math.ceil(nb_docs/20)
        source = "apec"

        remote_url = "http://selenium_chrome:4444/wd/hub"
        driver = webdriver.Remote(command_executor=remote_url, desired_capabilities=webdriver.DesiredCapabilities.CHROME)

        rootLink = "https://www.apec.fr"
        corpus = list()
        try:
            for page in range(pages):    
                try:
                    driver.get(f'{rootLink}/candidat/recherche-emploi.html/emploi?motsCles={keywords}&page={pages}')
                    # Initial find of elements
                    try:
                        deny_cookies_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button#onetrust-reject-all-handler'))
                        )

                        deny_cookies_button.click()
                    except TimeoutException:
                        pass

                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "div.card-offer"))
                    )

                    # Getting docs left if last page to query
                    if nb_docs%20 != 0 and page==pages-1: 
                        limit = nb_docs%20
                        div_elements_to_click_list = driver.find_elements(By.CSS_SELECTOR, 'div.card-offer')[:limit]
                    else :
                        div_elements_to_click_list = driver.find_elements(By.CSS_SELECTOR, 'div.card-offer')
                        
                    for index in range(len(div_elements_to_click_list)):
                        try:
                            WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, "div.card-offer"))
                            )
                            # Re-find elements after navigating back
                            div_elements_to_click_list = driver.find_elements(By.CSS_SELECTOR, 'div.card-offer')

                            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                            WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, "div.card-offer"))
                            )
                            # Check if the index is within the valid range

                            div_elements_to_click = div_elements_to_click_list[index]
                            company = div_elements_to_click.find_element(By.CSS_SELECTOR, 'p.card-offer__company').text
                            contract_type = div_elements_to_click.find_elements(By.CSS_SELECTOR, 'ul.important-list > li')[0].text
                            workplace = div_elements_to_click.find_elements(By.CSS_SELECTOR, 'ul.important-list > li')[1].text
                            published_date = div_elements_to_click.find_elements(By.CSS_SELECTOR, 'ul.important-list > li')[2].text
                            # Scroll into view

                            actions = ActionChains(driver)
                            actions.move_to_element(div_elements_to_click).click().perform()

                            # Wait for the child element to become present in the DOM
                            WebDriverWait(driver, 20).until(
                                EC.presence_of_element_located((By.XPATH, f"//h4[text()='Descriptif du poste']"))
                            )
                            # Get the page source after the click
                            page_source = driver.page_source

                            # Use Beautiful Soup to parse the page source
                            soup = BeautifulSoup(page_source, 'html.parser')

                            # Example: Retrieve the text of a specific element
                            desc = soup.select("h4:contains('Descriptif du poste') + p")
                            descText = ["".join(elem.text) for elem in desc][0]

                            profile = soup.select("h4:contains('Profil recherché') + p")
                            profileText = ["".join(elem.text) for elem in profile][0]                  

                            position = soup.select_one("h4:contains('Métier') + span").text
                            position_type = soup.select_one('h4:contains("Secteur d’activité du poste")+span').text
                            long_infos = " ".join([descText,profileText])
                            long_infos = getOccurences(long_infos)
                            corpus.append({"source":source,"link":rootLink,"position":position,"position_type":position_type,"company":company,"workplace":workplace,"published_date":published_date,"contract_type":contract_type,"description":long_infos})
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
            return corpus