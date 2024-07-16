from neo4j import GraphDatabase
import os

with open('.env', 'r') as fh:
    vars_dict = dict(
        tuple(line.replace('\n', '').split('='))
        for line in fh.readlines() if not line.startswith('#'))

os.environ.update(vars_dict)

database_uri = os.getenv("DATABASE_URL")
database_user = os.getenv("DATABASE_USER")
database_password = os.getenv("DATABASE_PASSWORD")
URI = database_uri
AUTH = (database_user, database_password)

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()

driver = GraphDatabase.driver(URI, auth=AUTH)
session = driver.session(database="neo4j")

records, summary, keys = driver.execute_query(
"MATCH (tom:Person {name: $name})-[:ACTED_IN]->(tomHanksMovies) RETURN tom,tomHanksMovies",
    name="Tom Hanks",
    database_="neo4j",
)

for record in records:
    print(record)

# Summary information
print("The query `{query}` returned {records_count} records in {time} ms.".format(
    query=summary.query, records_count=len(records),
    time=summary.result_available_after,
))

session.close()
driver.close()