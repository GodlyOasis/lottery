import random
import pymysql
from datetime import datetime
import hashlib


# 定义前区和后区的范围
front_range = list(range(1, 36))
back_range = list(range(1, 13))

# 连接MySQL数据库
db = pymysql.connect(host="localhost", user="root", password="258315", database="happyapp")
# 创建游标对象
cursor = db.cursor()

# 导入时间
now = datetime.now()
year = now.strftime("%Y")
month = now.strftime("%m")
day = now.strftime("%d")


# 定义一个函数，用于生成一注随机号码
def generate_random_number():
    # 从前区随机选5个不重复的号码，并排序
    front_number = sorted(random.sample(front_range, 5))
    # 从后区随机选2个不重复的号码，并排序
    back_number = sorted(random.sample(back_range, 2))
    # 返回一个列表，包含前区和后区的号码
    return front_number + back_number


# 定义一个函数，用于检查用户输入的号码是否合法
def check_user_number(user_number):
    # 如果用户输入的不是7个数字，返回False
    if len(user_number) != 7:
        return False
    # 将用户输入的数字分为前区和后区
    user_front = user_number[:5]
    user_back = user_number[5:]
    # 检查前区是否有重复的数字，或者是否超出范围，如果有，返回False
    if len(set(user_front)) != 5 or any(n not in front_range for n in user_front):
        return False
    # 检查后区是否有重复的数字，或者是否超出范围，如果有，返回False
    if len(set(user_back)) != 2 or any(n not in back_range for n in user_back):
        return False
    # 如果都没有问题，返回True
    return True


# 定义一个函数，用于比较用户号码和开奖号码，并返回中奖等级
def compare_number(user_number, lottery_number):
    # 将用户号码和开奖号码分为前区和后区
    user_front = user_number[:5]
    user_back = user_number[5:]
    lottery_front = lottery_number[:5]
    lottery_back = lottery_number[5:]
    # 计算前区和后区的匹配个数
    front_match = len(set(user_front) & set(lottery_front))
    back_match = len(set(user_back) & set(lottery_back))
    # 定义一个字典，存储中奖等级和对应的匹配个数
    prize_dict = {"1": (5, 2), "2": (5, 1), "3": (5, 0), "4": (4, 2),
                  "5": (4, 1),
                  "6": (3, 2), "7": (4, 0), "8": ((3, 1), (2, 2)), "9":
                      ((3, 0), (1, 2), (2, 1), (0, 2))}
    # 遍历字典，找到匹配个数对应的中奖等级，并返回一个字符串
    for prize_level, match in prize_dict.items():
        if (front_match, back_match) == match or (front_match, back_match) in match:
            return prize_level
    # 如果没有找到匹配的中奖等级，返回未中奖
    return "未中奖"


