import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By

# -------------------------------------- إعدادات المشروع - Project Settings ----------------------------------------

# URL الخاص بالموقع الهدف
# The target website URL
payscale_url = "https://www.payscale.com/college-salary-report/majors-that-pay-you-back/bachelors"

# اسم الملف لتخزين البيانات
# Name of the file to store the extracted data
output_file = "highest_paying_jobs_bachelors.csv"

# -------------------------------------- تهيئة متصفح كروم - Chrome Configuration -----------------------------------

# إعداد خيارات متصفح Chrome
# Configure Chrome browser options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

# تهيئة المتصفح
# Initialize the browser
driver = webdriver.Chrome(options=chrome_options)
driver.get(payscale_url)

# -------------------------------------- استخراج عناوين الأعمدة - Extract Column Headers --------------------------

# تأخير للسماح بتحميل الصفحة
# Delay to allow the page to load
time.sleep(20)

# العثور على رؤوس الجدول
# Locate table headers
table_headers = driver.find_elements(By.CSS_SELECTOR, "table thead tr th")
column_names = [header.text for header in table_headers]

# كتابة عناوين الأعمدة في ملف CSV
# Write column headers to the CSV file
with open(output_file, mode="a", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    if csv_file.tell() == 0:
        writer.writerow(column_names)

# -------------------------------------- تحديد عدد الصفحات - Determine Page Count ---------------------------------

# الصفحة الحالية
# Current page
current_page = 0

# البيانات المستخرجة
# Extracted data
table_data = []

# العثور على عدد الصفحات الكلي
# Find the total number of pages
total_pages = int(driver.find_element(By.XPATH, "//*[@id='__next']/div/div[1]/article/div[3]/a[6]").text)

while current_page < total_pages:
    print(f"Total Pages: {total_pages}, Current Page: {current_page}")

    # -------------------------------- استخراج بيانات الجدول - Extract Table Data ----------------------------------

    # العثور على الصفوف في الجدول
    # Locate rows in the table
    table_rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")

    for row in table_rows:
        # استخراج القيم من الأعمدة
        # Extract values from columns
        columns = row.find_elements(By.CSS_SELECTOR, "td .data-table__value")
        if len(columns) == 6:
            # إنشاء قاموس للبيانات
            # Create a dictionary for the data
            row_data = {
                "rank": columns[0].text,
                "major": columns[1].text,
                "degree_type": columns[2].text,
                "early_career_pay": columns[3].text,
                "mid_career_pay": columns[4].text,
                "high_meaning": columns[5].text
            }
            table_data.append(row_data)
            print(row_data)

    # ----------------------------------- الانتقال إلى الصفحة التالية - Navigate to Next Page -----------------------

    # العثور على رابط الصفحة التالية
    # Locate the next page link
    time.sleep(7)
    next_button = driver.find_element(By.CSS_SELECTOR, "a.pagination__btn.pagination__next-btn")
    next_page_url = next_button.get_attribute("href")
    driver.get(next_page_url)
    print(f"Navigated to: {next_page_url}")

    # تم تعيين وقت الانتظار طويلًا (30 ثانية) لأن الإنترنت كان بطيئًا أثناء تنفيذ الكود
    # A long wait time (30 seconds) is set because the internet was slow during code execution
    time.sleep(30)

    # تحديث الصفحة الحالية
    # Update the current page
    current_page = int(
        driver.find_element(By.CSS_SELECTOR, "a.pagination__btn--active div.pagination__btn--inner").text)
    print(f"Current Page Updated To: {current_page}")
    time.sleep(5)

# -------------------------------------- حفظ البيانات في ملف - Save Data to File ----------------------------------

print("Saving data to file...")
with open(output_file, mode="a", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    for entry in table_data:
        writer.writerow(entry.values())

print("Data extraction complete!")
