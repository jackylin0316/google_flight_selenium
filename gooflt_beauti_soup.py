from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
from bs4 import BeautifulSoup

#destination=['NRT','ITM','ICN','PVG','BJS'] #(宛樺)
#destination=['HKG','AMS','SGN','BKK','DXB'] #(立馨)
destination=['MNL','SIN','KUL','DPS','DEL'] #(士淵)
#destination=['SIN','KUL','DPS','MNL']
#destination=['DEL']
#destination=['LAX','JFK','YYZ','YVR','LHR'] #(啟璿)
#destination=['CPH','AMS','CDG','MAD','FCO'] #(宇皇)
#destination=['ZRH','OSL','MEL','AKL','CPT'] #(寬許)

days = 100


now = datetime.now() + timedelta(days=3) # current date and time
todaystr = now.strftime("%Y%m%d")
w = now.strftime("%a")
m = now.strftime("%b")
d = int(now.strftime("%d"))
everydate = f"{w}, {m} {d}"


# Chrome Driver ---------------------------------------------------
my_options = webdriver.ChromeOptions()
my_options.add_argument("--disable-popup-blocking") #禁用彈出攔截
my_options.add_argument("--disable-notifications")
my_options.add_argument("--incognito") #取消通知
my_options.add_argument("--start-maximized") 

my_executable_path = './chromedriver'

driver = webdriver.Chrome(
                executable_path = my_executable_path,
                options=my_options
                )


