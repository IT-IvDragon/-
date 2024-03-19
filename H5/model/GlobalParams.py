import time
from hashlib import md5

from KFCSpider.H5.utils import device_id, uuid4, timestamp_next_day, format_timestamp


class GlobalParams:
    def __init__(self, ticket, user_code, phone, password, business: str = 'preorder'):
        self.user_code: str
        self.locale: str
        self.route_cell: str
        self.session_id_cookie: str
        self.session_id_cookie_sig: str
        self.volcalb: str
        self.volcalb_cors: str
        self.user_agent: str
        self.portal_type: str
        self.channel_name: str
        self.channel_id: str
        self.brand: str
        self.business: str  # 预定
        self.device_id: str
        self.client_version: str
        self.first_ticket: str
        self.current_ticket: str
        self.fversion: str
        self.version_num: str
        self.store_code_parent: str  # 店铺id
        self.store_code_current: str  # 店铺id
        self.booking_date: str  # 预定时间，默认选明天9:15分早餐
        self.env: str
        self.order_id: str  # 订单id
        self.kbck: str
        self.phone: str
        self.payment_url: str
        self.signature: str
        self.phone_hash: str
        self.phone_mask: str
        self.cashier_data: str
        self.password: str
        self.order_send_time: str
        self.__attribute_init(ticket, user_code, phone, password, business)

    def __attribute_init(self, ticket, user_code, phone, password, business):
        """
        属性初始化

        :return:
        """
        self.session_id_cookie = ''
        self.session_id_cookie_sig = ''
        self.volcalb = ''
        self.volcalb_cors = ''
        self.user_code = user_code
        self.locale = 'zh-cn'
        self.route_cell = 'yumc4'
        self.user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1'
        self.portal_type = 'WAP'
        self.channel_name = 'Mobile Web'
        self.channel_id = '13'
        self.brand = 'KFC_PRE'
        self.business = business  # 预定
        self.device_id = device_id()
        self.client_version = 'v4.301(0ef76a5b)'
        self.first_ticket = ticket
        self.current_ticket = ''
        self.fversion = '240220'
        self.version_num = '5'
        self.store_code_parent = 'GZ1050'
        self.store_code_current = 'GZ1050'
        self.booking_date = timestamp_next_day()
        self.order_send_time = format_timestamp(self.booking_date)
        self.env = 'qcpil'
        self.order_id = ''
        self.kbck = 'kbwapzJAAUs1g2od'
        self.phone = phone
        self.payment_url = ''
        self.signature = ''
        self.phone_hash = ''
        self.phone_mask = ''
        self.cashier_data = ''
        self.password = password

    @property
    def cookies(self) -> dict:
        return {
            'locale': self.locale,
            'route-cell': self.route_cell,
            'VOLCALBCORS': self.volcalb_cors,
            'VOLCALB': self.volcalb,
            'sessionIdCookie': self.session_id_cookie,
            'sessionIdCookie.sig': self.session_id_cookie_sig,
        }

    @property
    def now(self) -> int:
        return int(round(time.time() * 1000))

    def safe_headers(self, api: str, json_data: str) -> dict:
        """
        获取安全请求头

        :param api: 请求的api后缀 例如'/preorder-portal/api/v2/cart/confirm'
        :param json_data: json_data的json字符串格式
        :return: headers
        """
        now = str(self.now)
        kbsv = f'{self.kbck}\tfegFLVMJJ88If2hp\t{now}\t{api}\t\t{json_data}'
        uuid = uuid4()
        headers = {
            'authority': 'order.kfc.com.cn',
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'content-type': 'application/json',
            'kbck': self.kbck,
            'kbcts': now,
            'kbsv': md5(kbsv.encode()).hexdigest(),
            'origin': 'https://order.kfc.com.cn',
            'pragma': 'no-cache',
            'rcsav': '',
            'rcsbcid': 'unique-test-' + uuid,
            'rcsdcid': 'unique-test-' + uuid,
            'referer': 'https://order.kfc.com.cn/preorder-taro/settlement',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sysbrand': 'kfc',
            'syschannel': 'preorder',
            'user-agent': self.user_agent,
            'x-yumc-client-deviceid': self.device_id,
            'x-yumc-route-cell': self.route_cell,
            'x-yumc-route-channel': self.channel_name,
            'x-yumc-route-usercode': self.user_code,
        }
        return headers
