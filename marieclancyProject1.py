import requests, time, json


# Main function that retrieves the jobs and writes them to a file.
def main():
    jobs = get_jobs()
    write_file(jobs)


# Function that retrives the jobs.
def get_jobs():
    url = "https://jobs.github.com/positions.json?page="
    totalJSON = []
    for counter in range(1,6):
        totalJSON += requests.get(url + str(counter)).json()
        time.sleep(2)
    return totalJSON


# Function that writes the data to a file.
def write_file(data):
    with open('jobs.txt', 'w') as openFile:
        for job in data:
            json.dump(job, openFile)


if __name__ == '__main__':
    main()