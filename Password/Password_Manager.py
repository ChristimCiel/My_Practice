# r 讀取
# w 覆寫
# a 在原先資料後再寫東西

#寫個可以讀取檔案且相加數字的程式碼

# with open('123.txt', 'r') as file:
#     total = 0
#     for line in file:
#         total += int(line)
#     print(total)

# import json

# json.dump -> 將資料轉換成為 json 格式儲存
# json.loads -> 將 json 轉換成 python 格式讀取
import json
print("歡迎使用密碼管理器！")


def get_old_dic():
    try:
        with open("123.txt", "r") as f:
            return json.loads(f.read())
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        # 如果文件不存在或是空的,返回空字典
        return {}
    
def check(account_name):
    account_dic = get_old_dic()
    if account_name in account_dic.keys():
        return False
    else:
        return True


def add_account(account_name, account, password):
    if check(account_name):
        get = get_old_dic()
        get[account_name]={
                "account" : account,
                "password" : password
        }
        with open("123.txt", "w") as f:
            f.write(json.dumps(get))
        return True
    else:
        return False


while True:
    mode = input('請問你要使用什麼功能？ （r 查詢、 a 寫入、q 離開）')
    if mode == 'q':
        break
    elif mode == 'a':
        account_name = input('請輸入你的帳號名稱：')
        account = input('請輸入你的帳號：')
        password = input('請輸入你的密碼：')
        if add_account(account_name, account, password):
            print("新增成功")
        else:
            print("已有此帳號")
    elif mode == 'r':
        account_name = input("請輸入要查詢的帳號名稱：")
        if check(account_name):
            print("無此帳號名稱")
        else:
            password_dic = get_old_dic()
            account = password_dic[account_name]["account"]
            password = password_dic[account_name]["password"]
            print(f"帳號 {account}，密碼 {password}")