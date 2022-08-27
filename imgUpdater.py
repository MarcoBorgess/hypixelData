from db import insertMany, select
import requests
import base64

def get_as_base64(url):
    request = requests.get(url)
    b64_encoded = base64.b64encode(request.content)
    if len(b64_encoded) > 10:
        print(f'✅ Icon found {url}')
        return b64_encoded
        
    print(f'⚠️ Icon not found {url}')
    return None

def get_icon64_values():
    db_items = select('SELECT id, iconURL FROM item where length(iconBase64) < 10;')
    
    updated_items = []
    
    def for_loop(items_to_update):
        for item in items_to_update:
            id = item[0]
            icon_url = item[1]
            
            converted_icon = get_as_base64(icon_url)     
            icon_base64 = converted_icon
            
            if icon_base64 is not None:
                print(f'✅ Icon added to list ({icon_url})')
                updated_item = (id, icon_base64)
                updated_items.append(updated_item)
            
    while updated_items.__len__() != db_items.__len__():
        filtered = list(filter(lambda x: x[0] not in [y[0] for y in updated_items], db_items))
        print(f'⚠️ {filtered.__len__()} items left to update')
        for_loop(filtered)
    
    print(f'✅ All items updated ({updated_items.__len__()} items)')
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
    print(f'✅ Inserting/updating table item... ({values.__len__()} items)')
    insertMany(insert_query, values)
        