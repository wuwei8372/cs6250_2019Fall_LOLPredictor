# python2 analyze.py

import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, col, collect_list, desc

heros = {}
with open('hero.json') as input:
    data = json.load(input)
    for id in data:
        heros[data[id]['key']] = id

sc = SparkSession \
    .builder \
    .appName("Flask on Spark") \
    .getOrCreate()

"""
sc.conf.set("spark.sql.shuffle.partitions", "400")
sc.conf.set("spark.default.parallelism", "400")
sc.conf.set("spark.driver.memory", "5g")
sc.conf.set("spark.executor.memory", "5g")
"""

gamesDF = sc.read.json('combined.txt')
# gameDF.printSchema()
games_count = gamesDF.count()
print gamesDF.count()

participantsDF = gamesDF.select('gameId', explode('participants').alias('participant'))
# participantsDF.show()
print participantsDF.count()

usageDF = participantsDF.select('participant.championId').groupBy('championId').count()
# usageDF.show()

usageRateDF = usageDF.withColumn('usage_rate', col('count') / games_count)
usageRateDF.show()
print usageRateDF.count()

championIdwinDF = participantsDF.select('participant.championId', 'participant.stats.win')

winDF = championIdwinDF.filter(championIdwinDF['win']).groupBy('championId').count()
winDF = winDF.withColumnRenamed('count', 'win_count')
# winDF.show()

winRateDF = usageDF.join(winDF, 'championId', 'left_outer').fillna(0) \
    .withColumn('win_rate', col('win_count') / col('count'))
winRateDF.show()
print winRateDF.count()

rateDF = usageRateDF.join(winRateDF, 'championId') \
    .select('championId', 'usage_rate', 'win_rate')
rateDF.printSchema()
# rateDF.show()
print rateDF.count()

rates = rateDF.toJSON().map(lambda row: json.loads(row)).collect()
rates_map = {r['championId']: r for r in rates}

teamDF = participantsDF.select('gameId', 'participant.championId', 'participant.teamId') \
    .groupby('gameId', 'teamId').agg(collect_list('championId').alias('team'))
teamDF.show()

teammateDF = teamDF.select(explode('team').alias('championId'), 'team')
teammateDF.show()

teammateDF = teammateDF.select('championId', explode('team').alias('teammateId')) \
    .filter(col('championId') != col('teammateId'))
teammateDF.show()
print teammateDF.count()

entries = []
for heroId in heros:
    championId = long(heroId)

    entry = {'key': heroId}
    for key in ['usage_rate', 'win_rate']:
        entry[key] = '0%'
        if championId in rates_map:
            entry[key] = "{:.0%}".format(rates_map[championId][key])

    topTeammateDF = teammateDF.filter(col('championId') == championId).select('teammateId') \
        .groupBy('teammateId').count().sort(desc('count')).limit(5)
        
    entry['top_teammates'] = [heros[str(top_teammate['teammateId'])]
                              for top_teammate in topTeammateDF.collect()]
    entries += [entry]
    print entry

sc.stop()

with open('bigDataResult_Array.json', 'w') as output:
    json.dump(entries, output, indent=4)

entries_map = {entry['key']: entry for entry in entries}
[entries_map[key].pop('key') for key in entries_map]

with open('bigDataResult_JSON.json', 'w') as output:
    json.dump(entries_map, output, indent=4)