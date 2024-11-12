from selenium import webdriver # allow launching browser
from selenium.webdriver.common.by import By # allow search with parameters
from selenium.webdriver.support.ui import WebDriverWait # allow waiting for page to load
from selenium.webdriver.support import expected_conditions as EC # determine whether the web page has loaded
from selenium.common.exceptions import TimeoutException # handling timeout situation
from dotenv import load_dotenv # use .env for privacy 
import os
import pandas as pd #exporting data

load_dotenv()

driver_option = webdriver.FirefoxOptions()
driver_option.add_argument(" — incognito")
geckodriver_path = os.getenv('pathToGeckodriver') # Change this to your own geckodriver path!
def create_webdriver():
    return webdriver.Firefox(executable_path=geckodriver_path, firefox_options=driver_option)

browser = create_webdriver()
browser.get("https://github.com/collections/machine-learning")

# Extract all projects
projects = browser.find_elements_by_xpath("//h1[@class='h3 lh-condensed']")

# Extract information for each project
project_list = {}
for proj in projects:
    proj_name = proj.text # Project name
    proj_url = proj.find_elements_by_xpath("a")[0].get_attribute('href') # Project URL
    project_list[proj_name] = proj_url

# Extracting data
project_df = pd.DataFrame.from_dict(project_list, orient = 'index')

# Manipulate the table
project_df['project_name'] = project_df.index
project_df.columns = ['project_url', 'project_name']
project_df = project_df.reset_index(drop=True)

# Export project dataframe to CSV
project_df.to_csv('project_list.csv')



browser.quit()