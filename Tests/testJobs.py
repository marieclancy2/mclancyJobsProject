import marieclancyProject1

# Test to check if the retrieved list has more than 100 items.
def test_get_jobs():
    jobs = marieclancyProject1.get_jobs()
    assert len(jobs) > 100


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