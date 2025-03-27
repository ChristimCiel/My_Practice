import random

letters_upper = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
                 "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                 "U", "V", "W", "X", "Y", "Z"]

letters_lower = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
                 "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                 "u", "v", "w", "x", "y", "z"]

numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

symbols = ["!", "@", "#", "$", "%", "^", "&", "*", "-", "+"]

# 定義一個函數來確保輸入為數字
def get_valid_number_input(prompt):
    while True:
        user_input = input(prompt)
        if user_input.isdigit():
            return int(user_input)
        else:
            print("請輸入數字")

print('歡迎使用密碼產生器～')
upper_num = get_valid_number_input('請問需要幾個大寫英文字母？ ')
lower_num = get_valid_number_input('請問需要幾個小寫英文字母？ ')
number_num = get_valid_number_input('請問需要幾個數字？ ')
symbol_num = get_valid_number_input('請問需要幾個符號？ ')
# 從 letters_upper 挑 big 數量的字母

password = ""
for i in range(0, upper_num):
    password += random.choice(letters_upper)

for i in range(0, lower_num):
    password += random.choice(letters_lower)

for i in range(0, number_num):
    password += random.choice(numbers)

for i in range(0, symbol_num):
    password += random.choice(symbols)

password_list = list(password)
random.shuffle(password_list)
new_str = ''
for jj in password_list:
    new_str += jj
print(new_str)

