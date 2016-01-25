# -*- coding: utf-8 -*-

# std import
import os
import re
import ftplib
import xml.etree.ElementTree as ET

# pip import
import requests
from fief import filter_effective_parameters as fief

# project import

@fief
def study2reads_number(accession_number, ena_base):
    """ Is a generator of read accession number related to study """

    #because ena is stupid
    study_url = ena_base + accession_number + "&display=xml"

    r = requests.get(study_url)

    r.raise_for_status()

    xml_root = ET.fromstring(r.text)

    read_acc = ""
    for xref in xml_root.findall("STUDY/STUDY_LINKS/STUDY_LINK/"):
        if list(xref)[0].text == "ENA-RUN":
            read_acc += "," + list(xref)[1].text

    return read_acc

@fief
def reads(accession_number, output, interactive, verbose, ena_base, ftp_adresse,
          ftp_dir):
    """ Write reads file with output as prefix """

    ftp = ftplib.FTP(ftp_adresse)
    ftp.login("anonymous", "anonymous")

    for read_acc in __read_acc_str2gen(
            study2reads_number(accession_number, ena_base)):

        ftp_read_path = __read_acc2path(read_acc)
        for read_name in ftp.nlst(ftp_dir + ftp_read_path):
            print(read_name)
            with open(output+os.path.basename(read_name), 'wb') as outfile:
                ftp.retrbinary('RETR ' + read_name, outfile.write)

    ftp.close()

def __read_acc_str2gen(read_acc_str):
    """ take XXX1011-XXX1021,XXX2030-XXX2049 and yield intermediate value """

    get_numb = re.compile(r"([^\d]+)(\d+)-[^\d]+(\d+)")

    for sub_read_acc in read_acc_str.split(",")[1:]:

        match = get_numb.search(sub_read_acc)
        if match:
            (prefix, first, second) = match.groups()

            for index in range(int(first), int(second)):
                yield prefix + str(index)

def __read_acc2path(read_acc):
    """ Generate the url of reads """

    get_numb = re.compile(r"[^\d]+(\d+)")
    number = get_numb.search(read_acc).group(1)

    if len(number) == 6:
        return read_acc[:6] + "/" + read_acc + "/"
    elif len(number) == 7:
        return read_acc[:6] + "/00" + read_acc[-1] + "/" + read_acc + "/"
    elif len(number) == 8:
        return read_acc[:6] + "/0" + read_acc[-2:-1] + "/" + read_acc + "/"
    elif len(number) == 9:
        return read_acc[:6] + "/" + read_acc[-3:-1] + "/" + read_acc + "/"
    else:
        raise AttributeError(read_acc + " isn't a valid read_acc")
