import os, sys, getopt
import json
import requests
from bs4 import BeautifulSoup

def getProgramSched(url):
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")
    programName = soup.find('h1').string
    print(programName)
    print("–"*len(programName))

    schedTable = soup.find(id="schedule-table")

    if (schedTable is None):
        print("Not currently being offered.")
    else:
        schedTableBody = schedTable.tbody

        rows = schedTableBody.find_all('tr')

        for row in rows:
            data = row.find_all("td")

            date = data[0].string
            time = data[1].string
            court = data[2].a.string

            print("%s \t\t %s \t\t %s" % (date, time, court))   
        
    print()


if __name__ == "__main__":
    def usage():
        print ('Usage: ' + os.path.basename(__file__) + ' option')
        print ('Options:')
        print ('\t -h, --help')
        print ('\t -b, --badminton')
        print ('\t -p, --pickleball')
        print ('\t -r, --rock-climbing')
        sys.exit(2)

    try:
        opts, args = getopt.getopt(sys.argv[1:],"hbrp",["help", "badminton", "rock-climbing", "pickleball"])
    except getopt.GetoptError:
        usage()
    
    selected = []        

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
        elif opt in ("-b", "--badminton"):
            selected.append("badminton")
        elif opt in ("-p", "--pickleball"):
            selected.append("pickleball")
        elif opt in ("-r", "--rock-climbing"):
            selected.append("rock-climbing")
    
    if (len(selected) == 0):
        selected.append("badminton")    #badminton is default

    json_file = open(os.path.dirname(os.path.abspath(__file__)) + '/tpasc.json') 
    programs = json.load(json_file)

    for item in selected:
        for url in programs[item]:
            getProgramSched(url)