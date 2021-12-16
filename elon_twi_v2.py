import json
import requests
import brotli #Необходимо, чтобы был установлен, используется неявно в запросах

"""URL на json из которого скриптом заполняется страница с твитами"""
url_elon = 'https://twitter.com/i/api/graphql/QvCV3AU7X1ZXr9JSrH9EOA/UserTweets?variables=%7B%22userId%22%3A%2244196397%22%2C%22count%22%3A20%2C%22withTweetQuoteCount%22%3Atrue%2C%22includePromotedContent%22%3Atrue%2C%22withQuickPromoteEligibilityTweetFields%22%3Atrue%2C%22withSuperFollowsUserFields%22%3Atrue%2C%22withBirdwatchPivots%22%3Afalse%2C%22withDownvotePerspective%22%3Afalse%2C%22withReactionsMetadata%22%3Afalse%2C%22withReactionsPerspective%22%3Afalse%2C%22withSuperFollowsTweetFields%22%3Atrue%2C%22withVoice%22%3Atrue%2C%22withV2Timeline%22%3Afalse%7D'


def twitter_simulation(url):

    """Заголовки для запроса"""
    header = {
        'authority': 'twitter.com',
        'method': 'GET',
        'path': '/i/api/graphql/7mjxD3-C6BxitPMVQ6w0-Q/UserByScreenName?variables=%7B%22screen_name%22%3A%22elonmusk%22%2C%22withSafetyModeUserFields%22%3Atrue%2C%22withSuperFollowsUserFields%22%3Atrue%7D',
        'scheme': 'https',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'ru,en;q=0.9',
        'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
        'content-type': 'application/json',
        'cookie': 'guest_id_marketing=v1%3A163957091488036374; guest_id_ads=v1%3A163957091488036374; _sl=1; kdt=fQmdkEs3UYOT73urIejzSJtT2LCakOxvJYbKSJ6N; dnt=1; att=1-vXOWlAglTzDv8CcbotWG6SOCiRb68LLiSdWOtQTh; personalization_id="v1_yLX0CmdcYK4i18VH1ANA3A=="; guest_id=v1%3A163957149380193698; ct0=dc68560651e292c91f67198969d86e46; gt=1471402477887135749',
        'referer': 'https://twitter.com/elonmusk',
        'sec-ch-ua': '"Chromium";v="94", "Yandex";v="21", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': "Windows",
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.85 YaBrowser/21.11.3.927 Yowser/2.5 Safari/537.36',
        'x-csrf-token': 'dc68560651e292c91f67198969d86e46',
        'x-guest-token': '1471402477887135749',
        'x-twitter-active-user': 'yes',
        'x-twitter-client-language': 'ru',
        'variables': '%7B%22screen_name%22%3A%22elonmusk%22%2C%22withSafetyModeUserFields%22%3Atrue%2C%22withSuperFollowsUserFields%22%3Atrue%7D}'
    }

    session = requests.Session()
    resp = session.get(url, headers=header)
    print(resp.status_code)

    """Парсинг json"""
    twi_json = json.loads(resp.text)['data']['user']['result']['timeline']['timeline']['instructions']

    for twi in twi_json:
        for i in range(11):
            try:
                tmp = twi['entries'][i]['content']['itemContent']['tweet_results']['result']['legacy']
                if tmp['full_text'][:5] == 'https':
                    continue
                else:
                    print(tmp['full_text'] + ' - ' + 'https://twitter.com/elonmusk/status/' + tmp['id_str'])
            except:
                continue
            
    session.close()


if __name__ == "__main__":
    twitter_simulation(url_elon)
