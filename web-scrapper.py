""" This program was created by Luis Garcia Estrades """
import urllib2
import urllib
import sys
import re
import os


def Usage():
    print """
    Usage: python bot.py subject_1 subject_2
    Example: python bot.py AC FM SO XC M2 NOTEXISTS
    """

if len(sys.argv) == 1:
    Usage()

if "help" in sys.argv[1:] or "HELP" in sys.argv[1:]:
    print """
    This program downloads all the available exams for a certain subjects"""
    Usage()
    exit()

# we simulate acces through a browser
ua = "Mozilla/5.0 (compatible; Konqueror/3.5.8; Linux)"
# we define the headers
h = {"User-Agent": ua}
# we define the target url
urltocatch = 'http://dafib.upc.edu/llista-examens/'
# and then we prepare the request to send to the url
r = urllib2.Request(urltocatch, headers=h)
# we go to the url
dafib = urllib2.urlopen(r)
# we read it's content
html_dafib = dafib.read()
# this regex will catch the available subjects
rex1 = "<a href=\"(\w+)/\">\w+/</a>"
# we look for all the subjects available
m0 = re.findall(rex1, html_dafib)

# for each subject in the parameters
for subject in sys.argv[1:]:
    # we check if it's in the list of available subjects
    if subject in m0:
        try:
	    # then we create it's directory
            os.mkdir(subject)
            print "A new dir named: '" + subject + "' was created."

        except:
            # or catch the error if it already exists
            print "-A dir named: '" + subject + "' already exists"

        finally:
            files = os.listdir(subject)
            subject_url = urllib2.Request(urltocatch + subject, headers=h)
            exams_list = urllib2.urlopen(subject_url)
            subject_html = exams_list.read()
            download_files = "<a href=\"(Examen%20" + subject + ".+\.pdf)\">(Examen " + subject + ".+\.pdf)</a>"
            m2 = re.findall(download_files, subject_html)
            for element in m2:
                if not element[1] in files:
                    print "File: '" + element[1] + "' downloaded."
                    pdfs = open(subject + "/" + element[1], "w")
                    pdfs.close()
                    pdf = urllib.urlretrieve(urltocatch + subject + '/' + element[0], subject + "/" + element[1])
                else:
                    print "-The file '" + element[1] + "' already exists."
    else:
        print "The subject: '" + subject + "' were not found in the url."

dafib.close()
