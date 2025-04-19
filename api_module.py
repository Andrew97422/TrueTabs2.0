import requests
import json

def get_api_key():
    # Чтение токена из файла
    with open('API_KEY.txt', 'r') as file:
        return file.read().strip()

def get_records(table_id, view_id, field_key="name"):
    url = f"https://true.tabs.sale/fusion/v1/datasheets/{table_id}/records"
    params = {
        'viewId': view_id,
        'fieldKey': field_key
    }
    headers = {
        'Authorization': f'Bearer {get_api_key()}'
    }
    response = requests.get(url, headers=headers, params=params)
    if response.ok:
        return response.json()
    else:
        raise Exception(f'Failed to get records: {response.status_code} {response.text}')

def post_records(table_id, records, view_id, field_key="name"):
    url = f"https://true.tabs.sale/fusion/v1/datasheets/{table_id}/records"
    params = {
        'viewId': view_id,
        'fieldKey': field_key
    }
    headers = {
        'Authorization': f'Bearer {get_api_key()}',
        'Content-Type': 'application/json'
    }
    data = {
        "records": records,
        "fieldKey": field_key
    }
    response = requests.post(url, headers=headers, params=params, data=json.dumps(data))
    if response.ok:
        return response.json()
    else:
        raise Exception(f'Failed to post records: {response.status_code} {response.text}')

def patch_records(table_id, records, view_id, field_key="name"):
    url = f"https://true.tabs.sale/fusion/v1/datasheets/{table_id}/records"
    params = {
        'viewId': view_id,
        'fieldKey': field_key
    }
    headers = {
        'Authorization': f'Bearer {get_api_key()}',
        'Content-Type': 'application/json'
    }
    data = {
        "records": records,
        "fieldKey": field_key
    }
    response = requests.patch(url, headers=headers, params=params, data=json.dumps(data))
    if response.ok:
        return response.json()
    else:
        raise Exception(f'Failed to patch records: {response.status_code} {response.text}')

def delete_records(table_id, record_ids):
    url = f"https://true.tabs.sale/fusion/v1/datasheets/{table_id}/records"
    params = [('recordIds', record_id) for record_id in record_ids]
    headers = {
        'Authorization': f'Bearer {get_api_key()}'
    }
    response = requests.delete(url, headers=headers, params=params)
    if response.ok:
        return response.json()
    else:
        raise Exception(f'Failed to delete records: {response.status_code} {response.text}')
