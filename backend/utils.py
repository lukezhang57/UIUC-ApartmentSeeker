# from pymongo import MongoClient
# def get_db_handle(db_name, host, port, username, password):
#
#     client = MongoClient(host=host,
#                       port=int(port),
#                       username=username,
#                       password=password
#                      )
#     db_handle = client['db_name']
#     return db_handle, client
#
# def get_collection_handle(db_handle,collection_name):
#     return db_handle[collection_name]
# Code copied from django. Will set up pymongo this week