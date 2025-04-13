import json
import pandas as pd

from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient('mongodb+srv://giuseppericcio:1234@cluster0.weahziy.mongodb.net/?retryWrites=true&w=majority')

    df = pd.read_csv('./relations.csv', header=None)
    df.columns = ['source', 'relationType', 'destination']

    db = client.healthcare
    relations = db.relations

    docs = json.loads(df.to_json(orient='records'))

    relations.delete_many({})
    relations.insert_many(docs)

    print(relations.count_documents({}))
