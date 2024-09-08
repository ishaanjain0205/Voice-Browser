#projectFunctions.py

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By  
from sentence_transformers import SentenceTransformer, util


# takes in input, actions[], and classifier
def compute_action(input, actions, text_based_actions, model, classifier):

    # check for search and click first
    classifier_results = classifier(input, text_based_actions)

    # if confidence is greater than threshold, return search or click command
    scores = classifier_results["scores"]
    labels = classifier_results["labels"]
    max_score = max(scores)
    print(labels[0] + " " + str(max_score))
    if max_score > 0.75:
        max_idx = scores.index(max_score)
#        print("Classifier executed")
        print("Best matching intent: " + labels[max_idx])
        return labels[max_idx]
    else:
        # check for all other actions if not search or click 
        # encode both querry and intents
        query = model.encode(input)
        intents = model.encode(actions)

        # calculate smilarities
        similarities = util.cos_sim(query, intents)

        # find most similar command index
        closest_intent = similarities.argmax()
#       print("Model executed")
        print(f"Best matching intent: {actions[closest_intent]}")

        return actions[closest_intent]

    
# redirect commands
def proccess_command(command, recognizedText, driver, model, classifier, click_model):
    if command in ["search", "look", "search up"]:
        search(recognizedText, driver)
    elif command == "scroll down" or command == "down":
        scroll_down(driver)
    elif command == "scroll up" or command == "up":
        scroll_up(driver)
    elif command == "open tab" or command == "open":
        open_tab(driver)
    elif command == "close tab" or command == "close":
        close_tab(driver)
    elif command == "next tab":
        next_tab(driver)
    elif command == "previous tab" or command == "last tab":
        previous_tab(driver)
    elif command == "next" or command == "next page":
        forward(driver)
    elif command == "go back" or command == "last page":
        back(driver)
    elif command == "refresh":
        refresh(driver)
    elif command == "click" or command == "click on":
        click(recognizedText, driver, model, classifier, click_model)


# search execution
def search(recognizedText, driver):
    try:
        # remove non-querry parts from input
        search_query = recognizedText
        search_query = search_query.replace("search up", "").strip()
        search_query = search_query.replace("search", "").strip()
        search_query = search_query.replace("look up", "").strip()
#        print("RECOGINZED SEARCH AND STRIPPED")

        if search_query == "":
            return

        # find search bar, clear, and search
        search_bar = driver.find_element(By.NAME, "q")

        search_bar.clear()
        search_bar.send_keys(search_query)
        search_bar.submit()
    except:
        print("Could not search")

# scroll down execution
def scroll_down(driver):    
    for i in range(100):
        driver.execute_script("window.scrollBy(0, 5);")

# scroll up execution
def scroll_up(driver):
    for i in range(100):
        driver.execute_script("window.scrollBy(0, -5);")

# open tab
def open_tab(driver):
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[-1])
    driver.get("https://www.google.com")

def close_tab(driver):
    current_tab_tag = driver.current_window_handle
    current_tab_index = driver.window_handles.index(current_tab_tag)
    switch_to_tab_index = current_tab_index - 1
    if switch_to_tab_index == -1 and len(driver.window_handles) == 1: 
        print("THERE WAS ONLY ONE TAB OPEN, CHROME CLOSED")
        driver.quit()
    else:
        driver.close()
        driver.switch_to.window(driver.window_handles[switch_to_tab_index])


def next_tab(driver):
    current_tab_tag = driver.current_window_handle
    current_tab_index = driver.window_handles.index(current_tab_tag)

    if current_tab_index < len(driver.window_handles):
        driver.switch_to.window(driver.window_handles[current_tab_index + 1])
        print("SWITCHED TO TAB" + str(current_tab_index + 2))
    else:
        print("ALREADY ON LAST TAB")


def previous_tab(driver):
    current_tab_tag = driver.current_window_handle
    current_tab_index = driver.window_handles.index(current_tab_tag)

    if current_tab_index != 0:
        driver.switch_to.window(driver.window_handles[current_tab_index - 1])
        print("SWITCHED TO TAB " + str(current_tab_index))
    else:
        print("ALREADY ON FIRST TAB")


def forward(driver):
    driver.forward()

def back(driver):
    driver.back()

def refresh(driver):
    driver.refresh()

def click(input, driver, model, classifier, click_model):
    try:
        # find all clickable elements
        search_results = driver.find_elements(By.TAG_NAME, 'a')
        link_texts = []
        links = []

        # find text for each link
        for link in search_results:
            if link.is_displayed() and link.is_enabled() and is_element_in_viewport(driver,link):
                href = link.get_attribute('href')
                text = link.text
                if href and text != "":
                    link_texts.append(text)
                    links.append(link)
        
        click_query = input
        click_query = click_query.replace("click on", "").strip()
        click_query = click_query.replace("click ", "").strip()
        
        # use model to see which links match closest to users search
        query = click_model.encode(input)
        possible_links = click_model.encode(link_texts)

        similarities = util.cos_sim(query, possible_links)
        closest_intent_idx = similarities.argmax()
        
        predicted_link = link_texts[closest_intent_idx]
        
        #for link in link_texts:
        #    print(link)
#       print("Classifier executed")
        print("Best matching link: " + predicted_link)
        
        final_link = driver.find_element(By.LINK_TEXT, predicted_link)
        final_link.click()
    except:
        print("Could not click")


def is_element_in_viewport(driver, element):
    script = """
    var elem = arguments[0];
    var box = elem.getBoundingClientRect();
    return (
        box.top >= 0 &&
        box.left >= 0 &&
        box.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        box.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
    """
    return driver.execute_script(script, element)