def show_input_page():
    # 打印欢迎信息和选择模式提示
    print('-' * 30)
    print("欢迎来到模拟大乐透！")
    # 定义一个空列表，用于存储用户号码
    user_numbers = []
    # 定义一个变量，用于控制循环
    continue_bet = True
    # 循环执行以下操作，直到用户选择不继续下注
    while continue_bet:
        print("请选择投注模式：")
        print("1. 自选")
        print("2. 机选")
        print('-' * 30)
        # 使用try-except语句来处理用户输入的异常
        try:
            # 获取用户输入的模式，如果不是1或者2，抛出异常
            mode = input("请输入1或者2：")
            if mode not in ["1", "2"]:
                raise ValueError("输入错误，请重新输入！")
            # 如果用户选择自选模式
            if mode == "1":
                # 提示用户输入7个数字，用空格分隔
                user_number = input("请输入7个数字，用空格分隔，前区5个，后区2个：")
                # 将用户输入的字符串转换为整数列表
                user_number = [int(n) for n in user_number.split()]
                # 检查用户输入的号码是否合法，如果不合法，抛出异常
                if not check_user_number(user_number):
                    raise ValueError("号码不合法，请重新输入！")
                # 将用户输入的号码添加到列表中
                user_numbers.append(user_number)
            # 如果用户选择机选模式
            else:
                # 定义一个变量，用于控制循环
                valid_input = False
                # 循环获取用户输入，直到用户输入一个合法的正整数为止
                while not valid_input:
                    # 使用try-except语句来处理用户输入的异常
                    try:
                        # 获取用户输入的下注数量，并转换为整数
                        num = input("请输入下注数量：")
                        num = int(num)
                        # 如果用户输入的整数大于0，将循环变量设为True，结束循环
                        if num > 0:
                            valid_input = True
                        # 否则，提示用户重新输入
                        else:
                            print("请输入一个正整数！")
                    # 如果用户输入的不是一个有效的数字，提示用户重新输入
                    except ValueError:
                        print("请输入一个数字！")
                # 循环生成随机号码，并添加到列表中
                for n in range(num):
                    user_numbers.append(generate_random_number())
            # 打印已投注的号码和总注数
            print('-' * 30)
            print("已投注的号码为：", user_numbers)
            print(f"共计{len(user_numbers)}注，{len(user_numbers) * 2}元")  # 使用f-string来格式化字符串
            print('-' * 30)
            # 提示用户是否继续下注，并获取用户输入的答案
            answer = input("是否继续下注？（y/n）")
            print('-' * 30)
            # 如果用户输入的不是y或者n，抛出异常
            if answer not in ["y", "n"]:
                raise ValueError("输入错误，请重新输入！")
            # 如果用户输入的是n，将循环变量设为False，结束循环
            if answer == "n":
                continue_bet = False
        except Exception as e:
            # 打印异常信息，并继续循环
            print(e)
    # 返回用户号码列表
    return user_numbers


# 定义一个函数，用于生成彩票代码，并存储到数据库中
def generate_ticket_code(user_numbers):
    # 定义一个空字符串，用于存储彩票代码
    ticket_code = ""
    # 定义一个空字符串，用于存储用户号码
    user_number_str = ""
    # 遍历用户号码列表，将每一注用户号码转换为字符串，并用;号分隔
    for user_number in user_numbers:
        user_number_str += ",".join(str(n) for n in user_number) + ";"
    # 使用MD5算法对用户号码进行哈希，得到一个32位的十六进制字符串
    hash_str = hashlib.md5(user_number_str.encode()).hexdigest()
    # 从哈希字符串中随机选取8位作为彩票代码
    ticket_code = "".join(random.sample(hash_str, 8))
    # 构造SQL语句，将彩票代码和用户号码插入到数据库中
    sql = f"INSERT INTO tickets (code, details, count) VALUES ('{ticket_code}', '{user_number_str}', {len(user_numbers)})"
    # 执行SQL语句，并提交到数据库
    cursor.execute(sql)
    db.commit()
    # 返回彩票代码
    return ticket_code


# 定义一个函数，用于显示开奖页面，并比较用户号码和开奖号码
def show_lottery_page():
    # 生成一注开奖号码，并返回给主程序
    lottery_number = generate_random_number()
    return lottery_number


