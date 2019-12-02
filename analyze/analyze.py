# python2 analyze.py

from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, col, collect_list, desc

sc = SparkSession.builder.appName("Spark").getOrCreate()

sc.conf.set("spark.default.parallelism", '10')
sc.conf.set("spark.sql.shuffle.partitions", "400")

gamesDF = sc.read.json('combined.txt')
gamesDF.printSchema()
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

teamDF = participantsDF.select('gameId', 'participant.championId', 'participant.teamId') \
    .groupby('gameId', 'teamId').agg(collect_list('championId').alias('team'))
teamDF.show()

teammateDF = teamDF.select(explode('team').alias('championId'), 'team')\
    .select('championId', explode('team').alias('teammateId')) \
    .filter(col('championId') != col('teammateId'))
teammateDF.show()
print teammateDF.count()

from operator import add
topTeammateDF = teammateDF.rdd \
    .map(lambda x: ((x[0], x[1]), 1)) \
    .reduceByKey(add) \
    .map(lambda x: (x[0][0], [(x[0][1], x[1])]))\
    .reduceByKey(add) \
    .mapValues(lambda vs: sorted(vs, key=lambda x: x[1], reverse=True)[: 5]) \
    .mapValues(lambda vs: [v[0] for v in vs]) \
    .toDF(['championId', 'top_teammates'])
topTeammateDF.show()
print topTeammateDF.count()

resultDF = usageRateDF.join(winRateDF, 'championId').join(topTeammateDF, 'championId') \
    .select('championId', 'usage_rate', 'win_rate', 'top_teammates')
resultDF.printSchema()

import json
results = resultDF.toJSON().map(lambda row: json.loads(row)).collect()
result_map = {r['championId']: r for r in results}

sc.stop()

heros = {}
with open('hero.json') as input:
    data = json.load(input)
    for id in data:
        heros[data[id]['key']] = id

entries = []
for heroId in heros:
    entry = {'key': heroId, 'usage_rate': '0%', 'win_rate': '0%', 'top_teammates': []}

    championId = long(heroId)
    if championId in result_map:
        for key in ['usage_rate', 'win_rate']:
            entry[key] = "{:.0%}".format(result_map[championId][key])
        key = 'top_teammates'
        entry[key] = [heros[str(t)] for t in result_map[championId][key]]

    entries += [entry]

with open('bigDataResult_Array.json', 'w') as output:
    json.dump(entries, output, indent=4)

entries_map = {entry['key']: entry for entry in entries}
[entries_map[key].pop('key') for key in entries_map]

with open('bigDataResult_JSON.json', 'w') as output:
    json.dump(entries_map, output, indent=4)