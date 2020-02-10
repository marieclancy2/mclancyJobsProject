import marieclancyProject1


# Test to check if the retrieved list has more than 100 items.
def test_get_jobs():
    jobs = marieclancyProject1.get_jobs()
    assert len(jobs) > 100
    assert type(jobs[1]) == dict


def test_insert_to_database():
    jobs = marieclancyProject1.get_jobs()
    existingTitle = "Web Full Stack Engineer"
    conn, cursor = marieclancyProject1.open_db("test.sqlite")
    marieclancyProject1.setup_db(cursor, conn)
    for job in jobs:
        marieclancyProject1.insert_to_database(cursor, conn, job)
    cursor.execute("SELECT * FROM jobs WHERE jobs.title = ?", (existingTitle,))
    assert cursor.fetchone()
    marieclancyProject1.close_db(conn)


# Test to check if the function actually writes a file with the correct data.
def test_write_file():
    jobs = marieclancyProject1.get_jobs()
    marieclancyProject1.write_file(jobs)
    titleToExist = "Web Full Stack Engineer"
    match = False
    with open('jobs.txt', 'r') as fileOpen:
        for line in fileOpen.readlines():
            if titleToExist in line:
                match = True
                break
    assert match


def test_send_extra_data():
    conn, cursor = marieclancyProject1.open_db("test.sqlite")
    marieclancyProject1.setup_db(cursor, conn)
    extraGoodData = {
        "id": "781", "type": "yes", "url": "ok.com", 'company': 'google',
        'company_url': 'ok.com123',
        'created_at': "March 1, 2019", 'location': "USA", 'title': 'senior designer',
        'description': "professional developer needed",
        'how_to_apply': "please visit website", 'company_logo': "none"}
    marieclancyProject1.insert_to_database(cursor, conn, extraGoodData)
    existingID = "781"
    cursor.execute("SELECT * FROM jobs WHERE jobs.id = ?", (existingID,))
    assert cursor.fetchone()

    # same as above but with fewer arguments
    extraBadData = {
        "id": "782", "type": "yes", "url": "ok.com", 'company': 'google',
        'title': 'senior designer',
        'description': "professional developer needed",
        'how_to_apply': "please visit website", 'company_logo': "none"}

    nonExistingID = 782
    marieclancyProject1.insert_to_database(cursor, conn, extraBadData)
    cursor.execute("SELECT * FROM jobs WHERE jobs.id = ?", (nonExistingID,))
    assert cursor.fetchone() is None

    marieclancyProject1.close_db(conn)