# 定义一个函数，用于显示验证页面，并获取用户输入的彩票代码和开奖号码，并比较中奖等级
def show_verify_page(lottery_number):
    # 提示用户输入彩票代码，并获取用户输入
    ticket_code = input("请输入你的彩票代码：")
    # 使用try-except语句来处理用户输入的异常
    try:
        # 构造SQL语句，从数据库中查询彩票代码是否已经开奖
        sql = f"SELECT * FROM prize WHERE code = '{ticket_code}'"
        # 执行SQL语句，并获取查询结果
        cursor.execute(sql)
        result = cursor.fetchone()
        # 如果查询结果不为空，说明该彩票已经开奖，提示用户并返回输入彩票代码页
        if result:
            print("该彩票已开奖！")
            return show_verify_page(lottery_number)
        # 否则，构造SQL语句，从数据库中查询彩票代码对应的用户号码
        sql = f"SELECT details FROM tickets WHERE code = '{ticket_code}'"
        # 执行SQL语句，并获取查询结果
        cursor.execute(sql)
        result = cursor.fetchone()
        # 如果查询结果为空，说明没有找到对应的彩票代码，抛出异常
        if not result:
            raise ValueError("无效的彩票代码，请重新输入！")
        # 否则，将查询结果转换为整数列表的列表，并遍历每一注用户号码
        user_numbers = [[int(n) for n in num.split(",") if n] for num in result[0].split(";")]
        # 定义一个列表，用于存储各个等级的中奖个数
        prize_count = [0] * 10  # 0代表未中奖，1-9代表一到九等奖
        for user_number in user_numbers:
            # 调用compare_number函数，比较用户号码和开奖号码，并打印出中奖等级
            if len(user_number) > 0:
                prize_level = compare_number(user_number, lottery_number)
                print(f"彩票号码：{user_number},中奖等级：{prize_level}")
                # 更新列表中对应的值
                if prize_level == "未中奖":
                    prize_count[0] += 1
                else:
                    prize_count[int(prize_level[0])] += 1  # 提取数字部分
        # 定义一个列表，存储各个等级的奖金
        prize_money = [0, 10000000, 5000000, 10000, 3000, 300, 200, 100, 15, 5]
        # 计算code旗下的所有彩票的奖金和
        bonus = sum(prize_count[i] * prize_money[i] for i in range(10))
        # 构造SQL语句，将彩票代码、未中奖个数、各个等级的中奖个数和奖金和插入到prize表中
        sql = f"INSERT INTO prize (code, noprize, prize1, prize2, prize3, prize4, prize5, prize6, prize7, prize8, " \
              f"prize9, bonus, cost) VALUES ('{ticket_code}', {prize_count[0]}, {', '.join(str(n) for n in prize_count[1:])}, {bonus}, {(len(user_numbers) * 2) - 2}) "
        # 执行SQL语句，并提交事务
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        # 打印异常信息，并返回None
        print(e)


# 定义一个函数，用于显示起始页面，并获取用户选择的入口
def show_start_page():
    # 打印欢迎信息和选择入口提示
    print('-' * 30)
    print("欢迎来到大乐透！")
    print("请选择功能：")
    print("1. 买彩票")
    print("2. 开奖")
    print("3. 退出系统")
    print('-' * 30)
    # 使用try-except语句来处理用户输入的异常
    try:
        # 获取用户输入的入口，如果不是1或者2或者3，抛出异常
        entry = input("请输入1或者2或者3：")
        if entry not in ["1", "2", "3"]:
            raise ValueError("输入错误，请重新输入1/2/3！")
        # 返回用户输入的入口
        return entry
    except Exception as e:
        # 打印异常信息，并返回None
        print(e)


# 定义一个变量，用于控制循环
continue_play = True
# 循环执行以下操作，直到用户选择退出系统
while continue_play:
    # 调用show_start_page函数，获取用户选择的入口，并根据不同的入口执行不同的操作
    entry = show_start_page()
    # 如果用户选择买彩票
    if entry == "1":
        # 调用show_input_page函数，获取用户号码列表，并打印出来
        user_numbers = show_input_page()
        print("你购买的号码为：", user_numbers)
        # 调用generate_ticket_code函数，生成彩票代码列表，并打印出来
        ticket_codes = generate_ticket_code(user_numbers)
        print("你的彩票代码为：", ticket_codes)
    # 如果用户选择开奖
    elif entry == "2":
        # 调用show_lottery_page函数，生成开奖号码，并打印出来
        lottery_number = show_lottery_page()
        # 调用show_verify_page函数，获取用户输入的彩票代码和开奖号码，并比较中奖等级
        show_verify_page(lottery_number)
        print('-' * 30)
        print("本期{}年{}月{}日的开奖号码：{}".format(year, month, day, lottery_number))
    # 如果用户选择退出系统
    else:
        # 将循环变量设为False，结束循环
        continue_play = False

# 关闭数据库连接
db.close()
# 打印感谢信息
print("感谢使用模拟大乐透！祝你好运！")
