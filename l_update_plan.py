# Create a systematic L-field update plan
import json

# Load the L-transfer mapping
l_transfer_updates = {
    '34.03': '2',        # Done
    '115.2': '2',        # Done  
    '117.4': '2',        # Done
    '231.25': '1,2',     # Done
    '362.8': '1,2',      # Need to update
    '422.3': '2',        # Need to update
    '463.9': '1,2',      # Need to update
    '698.2': '1,2',      # Need to update
    '1064.4': '2',       # Need to update
    '1086.7': '2',       # Need to update
    '1123.0': '2',       # Need to update
    '1124.5': '2',       # Need to update
    '1192.2': '2',       # Need to update
    '1279.4': '2',       # Need to update
    '1295.5': '2',       # Need to update
    '1351.4': '2',       # Need to update
    '1390.1': '2',       # Need to update
    '1449.6': '2',       # Need to update
    '1462.9': '2',       # Need to update
    '1475.5': '2',       # Need to update
}

# Also need to clear L fields for entries that should be blank
blank_entries = [
    '118.30', '162.1', '239.0', '255.5', '261.5', '275.3', '298.70', 
    '313.0', '317.51', '355.41', '368.7', '372.1', '372.8', '379.0', 
    '382.8', '396.14', '431.2', '435.4', '438.35', '443.45', '456.4', 
    '461.01', '469.85', '490.5', '510.02', '523.8', '573.0', '636.5', 
    '641.93', '682.7', '689.7', '713.0', '767.3', '786.5', '798.65',
    '813.8', '836.27', '850.94', '893.17', '902.0', '921.5', '930.0',
    '935.78', '941.0', '976.4', '982.0', '997.9', '1017.7', '1140.0',
    '1237.0', '1261.8', '1275.1', '1308.2', '1314.5', '1325.7', 
    '1388.0', '1447.2'
]

print('Updates needed:')
print('SET TO SPECIFIC VALUES:')
for energy, value in l_transfer_updates.items():
    print(f'{energy}: -> "{value}"')

print('\\nSET TO BLANK:')
for energy in blank_entries:
    print(f'{energy}: -> (blank)')
