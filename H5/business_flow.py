import json
import urllib
import requests

from loguru import logger
from bs4 import BeautifulSoup
from KFCSpider.H5.model.GlobalParams import GlobalParams
from KFCSpider.H5.utils import uuid4

global_params: GlobalParams


def init_global(
        ticket,
        user_code,
        password,
        phone
):
    global global_params
    global_params = GlobalParams(
        ticket=ticket,
        user_code=user_code,
        password=password,
        phone=phone
    )


def set_volcalb(echo=False):
    """
    设置volcalb volcalb-cors route-cell

    请求首页，从cookies中获取这3个值并设置进 global_params

    调用顺序->1
    :param echo:
    :return:
    """
    headers = {
        'authority': 'order.kfc.com.cn',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': global_params.user_agent,
    }

    response = requests.get('https://order.kfc.com.cn/preorder-taro/home', headers=headers)
    cookies: dict = response.cookies.get_dict()
    if echo:
        logger.info(f'function:set_volcalb cookies:{cookies}')
    global_params.volcalb = cookies['volcalb'.upper()]
    global_params.volcalb_cors = cookies['volcalbcors'.upper()]
    global_params.route_cell = cookies['route-cell']


def set_session_id(echo=False):
    """
    首次进入设置session_id ，这里要附带门店id，后续就用这个id进行识别

    调用顺序->2
    :param echo:
    :return:
    """
    headers = {
        'authority': 'order.kfc.com.cn',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'origin': 'https://order.kfc.com.cn',
        'pragma': 'no-cache',
        'referer': 'https://order.kfc.com.cn/preorder-taro/settlement',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': global_params.user_agent,
        'x-yumc-client-deviceid': global_params.device_id,
        'x-yumc-route-cell': global_params.route_cell,
        'x-yumc-route-channel': global_params.channel_name,
        'x-yumc-route-usercode': global_params.user_code,
    }

    json_data = {
        'portalType': global_params.portal_type,
        'channelName': global_params.channel_name,
        'channelId': global_params.channel_id,
        'brand': global_params.brand,
        'business': global_params.business,
        'deviceId': global_params.device_id,
        'clientVersion': global_params.client_version,
        'ticket': global_params.first_ticket,
        'fversion': global_params.fversion,
        'versionNum': global_params.version_num,
        'body': {
            'geoLocation': {},
        },
        'storeCodeParent': global_params.store_code_parent,
        'storeCodeCurrent': global_params.store_code_current,
        'bookingDate': global_params.booking_date,
        'env': global_params.env,
    }

    response = requests.post(
        'https://order.kfc.com.cn/preorder-portal/api/v2/init/combine/preorder',
        cookies=global_params.cookies,
        headers=headers,
        json=json_data,
    )
    res: dict = response.json()
    if echo:
        logger.info(f'function:set_session_id res:{res}')
        logger.info(f'function:set_session_id json_data:{json_data}')

    global_params.session_id_cookie = res['data']['sessionId']
    global_params.session_id_cookie_sig = res['data']['sessionId']


def set_login_ticket(echo=False):
    """
    设置登录ticket

    调用顺序->3/6
    :param echo:
    :return:
    """
    headers = {
        'authority': 'order.kfc.com.cn',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'origin': 'https://order.kfc.com.cn',
        'pragma': 'no-cache',
        'referer': 'https://order.kfc.com.cn/preorder-taro/settlement',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': global_params.user_agent,
        'x-yumc-client-deviceid': global_params.device_id,
        'x-yumc-route-cell': global_params.route_cell,
        'x-yumc-route-channel': global_params.channel_name,
        'x-yumc-route-usercode': global_params.user_code,
    }

    json_data = {
        'portalType': global_params.portal_type,
        'channelName': global_params.channel_name,
        'channelId': global_params.channel_id,
        'brand': global_params.brand,
        'business': global_params.business,
        'deviceId': global_params.device_id,
        'clientVersion': global_params.client_version,
        'sessionId': global_params.session_id_cookie,
        'ticket': global_params.first_ticket,
        'fversion': global_params.fversion,
        'versionNum': global_params.version_num,
        'env': global_params.env,

    }

    response = requests.post(
        'https://order.kfc.com.cn/preorder-portal/api/v2/user/login',
        cookies=global_params.cookies,
        headers=headers,
        json=json_data,
    )
    global_params.current_ticket = response.json()['data']['user']['ticket']['0']
    if echo:
        logger.info(f'function:set_login_ticket res:{response.json()}')


