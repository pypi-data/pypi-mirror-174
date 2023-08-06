#!/usr/bin/env python

import sys
import requests
import os
from bs4 import BeautifulSoup as bs


def main():
    class styles:
        red = '\033[31m'
        green = '\033[32m'
        yellow = "\033[33m"
        white = "\u001b[37m"
        cyan = "\u001b[36m"

    args = sys.argv
    home = os.getenv('HOME')

    # Checks if .archimedean file already exists or not
    if len(args) == 1:
        print("\nHere are a list of commands:")
        print("\tarchimedean login -> logs into Archie")
        exit()

    # Saves login to local file
    if args[1] == "login":
        print()
        username = input("Enter Archie's username: ")
        password = input("Enter Archie's password: ")

        if not os.path.isdir(os.path.join(home, '.archimedean')):
            os.makedirs(os.path.join(home, '.archimedean'))

        creds = open(os.path.join(home, '.archimedean', 'creds.txt'), 'w+')
        creds.write(f"{username}\n")
        creds.write(password)
        print("\nSaved credentials. You can now login to Archie.\n")

    if args[1] == "check_homework":
        if not os.path.isfile(os.path.join(home, '.archimedean', 'creds.txt')):
            print(styles.red + "\nRun 'archimedean login' first to save your credentials.\n")
            exit()

        creds = open(os.path.join(home, '.archimedean', 'creds.txt'), 'r')
        creds = creds.read().split()
        usr = creds[0]
        pswd = creds[1]

        login_data = {"login_name": usr,
                      "passwd": pswd, "submit": "Login"}

        url = "https://sis.archimedean.org/sis/default.php"

        with requests.Session() as s:
            r = s.post(url, data=login_data)
            soup = bs(r.content, 'html.parser')
            # print(soup.prettify())
            hw_url = "https://sis.archimedean.org/sis/course_wall.php"
            r = s.get(hw_url)
            soup = bs(r.content, 'html.parser')

        html_hw_lst = soup.findAll('td', nowrap='nowrap')
        html_duedate_lst = soup.findAll('td', nowrap='nowrap')
        html_teacher_lst = soup.findAll('td', nowrap='nowrap')
        duedate_lst_unf = []
        hw_lst = []
        teacher_lst = []
        duedate_lst = []

        for duedate in html_duedate_lst:
            duedate.findNext('td')
            duedate = duedate.findNext('td')
            duedate = duedate.findNext('td')
            duedate = duedate.findNext('td')
            duedate_lst_unf.append(duedate.get_text())

        for date_f in duedate_lst_unf:
            date_f = date_f.split("-")
            duedate_lst.append(str(date_f[1]) + "/" +
                               str(date_f[2] + "/" + str(date_f[0])))

        for hw in html_hw_lst:
            hw_lst.append(hw.get_text())

        for teacher in html_teacher_lst:
            teacher = teacher.findNext('td')
            teacher = teacher.findNext('td')
            teacher = teacher.findNext('td')
            teacher = teacher.findNext('td')
            teacher = teacher.findNext('td')
            teacher_lst.append(teacher.get_text())

        i = 0
        print(styles.cyan)
        for hw in hw_lst:
            print(f"{hw} due on {duedate_lst[i]} for {teacher_lst[i]}")
            i += 1

        print()


main()
