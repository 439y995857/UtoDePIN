import time
from decimal import Decimal, getcontext

# 设置精确度为18位
getcontext().prec = 18

# 初始化参数
reserve_fund = Decimal('1.01')  # 兑付储备金
starting_price = Decimal('1.01')  # 起始价格
tolerance = Decimal('0.01')  # 容差
total_transactions = 100000000000  # 总交易次数，为了演示，这里设置为100次

# 初始化变量
current_price = starting_price
current_reserve_fund = reserve_fund
current_supply = Decimal('1')  # 初始市场流通量已经有1枚Uto代币
user_tokens = Decimal('1')  # 用户手上持有的代币数量，初始为1
tokens_to_sell = Decimal('0.999')  # 每次卖出的代币数量

# 循环购买
for i in range(1, total_transactions + 1):
    # 计算买入前的价格
    price_before = current_reserve_fund / current_supply

    # 计算每次购买的金额（买入价格 + 容差）
    buy_amount = current_price + (current_price * tolerance)
    current_reserve_fund += buy_amount  # 更新储备金

    # 更新市场流通量
    current_supply += Decimal('1')
    user_tokens += Decimal('1')  # 用户每次购买1枚代币

    # 计算买入后的价格
    price_after = current_reserve_fund / current_supply

    # 每满100次交易，卖出代币
    if i % 100 == 0:
        # 检查是否有足够的代币可以卖出
        if user_tokens >= tokens_to_sell:
            # 卖出代币，减少储备金和市场流通量
            sell_amount = tokens_to_sell * price_after
            current_reserve_fund -= sell_amount
            user_tokens -= tokens_to_sell  # 卖出代币
            current_supply -= tokens_to_sell  # 减少市场流通量
        else:
            print(f"第{i+1}次交易：不足够代币卖出，当前持有量：{user_tokens}, 需要卖出：{tokens_to_sell}")
            user_tokens = Decimal('0')  # 如果没有足够的代币卖出，将用户持有量设置为0

    # 计算总共上涨率
    total_rising_rate = (price_after - starting_price) / starting_price * Decimal('100')

    # 打印每次购买的结果
    print(f"第{i+1}次购买：")
    print(f"购买金额: {buy_amount}")
    print(f"买入前价格: {price_before}")
    print(f"买入后价格: {price_after}")
    print(f"总共上涨率: {total_rising_rate}")
    print(f"用户持有量: {user_tokens}")
    print(f"兑付储备金金额: {current_reserve_fund}")
    print("-" * 50)
    
    # 更新当前价格为买入后的价格，准备下一次交易
    current_price = price_after

    # 暂停0.01秒
    time.sleep(0.01)

# 最终结果
total_rising_rate = (current_price - starting_price) / starting_price * Decimal('100')
print(f"最终兑付储备金价值：{current_reserve_fund}")
print(f"最终价格：{current_price}")
print(f"最终总共上涨率：{total_rising_rate}")
print(f"最终用户持有量：{user_tokens}")
print(f"最终累计Uto总价值：{user_tokens * current_price}")