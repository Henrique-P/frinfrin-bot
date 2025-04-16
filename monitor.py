from datetime import datetime, timezone
import json
def logRequest():
    try:
        file = open('./logs/log.json','r')
        tempFile = json.loads(file.read())
        file.close()
        tempFile.append(datetime.now().strftime("%d-%m-%Y-%H:%M:%S"))
        file = open('./logs/log.json','w')
        file.write(json.dumps(tempFile))
        file.close()
    except FileNotFoundError: 
        file = open('./logs/log.json','w')
        file.write(json.dumps([datetime.now().strftime("%d-%m-%Y-%H:%M:%S")]))
        file.close()
    except json.JSONDecodeError:
        file = open('./logs/log.json','w')
        file.write(json.dumps([datetime.now().strftime("%d-%m-%Y-%H:%M:%S")]))
        file.close()