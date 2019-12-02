import json
# read file
filepath = 'test.txt'
with open('out-select.txt', 'w') as target:
    with open(filepath) as fp:
        for cnt, line in enumerate(fp):
            obj = json.loads(line)
            temp1 = str(obj["gameId"])
            status = obj["teams"][0]["win"]
            count = 0
            temp2, temp3, res = "", "", ""
            for subline in obj["participants"]:
                if(count < 5):
                    temp2 += str(subline["championId"]) + ' '
                    count += 1
                else:
                    temp3 += str(subline["championId"]) + ' '
            if(status == "Win"):
                res = temp1 + ' ' + temp2 + temp3
            else:
                res = temp1 + ' ' + temp3 + temp2
            target.write(res)
            target.write('\n')