def update_cart(items: list, echo=False):
    """
    更新购物车，首次添加购物车会生成一个order_id

    调用顺序->4
    :param items: 购物车列表
    :param echo:
    :return:
    """
    headers = {
        'authority': 'order.kfc.com.cn',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'origin': 'https://order.kfc.com.cn',
        'pragma': 'no-cache',
        'referer': 'https://order.kfc.com.cn/preorder-taro/settlement',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': global_params.user_agent,
        'x-yumc-client-deviceid': global_params.device_id,
        'x-yumc-route-cell': global_params.route_cell,
        'x-yumc-route-channel': global_params.channel_name,
        'x-yumc-route-usercode': global_params.user_code,
    }
    json_data = {
        'portalType': global_params.portal_type,
        'channelName': global_params.channel_name,
        'channelId': global_params.channel_id,
        'brand': global_params.brand,
        'business': global_params.business,
        'deviceId': global_params.device_id,
        'clientVersion': global_params.client_version,
        'sessionId': global_params.session_id_cookie,
        'ticket': global_params.current_ticket,
        'fversion': global_params.fversion,
        'versionNum': global_params.version_num,
        'env': global_params.env,
        'selectProductId': '',
        'items': items,
        'scenceType': '',
    }
    response = requests.post(
        'https://order.kfc.com.cn/preorder-portal/api/v2/cart/update',
        cookies=global_params.cookies,
        headers=headers,
        json=json_data,
    )
    global_params.order_id = response.json()['data']['cart']['id']
    if echo:
        logger.info(f'function:update_cart res:{response.json()}')


def confirm_cart(echo=False):
    """
    确认购物车，确认购物车后才能提交订单

    调用顺序->5
    :param echo:
    :return:
    """
    api = '/preorder-portal/api/v2/cart/confirm'
    json_data = {
        'portalType': global_params.portal_type,
        'channelName': global_params.channel_name,
        'channelId': global_params.channel_id,
        'brand': global_params.brand,
        'business': global_params.business,
        'deviceId': global_params.device_id,
        'clientVersion': global_params.client_version,
        'sessionId': global_params.session_id_cookie,
        'ticket': global_params.current_ticket,
        'fversion': global_params.fversion,
        'versionNum': global_params.version_num,
        'env': global_params.env,
        'cartId': global_params.order_id,
    }
    headers: dict = global_params.safe_headers(api, json.dumps(json_data))
    response = requests.post(
        f'https://order.kfc.com.cn{api}',
        cookies=global_params.cookies,
        headers=headers,
        json=json_data,
    )
    if echo:
        logger.info(f'function:confirm_cart res:{response.json()}')


def submit_order(echo=False):
    """
    确认订单

    调用顺序->6
    :return:
    """
    api = '/preorder-portal/api/v2/order/submit'
    json_data = {
        'portalType': global_params.portal_type,
        'channelName': global_params.channel_name,
        'channelId': global_params.channel_id,
        'brand': global_params.brand,
        'business': global_params.business,
        'deviceId': global_params.device_id,
        'clientVersion': global_params.client_version,
        'sessionId': global_params.session_id_cookie,
        'ticket': global_params.current_ticket,
        'fversion': global_params.fversion,
        'versionNum': global_params.version_num,
        'env': global_params.env,
        'phone': global_params.phone,
        'packType': 1,  # 打包带走
        'iremark': '',
        'orderId': global_params.order_id,
        'queryThirdParam': '',
        'riskCtrlParam': {
            'channelName': global_params.channel_name,
            'openId': '',
            'browserId': 'bid_' + global_params.device_id,
            'deviceId': global_params.device_id,
            'td_id': '',
        },
    }
    headers: dict = global_params.safe_headers(api, json.dumps(json_data))
    response = requests.post(
        'https://order.kfc.com.cn' + api,
        cookies=global_params.cookies,
        headers=headers,
        json=json_data,
    )
    if echo:
        logger.info(f'function:submit_order res:{response.json()}')


def init_session(echo=False):
    """
    初始化session，准备进入支付页面

    调用顺序->7
    :return:
    """
    api = '/preorder-portal/api/v2/init/initSession'
    json_data = {
        'portalType': global_params.portal_type,
        'channelName': global_params.channel_name,
        'channelId': global_params.channel_id,
        'brand': global_params.brand,
        'business': global_params.business,
        'deviceId': global_params.device_id,
        'clientVersion': global_params.client_version,
        'ticket': global_params.current_ticket,
        'fversion': global_params.fversion,
        'versionNum': global_params.version_num,
    }
    headers: dict = global_params.safe_headers(api, json.dumps(json_data))
    response = requests.post(
        'https://order.kfc.com.cn' + api,
        cookies=global_params.cookies,
        headers=headers,
        json=json_data,
    )
    global_params.session_id_cookie = response.json()['data']['sessionId']
    global_params.session_id_cookie_sig = response.json()['data']['sessionId']

    if echo:
        logger.info(f'function:init_session res:{response.json()}')


