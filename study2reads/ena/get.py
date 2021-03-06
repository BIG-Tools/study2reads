# -*- coding: utf-8 -*-

"""
Read study information and download reads
"""

# std import
import re
import xml.etree.ElementTree as ET

# pip import
import ftputil
from progressbar import ProgressBar, Percentage, Bar, ETA
from fief import filter_effective_parameters as fief
import requests

# project import


@fief
def reads(accession_number, output, interactive=False, verbose=False,
          ena_base="http://www.ebi.ac.uk/ena/data/view",
          ftp_address="ftp.sra.ebi.ac.uk", ftp_dir="vol1/fastq/"):
    """ Write reads file with output as prefix """

    with ftputil.FTPHost(ftp_address, "anonymous", "anonymous") as host:
        for read_acc in __read_acc_str2gen(
                study2reads_number(accession_number, ena_base)):
            ftp_read_path = __read_acc2path(read_acc)
            for read_name in host.listdir(ftp_dir+ftp_read_path):
                if __dl_file(read_name, interactive):
                    if verbose:
                        file_size = host.path.getsize(ftp_dir + ftp_read_path +
                                                      read_name)
                        pbar = _ProgressBar(widgets=[read_name, ":",
                                                     Percentage(),
                                                     Bar(), ETA()],
                                            maxval=file_size).start()
                        host.download(ftp_dir + ftp_read_path + read_name,
                                      output + read_name,
                                      callback=pbar.update)
                        pbar.finish()
                    else:
                        host.download(ftp_dir + ftp_read_path + read_name,
                                      output + read_name)


@fief
def study2reads_number(accession_number, ena_base):
    """ Is a generator of read accession number related to study """

    # because ena is stupid
    study_url = ena_base + accession_number + "&display=xml"

    req_ret = requests.get(study_url)

    req_ret.raise_for_status()

    xml_root = ET.fromstring(req_ret.text)

    read_acc = list()
    for xref in xml_root.findall("STUDY/STUDY_LINKS/STUDY_LINK/"):
        if list(xref)[0].text == "ENA-RUN":
            read_acc.append(list(xref)[1].text)

    return ",".join(read_acc)


def __read_acc_str2gen(read_acc_str):
    """ take XXX1011-XXX1021,XXX2030-XXX2049 and yield intermediate value """

    # take prefix, numeric part and ponctuation
    cut = re.compile(r"([^-,\d]+)(\d+)([-,]?)")

    # add false value to the end for remove some side effect
    all_match = cut.findall(read_acc_str + ',')
    all_match.append(['', '', ''])

    if len(all_match) <= 1:  # if you don't understand tha your are stupid
        yield all_match[0][:2]

    # read element by 2-mer
    for ((prefix, first, sep), (_, last, _)) in [all_match[i:i+2] for i in
                                                 range(len(all_match) - 1)]:
        if sep == ',':
            # no successor we yield it
            yield prefix + first

        if sep == '-':
            # begin of series
            len_number = len(first)  # take size of suffix

            # loop on begin to end - 1 (end is yield on next general loop)
            for index in range(int(first), int(last)):
                index = str(index)
                # element is prefix + some 0 to complete the length of
                # numeric part + the numeric part
                yield prefix + '0'*(len_number-len(index)) + index


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


def __dl_file(read_name, interactive):
    """ Answer to user for dl read or not """
    if interactive:
        answer = input("download "+read_name+" (Y/n) : ")
        return answer.startswith("y")
    else:
        return True


class _ProgressBar(ProgressBar):
    """ Derivation of ProgressBar for save actual value """

    def __init__(self, **arg):
        self.__val = 0
        super().__init__(**arg)

    def start(self):
        self.__val = 0
        return super().start()

    def update(self, val=None):
        if isinstance(val, bytes):
            self.__val += len(val)

        return super().update(self.__val)
