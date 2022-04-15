import json
import requests
import time
import hashlib
import pygsheets
import pandas as pd

contestId = 369610  #add contest id here , it can be foun
apiKey = "" # add Api key and secret that can be found in your account and don't share them with anyone
secret = ""
time = int(time.time())
rand = "123456"
route = f"/contest.status?apiKey={apiKey}&contestId={contestId}&time={time}"
apiSigRaw = f"{rand}{route}#{secret}"
apiSig = hashlib.sha512(bytes(apiSigRaw, 'utf-8')).hexdigest()
submissions_url = f"https://codeforces.com/api{route}&apiSig={rand}{apiSig}"

response = requests.get(submissions_url)
resJson = response.json()

with open('output.json', 'w') as outputFile:
    json.dump(resJson, outputFile, indent=4)

# print(response.status_code)

df = pd.DataFrame(columns=["handle", "problemName", "spotId"])
# check sorted based on eh el submission time
for i, submission in enumerate(resJson['result'][::-1]):
    if submission['author']['participantType'] == 'CONTESTANT' and submission['verdict'] == 'OK' and \
            submission['author'][
                'ghost'] == False:
        df.loc[i] = [submission['author']['members'][0]['handle'], submission['problem']['index'], 0]

print(df)

