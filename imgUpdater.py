from db import insertMany, select
import requests
import base64

def get_as_base64(url):
    response = requests.get(url)
    headers = response.headers
    if headers['Content-Type'] == 'image/png':
        b64_encoded = base64.b64encode(response.content)
        print(f'✅ Icon found {url}')
        return b64_encoded
        
    print(f'⚠️ Icon not found {url}')
    return None

def get_icon64_values():
    db_items = select('SELECT id, iconURL FROM item WHERE length(iconBase64) < 10 OR iconBase64 IS NULL')
    
    updated_items = []
    
    for item in db_items:
        id = item[0]
        icon_url = item[1]
        
        icon_base64 = get_as_base64(icon_url)     
        
        if icon_base64 is not None:
            updated_item = (id, icon_base64)
            updated_items.append(updated_item)
    
    print(f'✅ Updated icon from {updated_items.__len__()} items')
    return updated_items
        
def update_icon64_column():
    values = get_icon64_values()

    if not values:
        print('⚠️ get_icon64_values returned nothing')
        return
    
    insert_query = """
                        INSERT INTO item (id, iconBase64) 
                        VALUES (%s, %s) 
                        ON DUPLICATE KEY UPDATE
                        id = VALUES(id),
                        iconBase64 = VALUES(iconBase64)
                    """       
    print(f'✅ Inserting/updating table item...')
    insertMany(insert_query, values)
        