# -*- encoding: utf-8 -*-

import requests

cookies = {
	'BIDUPSID': '2C38F3EB848A082341E751BAED2BC2FA',
	'PSTM': '1666017860',
	'BAIDUID': '2C38F3EB848A08231F2FC958AC261F79:FG=1',
	'BD_UPN': '12314753',
	'BDORZ': 'B490B5EBF6F3CD402E515D22BCDA1598',
	'BA_HECTOR': '0500ag0l8g25012g8ga126qc1hl2ppb1a',
	'BAIDUID_BFESS': '2C38F3EB848A08231F2FC958AC261F79:FG=1',
	'ZFY': 'TBZVN1ED8yM4eAQ6wGGPTH0OPaPbyZNmeHwz4jpsubs:C',
	'baikeVisitId': '43179892-7680-40af-bae0-3b55f1a3f5b3',
	'delPer': '0',
	'BD_CK_SAM': '1',
	'PSINO': '7',
	'H_PS_PSSID': '36561_37584_36884_37486_36807_36786_37532_37497_26350_37371',
	'H_PS_645EC': '1fc3CbZpKIDdoSN7Wm7Y7GUGosO8XkKSTTstqL9QT0fa7oTkNcJPtdIQMqM',
	'BDSVRTM': '0',
}

headers = {
	'Connection': 'keep-alive',
	'Cache-Control': 'max-age=0',
	'sec-ch-ua': '"Chromium";v="21", " Not;A Brand";v="99"',
	'sec-ch-ua-mobile': '?0',
	'sec-ch-ua-platform': '"Windows"',
	'Upgrade-Insecure-Requests': '1',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
	'Sec-Fetch-Site': 'none',
	'Sec-Fetch-Mode': 'navigate',
	'Sec-Fetch-User': '?1',
	'Sec-Fetch-Dest': 'document',
	'Accept-Language': 'zh-CN,zh;q=0.9'}

if __name__ == "__main__":
	response = requests.get('https://www.baidu.com/s?wd=%27Connection+aborted.%27%2C+RemoteDisconnected(%27Remote+end+closed+connection+without+response%27&ie=UTF-8', cookies=cookies, headers=headers)
