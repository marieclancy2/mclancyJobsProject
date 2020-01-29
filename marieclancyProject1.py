import requests


rawData = requests.get("https://jobs.github.com/positions.json?page=1&search=code")
jsonData1 = rawData.json()

rawData = requests.get("https://jobs.github.com/positions.json?page=2&search=code")
jsonData2 = rawData.json()

rawData = requests.get("https://jobs.github.com/positions.json?page=3&search=code")
jsonData3 = rawData.json()

jsonTotalData = jsonData1 + jsonData2 + jsonData3

f = open("marieclancy.txt", "w")

print(len(jsonTotalData))
for data in jsonTotalData:
    print("\n")
    print(data)
    f.write(str(data) + '\n')

f.close()