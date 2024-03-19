from dynaconf import Dynaconf

from business_flow import *

if __name__ == '__main__':
    # 读配置
    settings = Dynaconf(
        settings_files=["settings.dev.toml"],
        # settings_files=["settings.prod.toml"],
        environments=True,
    )
    ticket = settings.ticket
    user_code = settings.user_code
    password = settings.password
    phone = settings.phone
    # 流程
    init_global(
        ticket=ticket,
        user_code=user_code,
        password=password,
        phone=phone
    )
    set_volcalb()
    set_session_id()
    set_login_ticket()

    # 添加购物车，并且生成订单
    # 购物车列表
    items: list = [
        {
            'linkId': '100004774',  # 早餐6元薯饼
            'quantity': 1,
            'card': False,
            'menuFlag': 'P',
        },
    ]
    update_cart(items)

    # 确定购物车
    confirm_cart()

    # 提交订单
    submit_order()
    # 初始化session，重新登录
    init_session()
    set_login_ticket()

    # 选择支付方式-确认支付
    order_pay()

    # 获取支付参数
    set_jsp_param()

    # 风险评估
    cashier_assess_risk()

    # 输入密码完成支付
    complete_payment()