def order_pay(echo=False):
    """
    选择支付方式准备支付

    调用顺序8
    :param echo:
    :return:
    """
    api = '/cashier/unifiedOrderPay'
    json_data = {
        'orderInfo': {
            'bookingDate': global_params.booking_date,
            'donation': 0,
            'goodsDetail': [
                {
                    'goodsId': '100004774',  # 订单购物车单号
                    'promotionFlag': 'YES',
                    'financeDepartmentCode': '1',
                },
            ],
            'isAnotherDay': '1',
            'orderAmount': 650,  # 价格
            'orderId': global_params.order_id,
            'orderSendTime': global_params.order_send_time,
            'payDetail': [
                {
                    'payAmount': 650,
                    'channel': 'EKFCPAY',
                    'productCode': 'EKFC_H5',
                    'payNo': 0,
                    'portalType': global_params.portal_type,
                    'returnUrl': f'https://order.kfc.com.cn/preorder-taro/order/kfcOrderDetails/detail/index?orderId={global_params.order_id}&opener=settlement&type=1&paystatus=&isSettlePage=true',
                },
            ],
            'promotionFlag': 'YES',
            'storeCode': global_params.store_code_parent,
            'businessApp': 'KFC_PRE',
        },
        'payNo': 0,
        'token': global_params.current_ticket,
    }
    headers: dict = global_params.safe_headers(api, json.dumps(json_data))
    response = requests.post(
        'https://order.kfc.com.cn' + api,
        cookies=global_params.cookies,
        headers=headers,
        json=json_data,
    )
    global_params.payment_url = response.json()['data']['paymentUrl']
    if echo:
        logger.info(f'function:order_pay res:{response.json()}')


def set_jsp_param(echo=False):
    """

    调用顺序9
    :param echo:
    :return:
    """
    headers = {
        'authority': 'card.yumchina.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'referer': 'https://order.kfc.com.cn/',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': global_params.user_agent,
    }

    response = requests.get(
        global_params.payment_url,
        headers=headers,
    )
    soup = BeautifulSoup(response.text, 'html.parser')

    # 提取signature、userCode、phoneHash和phoneMask的值
    global_params.signature = soup.find('input', {'id': 'signature'}).get('value')
    global_params.phone_hash = soup.find('input', {'id': 'phoneHash'}).get('value')
    global_params.phone_mask = soup.find('input', {'id': 'phoneMask'}).get('value')

    # 找到id为'cashierForm'的表单内的所有隐藏input标签
    inputs = soup.find('form', id='cashierForm').find_all('input', type='hidden')

    data_dict = {}

    for input_field in inputs:
        # 获取每个input标签的name和value属性
        name = input_field['name']
        value = input_field['value']
        if name == 'originalUrl':
            value = value.replace('https://card.yumchina.com/card-pay', '')
        if name in ('notifyUrl', 'originalUrl'):
            value = urllib.parse.quote(value, safe='*')
        # 将它们添加到字典中
        data_dict[name] = value

    # 将字典转换为查询字符串形式
    data = '&'.join([f"{k}={v}" for k, v in data_dict.items()])
    data += f'&paymentPwd={global_params.password}'
    global_params.cashier_data = data


def cashier_assess_risk(echo=False):
    """
    支付风险评估

    调用顺序10
    :param echo:
    :return:
    """
    headers = {
        'authority': 'card.yumchina.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'origin': 'https://card.yumchina.com',
        'pragma': 'no-cache',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
        'x-requested-with': 'XMLHttpRequest',
    }
    params = {
        'signature': global_params.signature,
    }

    json_data = {
        'userCode': global_params.user_code,
        'phoneHash': global_params.phone_hash,
        'phoneMask': global_params.phone_mask,
        'issuerBrandId': '002',
        'eventName': 'PAY_FOR',
        'userAgent': global_params.user_agent,
        'clientId': 'unique-test-' + uuid4(),
        'transTime': global_params.now,
    }
    response = requests.post(
        'https://card.yumchina.com/card-pay/rest/assessRisk',
        params=params,
        cookies=global_params.cookies,
        headers=headers,
        json=json_data,
    )
    print(response.text)


def complete_payment():
    """
    支付完成

    :return:
    """
    cookies = global_params.cookies
    cookies.pop('locale')
    cookies.pop('sessionIdCookie')
    cookies.pop('sessionIdCookie.sig')
    cookies['errorTimesCookie'] = '-2'
    headers = {
        'authority': 'card.yumchina.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://card.yumchina.com',
        'pragma': 'no-cache',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': global_params.user_agent,
    }

    response = requests.post('https://card.yumchina.com/card-pay/servlet/cashier', cookies=global_params.cookies,
                             headers=headers,
                             data=global_params.cashier_data)
    print(response.text)