html_dict = {}
for dest in destination:
    print(dest+" ------------------------------")
    driver.get('https://www.google.com/travel/flights?hl=en-US')
    time.sleep(3)
    

    # Select Departure Date --------------------------------------------
    driver.find_element(
        By.CSS_SELECTOR,
        "div.oSuIZ.YICvqf.kStSsc.ieVaIb > div"
    ).click()
    time.sleep(0.5)
    
    driver.find_element(
        By.CSS_SELECTOR,
        "div[role='button'] > div[aria-label='%s']"%everydate
    ).click()
    time.sleep(0.5)
    
    driver.find_element(
        By.CSS_SELECTOR,
        "div.akjk5c.FrVb0c > div.WXaAwc > div > button"
    ).click()
    time.sleep(0.5)
    
    # --------------------------------------------------------------
    # Select City and Click Search button
    
    # 點一下destination
    driver.find_elements(
        By.CSS_SELECTOR,
        "div > input"
    )[2].click()
    time.sleep(0.5)
    
    #enter destination
    driver.find_elements(
        By.CSS_SELECTOR,
        "div > input"
    )[3].send_keys(dest)
    time.sleep(0.5)
    
    
    #choose the destination
    txtInput = driver.find_element(
        By.CSS_SELECTOR,
        'div.XOeJFd.rHFvzd > ul >li'
    ).click()
    time.sleep(0.5)
    
    
    #choose where from
    x=driver.find_element(
        By.CSS_SELECTOR,
        "div.V00Bye.ESCxub.KckZb"
    )
    time.sleep(0.5)
    x.click()
    
    driver.find_elements(
        By.CSS_SELECTOR,
        "div.lJj3Hd.PuaAn > div.peGo5b.ozeT5c > div > input"
    )[1].send_keys('TPE')
    time.sleep(0.5)
    
    
    txtInput = driver.find_element(
        By.CSS_SELECTOR,
        'div.XOeJFd.rHFvzd > ul >li'
    ).click()
    time.sleep(0.5)
    
    driver.find_elements(
        By.CSS_SELECTOR,
        "span.snByac"
    )[0].click()
    time.sleep(1)
    
    driver.find_elements(
        By.CSS_SELECTOR,
        "div >ul >li"
    )[1].click()
    time.sleep(0.5)
    
    
    # search
    driver.find_element(
        By.CSS_SELECTOR,
        "span.VfPpkd-kBDsod.E6fbI"
    ).click()
    time.sleep(1)
    
    #-------------------------------------------------------------
    df_ls = [] # df_ls reset
    for day in range(days):
        #------------------------------------------------------------------
        # 擷取搜尋到的資料 (不同日的loop起點)
        print(str(day)+' day-', end='')
        
        # list reset
        company=[]
        ts=[]
        price=[]
        duration=[]
        stops=[]

        # 取得起飛日期
        d=driver.find_elements(
            By.CSS_SELECTOR,
            "input.RKk3r.eoY5cb.j0Ppje"    #"input[aria-label='Departure']"
        )[0].get_attribute('value')
        time.sleep(0.5)

        
        # 捲到最底
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.5)
        
        # 展開選單
        if d == everydate:
            elements = driver.find_elements(
                            By.CSS_SELECTOR,
                            "div[role='button'] > span > svg")
        
            if len(elements)>0:
                webdriver.ActionChains(driver).move_to_element(elements[0]).click(elements[0]).perform()
            time.sleep(1)
        

        # 使用 soup 擷取資料 ----------------------------------------------------
        # 取得HTML原始碼
        html_text = driver.page_source
        soup = BeautifulSoup(html_text, "lxml")
        
        # 1. 航空公司
        companies = soup.select("div.OgQvJf.nKlB3b > div:nth-child(2) > div:nth-child(2) > span:nth-child(1)")
        company = [c.get_text() for c in companies]

        # 2. 起、降時間
        dept_times = soup.select("span.mv1WYe > span:nth-child(1) > span > span > span")
        dept_time = [t.get_text() for t in dept_times]
        
        arrive_times = soup.select("span.mv1WYe > span:nth-child(2) > span > span > span")
        arrive_time = [t.get_text() for t in arrive_times]
        
        # 3. 機票價
        prices = soup.select("div.OgQvJf.nKlB3b > div:nth-child(6) > div > div:nth-child(2) >span")    
        price = [p.get_text() for p in prices]
        
        
        # 4. 轉機次數
        stops1 = soup.select("div.OgQvJf.nKlB3b > div:nth-child(4) > div.EfT7Ae.AdWm1c.tPgKwe > span:nth-child(1)")
        stops = [s.text for s in stops1]
        
        # 5. 飛行時間
        duration1 = soup.select("div.OgQvJf.nKlB3b>div:nth-child(3)>div.gvkrdb.AdWm1c.tPgKwe.ogfYpf")
        duration = [d.text for d in duration1]
        
        #------------------------------------------------------------------
        # 轉成 DataFrame
        df = pd.DataFrame({"date":        d,
                           "company":     company,
                           "dept_time":   dept_time,
                           "arrive_time": arrive_time,
                           "price":       price,
                           "path":        dest,
                           "stops":       stops,
                           "duration":    duration})
        
        df_ls.append(df)


        # 關掉泡泡框 ----------------------------------------------------
        elements = driver.find_elements(By.CSS_SELECTOR, "div.FtH4Gc.BXkgYe svg")
        if len(elements)>0: 
            webdriver.ActionChains(driver).move_to_element(elements[0]).click(elements[0]).perform()
        time.sleep(0.5)
        
        # 換日
        e = driver.find_elements(
                By.CSS_SELECTOR,
                "button.VfPpkd-LgbsSe.VfPpkd-LgbsSe-OWXEXe-Bz112c-M1Soyc.LjDxcd.XhPA0b.qfvgSe.joofcc"
                )[1]
        
        webdriver.ActionChains(driver).move_to_element(e).click(e).perform()
        time.sleep(1)
        
        print('end')
        # days_loop 結束 -------------------------------------------------

    all_df = pd.concat(df_ls)
    all_df.to_csv(datetime.now().strftime("%Y%m%d") + '_' + dest + '.csv', index=False, encoding='utf-8')
    # dest_loop 結束 -----------------------------------------------------

