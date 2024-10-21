from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError 
import csv


es = Elasticsearch("http://localhost:9200/")


def createCollection(p_collection_name):
    if not es.indices.exists(index=p_collection_name):
        es.indices.create(index=p_collection_name)
        print(f"Index {p_collection_name} created.")
    else:
        print(f"Index {p_collection_name} already exists.")


def indexData(p_collection_name, p_exclude_column):

    with open('C:/Users/ADMIN/Downloads/archive/Employee Sample Data 1.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
       

        for row in reader:
            if p_exclude_column in row:
                del row[p_exclude_column]
            es.index(index=p_collection_name, document=row)
        print(f"Data indexed into {p_collection_name}, excluding column {p_exclude_column}.")


def searchByColumn(p_collection_name, p_column_name, p_column_value):
    query = {
        "query": {
            "match": {
                p_column_name: p_column_value
            }
        }
    }
    print(f"Running query: {query}")
    result = es.search(index=p_collection_name, body=query)
    print(f"Search results for {p_column_name} = {p_column_value}:")
    for hit in result['hits']['hits']:
        print(hit['_source'])
    if not result['hits']['hits']:
        print("No results found.")


def getEmpCount(p_collection_name):
    count = es.count(index=p_collection_name)['count']
    print(f"Total employees in {p_collection_name}: {count}")
    return count


def checkMapping(p_collection_name):
    mapping = es.indices.get_mapping(index=p_collection_name)
    print(f"Mapping for {p_collection_name}:")
    print(mapping)

def checkEmployeeExists(p_collection_name, p_employee_id):
    query = {
        "query": {
            "term": {
                "Employee ID": p_employee_id
            }
        }
    }
    
    result = es.search(index=p_collection_name, body=query)
    if result['hits']['total']['value'] > 0:
        print(f"Found {result['hits']['total']['value']} document(s) with Employee ID {p_employee_id}.")
        for hit in result['hits']['hits']:
            print(f"Document ID: {hit['_id']}, Document: {hit['_source']}")
    else:
        print(f"No documents found with Employee ID {p_employee_id}.")

def deleteByEmployeeId(p_collection_name, p_employee_id):

    checkEmployeeExists(p_collection_name, p_employee_id)

    query = {
        "query": {
            "match": {
                "Employee ID": p_employee_id
            }
        }
    }

    response = es.delete_by_query(index=p_collection_name, body=query)
    print("Delete by query response:", response)

    if response['deleted'] > 0:
        print(f"Deleted {response['deleted']} document(s) with Employee ID {p_employee_id}.")
    else:
        print(f"No documents found with Employee ID {p_employee_id} to delete.")


def getDepFacet(p_collection_name):
    query = {
        "size": 0,
        "aggs": {
            "department_count": {
                "terms": {
                    "field": "Department.keyword"
                }
            }
        }
    }
    result = es.search(index=p_collection_name, body=query)
    print("Department facet results:")
    for bucket in result['aggregations']['department_count']['buckets']:
        print(f"Department: {bucket['key']}, Count: {bucket['doc_count']}")

v_nameCollection = 'hash_krishnaveni'  
v_phoneCollection = 'hash_2916'          

#createCollection(v_nameCollection)
#createCollection(v_phoneCollection)


#getEmpCount(v_nameCollection)


#indexData(v_nameCollection, 'Department') 
#indexData(v_phoneCollection, 'Gender')      

#checkMapping(v_nameCollection)
#deleteByEmployeeId(v_nameCollection, 'E02003')


#getEmpCount(v_nameCollection)


#searchByColumn(v_nameCollection, 'Department', 'IT')     
#searchByColumn(v_nameCollection, 'Gender', 'Male')      
#searchByColumn(v_phoneCollection, 'Department', 'IT')   


#getDepFacet(v_nameCollection)
getDepFacet(v_phoneCollection)


