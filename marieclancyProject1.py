import requests
import feedparser
import time
import json
import sqlite3
from typing import Tuple
import ssl


def get_data_from_stackoverflow():
    ssl._create_default_https_context = ssl._create_unverified_context
    feedParse = feedparser.parse('https://stackoverflow.com/jobs/feed')
    jobEntries = feedParse["entries"]

    allJobs = []
    currentDict = {}
    for job in jobEntries:
        currentDict["id"] = job["id"]
        currentDict["type"] = None
        currentDict["url"] = job["link"]
        currentDict["created_at"] = None
        currentDict["company"] = job["author"]
        currentDict["company_url"] = None
        currentDict["title"] = job["title"]
        currentDict["description"] = job["summary"]
        currentDict["how_to_apply"] = None
        currentDict["company_logo"] = None

        try:
            currentDict["location"] = job["location"]
        except KeyError:
            currentDict["location"] = None

        allJobs.append(currentDict)
        currentDict = {}

    return allJobs


# function to open a database
def open_db(filename: str) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    db_connection = sqlite3.connect(filename)  # connect to existing DB or create new one
    cursor = db_connection.cursor()  # get ready to read/write data
    return db_connection, cursor


# Function to close a database
def close_db(connection: sqlite3.Connection):
    connection.commit()  # make sure any changes get saved
    connection.close()


# Function to commit to database
def commit_db(connection: sqlite3.Connection):
    connection.commit()


# Main function that retrieves the jobs and writes them to a file.
def main():
    jobs = get_jobs()
    jobs2 = get_data_from_stackoverflow()
    write_file(jobs)
    conn, cursor = open_db("jobs.sqlite")
    setup_db(cursor, conn)
    conn.commit()
    for job in jobs:
        insert_to_database(cursor, conn, job)
    for job in jobs2:
        print(job)
        insert_to_database(cursor, conn, job)
    close_db(conn)


# Function that creates the table jobs
def setup_db(cursor: sqlite3.Cursor, connection: sqlite3.Connection):
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS jobs( 
    id TEXT PRIMARY KEY,
    type TEXT,
    url TEXT NOT NULL,
    company TEXT,
    company_url TEXT,
    created_at TEXT,
    location TEXT,
    title TEXT,
    description TEXT NOT NULL,
    how_to_apply TEXT,
    company_logo TEXT
    );''')
    connection.commit()


def insert_to_database(cursor: sqlite3.Cursor, connection: sqlite3.Connection, data: dict):
    if len(data) != 11:
        return
    try:
        cursor.execute(f'''
        INSERT INTO jobs (id, type, url, company, company_url, created_at, location, title, description,
        how_to_apply, company_logo)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);''',
                       (data['id'], data['type'], data['url'], data['company'], data['company_url'],
                        data['created_at'], data['location'], data['title'], data['description'],
                        data['how_to_apply'], data['company_logo'],))
    except sqlite3.IntegrityError:
        pass

    connection.commit()


# Function that retrieves the jobs.
def get_jobs():
    """retrieve github jobs data in form of a list of dictionaries after json processing"""
    all_data = []
    page = 1
    more_data = True
    while more_data:
        url = f"https://jobs.github.com/positions.json?page={page}"
        raw_data = requests.get(url)
        if "GitHubber!" in raw_data:  # sometimes if I ask for pages too quickly I get an error; only happens in testing
            continue  # trying continue, but might want break
        partial_jobs_list = raw_data.json()
        all_data.extend(partial_jobs_list)
        if len(partial_jobs_list) < 50:
            more_data = False
        time.sleep(.1)  # short sleep between requests so I dont wear out my welcome.
        page += 1
    return all_data


# Function that writes the data to a file.
def write_file(data):
    with open('jobs.txt', 'w') as openFile:
        for job in data:
            json.dump(job, openFile)


if __name__ == '__main__':
    main()
