from flask import Flask, request,render_template
import time
import undetected_chromedriver
# import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyvirtualdisplay import display
import os



app = Flask(__name__)
current_dir = os.getcwd()
global driver_new


@app.route("/")
def hello_world():
    return render_template("AnkitChatGPT.html")


@app.route("/login", methods=["GET","POST"])
def chatgpt_login():
    # driver = webdriver.Chrome("chromedriver.exe")
    chrome_ver = int(input("Enter the chrome browser version:"))
    driver = undetected_chromedriver.Chrome(version_main=chrome_ver)
    driver.get("https://chat.openai.com/chat")
    
    # Wait for the text to appear
    try:
        WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'How can I help you today?')]")))
        global driver_new
        driver_new = driver
        print('Login success')
    except Exception as e:
        print(e)
        print('Login failed')
    return "Login Success!!"





@app.route("/requestChatGPT")
def chatgpt():
    try:
        #display.Display(visible=0, size=(500,500)).start()
        #query = st.text_input("Enter your query","")
        #if query.lower() == "exit":
        #query = str(input("Enter your query:"))
        print(os.getppid())
        #driver = os.environ.get('DRIVER')
        driver = driver_new
        #driver = app.config['LOGGER']
        query = request.args.get('q')
        print(query)
        textarea = driver.find_element(By.TAG_NAME, "textarea")
        print("debug 1")
        textarea.send_keys(query)
        print("debug 2")
        ActionChains(driver).key_down(Keys.ENTER).key_up(Keys.ENTER).perform()
        #st.text("generating response...")
        print("debug 3")
        time.sleep(5)
        resp = ""
        while True:
            response = driver.find_elements(By.CLASS_NAME, "markdown")
            print("------Response------")
            print("\n"+response[-1].text)
            print("\n\n")
            if resp == response[-1].text:
                break
            else:
                resp = response[-1].text
                time.sleep(3)
            
        #st.write(response[-1].text)
        return resp
    except Exception as e:
        print(e)
        return "Somthing went wrong!!"


'''if __name__ == "__main__":'''
app.run(debug=True,)
