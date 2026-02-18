import json

with open("C:/Users/арсен/Desktop/KBTU/PP2_2026/lab4/sample-data.json") as file:
    data = json.load(file)

print("Interface Status")
print("=" * 80)
print("DN                                               Description           Speed    MTU")
print("-" * 50)

for item in data['imdata']:
    attributes = item['l1PhysIf']['attributes']
    dn = attributes['dn']
    description = attributes.get('descr', '')  
    speed = attributes['speed']
    mtu = attributes['mtu']
    
    print(f"{dn:<50} {description:<20} {speed:<6} {mtu}")