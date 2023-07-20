import os
import pandas as pd
import requests
import streamlit as st

NOTION_TOKEN = st.secrets['NOTION_TOKEN1']
DATABASE_ID = st.secrets['DATABASE_ID']

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
    import json
    with open('db.json', 'w', encoding='utf8') as f:
       json.dump(data, f, ensure_ascii=False, indent=4)

    results = data["results"]
    while data["has_more"] and get_all:
        payload = {"page_size": page_size, "start_cursor": data["next_cursor"]}
        url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        results.extend(data["results"])

    return results


def check_duplicate(사번:str, booking_date: str, table_number: str):
    
    target = get_pages()
    df = read_as_df(target)
    중복테이블 = df.loc[(df["booking_date"]==booking_date)&(df["table_number"]==str(table_number))]["고유번호"].values
    중복사번 = df.loc[(df["booking_date"]==booking_date)&(df["사번"]==사번)]["고유번호"].values

    if len(중복테이블) == 0 and len(중복사번) == 0:
        return True
    
    else:
        return False



def insert_data(data: dict, 사번, booking_date, table_number):
    
    if check_duplicate(사번, booking_date, table_number):
        url = 'https://api.notion.com/v1/pages'
        payload = {"parent": {"database_id": DATABASE_ID}, "properties": data}
        res = requests.post(url, json=payload, headers=headers)
        print(f"response_status_code: {res.status_code}")
        return True, st.info("입력 성공")
    else:
        print("중복데이터 입력 오류")
        return False, st.info("중복데이터 입력 오류")
    


def read_as_df(target):
    pages = target
    id_list, dept_list, sub_list, name_list, tbm_list, status_list, time_list = [], [], [], [], [], [], []
    
    for page in pages:
        page_id = page["id"]
        props = page["properties"]
        
        dept_name = props['dept_name']['title'][0]['text']['content']
        sub_name = props['sub_name']['rich_text'][0]['text']['content']
        name = props['name']['rich_text'][0]['text']['content']
        tbm_result = props['tbm_result']['rich_text'][0]['text']['content']
        status = props['status']['rich_text'][0]['text']['content']
        created_time = props['Created time']['created_time']

        id_list.append(page_id)
        dept_list.append(dept_name)
        sub_list.append(sub_name)
        name_list.append(name)
        tbm_list.append(tbm_result)
        status_list.append(status)
        time_list.append(created_time)

        df = pd.DataFrame(list(zip(id_list, dept_list, sub_list, name_list, tbm_list, status_list, time_list)), 
                        columns=['id_list', 'dept_name', 'sub_name', 'name', 'tbm_result', 'status', 'created'])
    return df

def insert_data(data: dict):
    url = 'https://api.notion.com/v1/pages'
    payload = {"parent": {"database_id": DATABASE_ID}, "properties": data}
    res = requests.post(url, json=payload, headers=headers)
    print(f"response_status_code: {res.status_code}")
    return True


if __name__ == "__main__":

    dept_name = "판넬조립1부"
    sub_name = "판계1팀"
    name = "홍길동"
    tbm_result = '''
    동해물과 백두산이 마르고 닳도록
    하느님이 보우하사 우리나라 만세
    무궁화 삼천리 화려강산
    대한사람 대한으로 길이 보전하세   
    
    '''
    status = "False"

    data = {
        "name" : {"title": [{"text": {"content": name}}]},
        "sub_name": {"rich_text": [{"text": {"content": sub_name}}]},
        "name": {"rich_text": [{"text": {"content": name}}]},
        "tbm_result": {"rich_text": [{"text": {"content": tbm_result}}]},
        "status":  {"rich_text": [{"text": {"content": status}}]},
        }

    insert_data(data)
    
    target = get_pages()
    print(read_as_df(target))