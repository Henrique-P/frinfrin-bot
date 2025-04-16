from datetime import datetime
import json

def logRequest():
    try:
        # Open the file in read mode using 'with'
        with open('./logs/log.json', 'r') as file:
            tempFile = json.loads(file.read())
        
        # Append the new timestamp
        tempFile.append(datetime.now().strftime("%d-%m-%Y-%H:%M:%S"))
        
        # Open the file in write mode using 'with'
        with open('./logs/log.json', 'w') as file:
            file.write(json.dumps(tempFile))
    
    except FileNotFoundError:
        # Create the file and write the timestamp if it doesn't exist
        with open('./logs/log.json', 'w') as file:
            file.write(json.dumps([datetime.now().strftime("%d-%m-%Y-%H:%M:%S")]))
    
    except json.JSONDecodeError:
        # Overwrite the file with a new array if JSON is invalid
        with open('./logs/log.json', 'w') as file:
            file.write(json.dumps([datetime.now().strftime("%d-%m-%Y-%H:%M:%S")]))