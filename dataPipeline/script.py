import requests
import json
import time

headers = {
    "Origin": "https://developer.riotgames.com",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Riot-Token": "RGAPI-1f4eeae1-fe3e-4512-a7e6-930a1f136d63",
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36"
}

filepath = 'gameId'
# f = open('gameId', 'r')
# content = f.read()
# print(content)
# fp = open(filepath)
with open('out.txt', 'w') as target:
    with open(filepath) as fp:
        for cnt, line in enumerate(fp):
            # print(type(line))
            # print("Line {}: {}".format(cnt, line))
            # target.write(line)
            matchId = line.strip()
            # print(matchId)
            url = "https://euw1.api.riotgames.com/lol/match/v4/matches/{0}".format(matchId)
            # print(url == "https://euw1.api.riotgames.com/lol/match/v4/matches/3326086514")
            response = requests.get(url=url, headers=headers)
            if response.status_code == 200:
                print(cnt)
                # print(json.loads(response.content))
                target.write(response.text)
                target.write('\n')
            else:
                print(response.status_code)
            time.sleep(3)
        
# matchId = '3330080762'
# response = requests.get(url="https://euw1.api.riotgames.com/lol/match/v4/matches/{0}".format(matchId), headers=headers)

# if response.status_code == 200:
#     print(json.loads(response.content))
# else:
#     print(response.status_code)

