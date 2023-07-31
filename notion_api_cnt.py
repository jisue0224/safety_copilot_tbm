import os
import pandas as pd
import requests
import streamlit as st


NOTION_TOKEN = st.secrets['NOTION_TOKEN2']
DATABASE_ID = st.secrets['DATABASE_ID2']


headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

def get_pages(num_pages=None):
    """
    If num_pages is None, get all pages, otherwise just the defined number.
    """
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

    get_all = num_pages is None
    page_size = 100 if get_all else num_pages

    payload = {"page_size": page_size}
    response = requests.post(url, json=payload, headers=headers)

    data = response.json()

    # Comment this out to dump all data to a file
    # import json
    # with open('db.json', 'w', encoding='utf8') as f:
    #    json.dump(data, f, ensure_ascii=False, indent=4)

    results = data["results"]
    while data["has_more"] and get_all:
        payload = {"page_size": page_size, "start_cursor": data["next_cursor"]}
        url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        results.extend(data["results"])

    return results


def insert_data(data: dict):
    url = 'https://api.notion.com/v1/pages'
    payload = {"parent": {"database_id": DATABASE_ID}, "properties": data}
    res = requests.post(url, json=payload, headers=headers)
    # print(f"response_status_code: {res.status_code}")
    return True


if __name__ == "__main__":
    
    
    # print(get_pages())
    
    name = "박보검"
    data = {
        "Name" : {"title": [{"text": {"content": name}}]},
        }
    
    insert_data(data)
