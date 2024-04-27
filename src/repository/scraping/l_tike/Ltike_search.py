# from time import sleep

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By


# def search(url: str, artist: str):
#     options = Options()
#     # options.add_argument("--headless")
#     browser = webdriver.Chrome(options=options)

#     browser.get(url)
#     # search_field = browser.find_element(By.ID, "SearchField")
#     # search_field.send_keys(artist)
#     # search_btn = browser.find_elements(By.CLASS_NAME, "SearchButton")[0]
#     # search_btn.click()
#     # artist_tab = browser.find_element(By.CSS_SELECTOR, "a[href='#artist']")
#     # artist_tab.click()
#     # artist_link = browser.find_elements(By.CLASS_NAME, "ResultBlock__link")[0]
#     # artist_link.click()
#     lives = browser.find_elements(By.CLASS_NAME, "artist_Lcode_schedule")

#     for live in lives:
#         live.click()
#         title = browser.find_element(By.CLASS_NAME, "TicketTitle").text
#         apply_range = browser.find_element(
#             By.CLASS_SELECTOR,
#             "p.Text:nth-child(1)",
#         ).text
#         print(title, apply_range, "test")
#     sleep(5)


# # search("https://l-tike.com/", "絢香")
# search("https://l-tike.com/artist/000000000331206/", "絢香")
