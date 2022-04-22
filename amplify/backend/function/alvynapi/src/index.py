# import json

# def handler(event, context):
#     print('received event:')
#     print(event)
    
#     return {
#         'statusCode': 200,
#         'headers': {
#             'Access-Control-Allow-Headers': '*',
#             'Access-Control-Allow-Origin': '*',
#             'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
#         },
#         'body': json.dumps('Hello from your new Amplify Python lambda!')
#     }

import os
import awsgi
import boto3
from uuid import uuid4
from flask_cors import CORS
from flask import Flask, jsonify, request

BASE_ROUTE = "/song"
ENV = os.environ.get("ENV")
REGION = os.environ.get("REGION")
ARN = os.environ.get("STORAGE_ALVYNDB_ARN")
TABLE = os.environ.get("STORAGE_ALVYNDB_NAME")

client = boto3.client("dynamodb", region_name=REGION)
app = Flask(__name__)
CORS(app)

@app.route(BASE_ROUTE, methods=["POST"])
def create_song():
    try:
        request_json = request.get_json()
    except Exception as e:
        print(e)
        return jsonify(message="invalid body"), 400
    try:
        client.put_item(TableName=TABLE, Item={
            "id": {'S': str(uuid4())},
            "name": {'S': request_json.get("name")},
            "year": {'S': request_json.get("year")},
            "link": {'S': request_json.get("link")}
        })
        return jsonify(message="item created successfully!"), 201
    except Exception as e:
        print(e)
        return jsonify(message="invalid body!"), 400


@app.route(BASE_ROUTE + "/<song_id>", methods=["GET"])
def get_song(song_id):
    try:
        song = client.get_item(TableName=TABLE, Key={
            "id": {
                'S': song_id,
            }
        })
        return jsonify(data=song), 200
    except Exception as e:
        print(e)
        return jsonify(message="error geting song!"), 500


@app.route(BASE_ROUTE, methods=["GET"])
def list_songs():
    return jsonify(data=client.scan(TableName=TABLE)), 200


@app.route(BASE_ROUTE + "/<song_id>", methods=["DELETE"])
def delete_song(song_id):
    try:
        client.delete_item(TableName=TABLE, Key={"id": {'S': song_id}})
        return jsonify(message="song deleted successfully")
    except Exception as e:
        print(e)
        return jsonify(message="error deleting!"), 500


@app.route(BASE_ROUTE + "/<song_id>", methods=["PUT"])
def update_song(song_id):
    try:
        request_json = request.get_json()
    except Exception as e:
        return jsonify(message="Invalid Body!"), 400
    
    
    try:
        name = request_json.get("name")
    except Exception as e:
        print("name", e)
        name = None
    
    try:
        year = request_json.get("year")
    except Exception as e:
        print("year", e)
        year = None
    
    try:
        link = request_json.get("link")
    except Exception as e:
        print("link", e)
        link = None

    if name is None and year is None and link is None:
        return jsonify(message="Invalid Body!"), 400

    UpdateExpression = "SET"
    ExpressionAtributeNames = {}
    ExpressionAtributeValues = {}

    if name is not None:
        UpdateExpression += " #name = :name"
        ExpressionAtributeNames |= {"#name": "name"}
        ExpressionAtributeValues |= {":name": name}
    if year is not None:
        UpdateExpression += " #year = :year"
        ExpressionAtributeNames |= {"#year": "year"}
        ExpressionAtributeValues |= {":year": year}
    if link is not None:
        UpdateExpression += " #link = :link"
        ExpressionAtributeNames |= {"#link": "link"}
        try:
            ExpressionAtributeValues |= {":link", link}
        except ValueError as e:
            print(e)
            ExpressionAtributeValues.update({":link": link})
    
    try:
        client.update_item(
            TableName=TABLE, 
            Key={"id": {'S': song_id}}, 
            UpdateExpression=UpdateExpression,
            ExpressionAtributeNames=ExpressionAtributeNames,
            ExpressionAtributeValues=ExpressionAtributeValues
        )
        return jsonify("Updated successfully!")
    except Exception as e:
        print(e)
        return jsonify("Update Error!"), 500


def handler(event, context):
    return awsgi.response(app, event, context)