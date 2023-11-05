#Câu 1
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd

# Create a function to extract titles from a single page
def extract_titles(soup):
    titles = soup.find_all('span', class_='hlFld-Title')
    content_list = [title.text for title in titles]
    return content_list

# Set the start page number and the maximum number of pages to scrape
start_page = -1
max_pages = 120

# Initialize the dataframe
data = {'STT': [], 'Tên Tạp chí': []}
df = pd.DataFrame(data)

# Initialize ChromeDriver
stt = 1  # Initialize STT

for i in range(start_page, max_pages + 1):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # Go to the current page
    driver.get(f'https://journals.sagepub.com/action/showPublications?startPage={i + 1}&pageSize=10')
    
    # Extract the titles from the current page
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    titles = extract_titles(soup)
    
    # Add the titles to the dataframe with STT
    data_page = {'STT': [f'{stt + idx}' for idx in range(len(titles))], 'Content': titles}
    df_page = pd.DataFrame(data_page)
    df = pd.concat([df, df_page], ignore_index=True)
    
    # Update the STT for the next page
    stt += len(titles)
    
    driver.quit()

# Save the dataframe to an Excel file
df.to_excel('test.xlsx', index=False)




#Câu 2
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd

# Initialize ChromeDriver
# Define the start page and the maximum number of pages to scrape
start_page = -1
max_pages = 121  # Change this to the desired number of pages to scrape
# Initialize an empty list for abbreviations
all_abbreviations = []
link = []
for i in range(start_page, max_pages):
    # Construct the URL for the current page
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    current_url = f'https://journals.sagepub.com/action/showPublications?startPage={i +1 }&pageSize=10'

    # Navigate to the current page
    driver.get(current_url)

    # Find all elements with a href attribute inside .item__image
    elems = driver.find_elements(By.CSS_SELECTOR, ".item__image a[href]")
    links = [elem.get_attribute('href') for elem in elems]

    # Extract abbreviations from links on the current page
    abbreviations = [link.split("/")[-1] for link in links if len(link.split("/")) >= 5]

    # Extend the list of abbreviations with the ones from the current page
    all_abbreviations.extend(abbreviations)
    link.extend(links)

# Close the driver
    driver.quit()

# Create a DataFrame
data = {'Tên Viết Tắt': all_abbreviations, 'links': link}
df = pd.DataFrame(data)
# Save the DataFrame to an Excel file
df.to_excel('abbreviations.xlsx', index=False)






#Câu3, 4

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd

# Danh sách các đường dẫn cần đào
urls = link  # Thay thế bằng danh sách các đường dẫn thực tế

# Khởi tạo danh sách để lưu dữ liệu từ các đường dẫn
data_list = []

# Duyệt qua từng đường dẫn
for url in urls:
    # Khởi tạo ChromeDriver cho mỗi đường dẫn
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # Sử dụng driver để tải trang web
    driver.get(url)

    # Chờ trang web tải hoàn toàn (tùy theo trang web có thể cần thời gian chờ khác nhau)
    # Ví dụ chờ 10 giây:
    driver.implicitly_wait(10)

    # Lấy nội dung trang web
    page_source = driver.page_source

    # Sử dụng BeautifulSoup để phân tích trang web
    soup = BeautifulSoup(page_source, 'html.parser')

    # Trích xuất thông tin Impact Factor
    impact_factor_span = soup.find('span', class_='impact-factor__text')
    impact_factor = impact_factor_span.strong.get_text() if impact_factor_span else None

    # Trích xuất ISSN và eISSN
    issn_list = soup.find_all('span', string=lambda text: text and 'ISSN' in text)
    eissn_list = soup.find_all('span', string=lambda text: text and 'Online ISSN' in text)

    # Kiểm tra xem ISSN và eISSN có tồn tại không
    issn = eissn = None
    if issn_list:
        issn_text = issn_list[0].text
        issn_value = issn_text.split(':')[-1].strip()
        issn = issn_value if issn_value else None
    if eissn_list:
        eissn_text = eissn_list[0].text
        eissn_value = eissn_text.split(':')[-1].strip()
        eissn = eissn_value if eissn_value else None

    # Trích xuất tiêu đề (title)
    title_h2 = soup.findAll('h2', class_='footer__title')
    title = title_h2[-1].get_text() if title_h2 else None

    # Tạo dictionary cho dòng hiện tại
    current_data = {'Tên Tạp Chí': title, 'ISSN': issn, 'eISSN': eissn, 'Impact Factor': impact_factor}

    # Thêm dữ liệu hiện tại vào danh sách
    data_list.append(current_data)

    # Đóng trình duyệt sau khi hoàn thành việc đào dữ liệu từ đường dẫn hiện tại
    driver.quit()

# Tạo DataFrame từ danh sách dữ liệu
result_df = pd.DataFrame(data_list)

# Lưu toàn bộ DataFrame kết quả vào tệp Excel
result_df.to_excel('output.xlsx', index=False)





from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd

# Create a function to extract titles from a single page
def extract_titles(soup):
    titles = soup.find_all('span', class_='hlFld-Title')
    content_list = [title.text for title in titles]
    return content_list

# Set the start page number and the maximum number of pages to scrape
start_page = -1
max_pages = 120

# Initialize the dataframe
data = {'STT': [], 'Content': []}
df = pd.DataFrame(data)

# Initialize ChromeDriver
stt = 1  # Initialize STT

for i in range(start_page, max_pages + 1):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # Go to the current page
    driver.get(f'https://journals.sagepub.com/action/showPublications?startPage={i + 1}&pageSize=10')
    
    # Extract the titles from the current page
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    titles = extract_titles(soup)
    
    # Add the titles to the dataframe with STT
    data_page = {'STT': [f'{stt + idx}' for idx in range(len(titles))], 'Content': titles}
    df_page = pd.DataFrame(data_page)
    df = pd.concat([df, df_page], ignore_index=True)
    
    # Update the STT for the next page
    stt += len(titles)
    
    driver.quit()

# Save the dataframe to an Excel file
df.to_excel('test.xlsx', index=False)

#Câu 5
import pandas as pd

# Đọc dữ liệu từ 3 bộ dữ liệu vào các DataFrame riêng biệt
df1 = pd.read_csv('output.xlsx')
df2 = pd.read_csv('abbreviations.xlsx')
df3 = pd.read_csv('test.xlsx')

# Kết hợp các DataFrame theo các trường chung (ở đây là 'Tên tạp chí')
merged_df = pd.merge(df3, df1, on='Tên tạp chí', how='inner')
merged_df = pd.merge(merged_df, df2, on='Tên tạp chí', how='inner')

# Sắp xếp lại các cột theo thứ tự mong muốn
merged_df = merged_df[['STT', 'Tên tạp chí', 'issn', 'eissn', 'Tên viết tắt', 'Impact Factor']]

# Lưu bộ dữ liệu kết hợp vào một tệp mới
merged_df.to_csv('Complete.xlsx', index=False)

