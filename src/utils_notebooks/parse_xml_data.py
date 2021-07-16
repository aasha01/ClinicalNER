# Python code to illustrate parsing of XML files
# importing the required modules
import csv
import requests
import xml.etree.ElementTree as ET
import os
import pandas as pd


def loadRSS():
    # url of rss feed
    url = 'http://www.hindustantimes.com/rss/topnews/rssfeed.xml'

    # creating HTTP response object from given url
    resp = requests.get(url)

    # saving the xml file
    with open('topnewsfeed.xml', 'wb') as f:
        f.write(resp.content)


# Parse and get the Report text - single node. No need to iterate
def parseXML(xmlfile):
    # create element tree object
    tree = ET.parse(xmlfile)

    # get root element
    root = tree.getroot()

    report = root.find('TEXT').text

    # return news items list
    return report


def savetoCSV(newsitems, filename):
    # specifying the fields for csv file
    fields = ['filename', 'report_text']

    # writing to csv file
    with open(filename, 'w') as csvfile:
        # creating a csv dict writer object
        writer = csv.DictWriter(csvfile, fieldnames=fields)

        # writing headers (field names)
        writer.writeheader()

        # writing data rows
        writer.writerows(newsitems)


def get_report_text(filename):
    # parse xml file
    report_text = parseXML(filename)

    # print(report_text)

    # store news items in a csv file
    # savetoCSV(newsitems, 'data.csv')

    return report_text


def get_report_from_xml_files(path):
    # create empty list for news items
    all_reports = []
    file_names = []

    # path = 'D:/Work/DataSets_NLP/n2c2_medical/ClinicalTrial/train/train/'
    for filename in os.listdir(path):
        if not filename.endswith('.xml'): continue
        fullname = os.path.join(path, filename)
        print(fullname)
        # append news dictionary to news items list
        all_reports.append(get_report_text(fullname))
        file_names.append(filename)

    out = pd.DataFrame([all_reports, file_names]).T
    out.rename(columns={0: 'filename', 1: 'report_text'})
    out.to_csv('data1.csv', header=['filename', 'report_text'], index=None)

    return all_reports


if __name__ == "__main__":
    path = 'D:/Work/DataSets_NLP/n2c2_medical/ClinicalTrial/train/train/'
    get_report_from_xml_files(path)
    # calling main function
    # tree = ET.parse('100.xml')

    # get root element
    # root = tree.getroot()
    # print(root.find('TEXT').text)
