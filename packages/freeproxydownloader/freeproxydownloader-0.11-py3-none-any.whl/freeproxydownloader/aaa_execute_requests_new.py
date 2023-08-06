import argparse
import os

import re

import sys

from time import time, sleep

import kthread
import requests
import regex
from PrettyColorPrinter import pdp

pythonpath = sys.executable
import pandas as pd


"""            resultdict = {
                proxy: {'proxy':proxy,'timeout': timeout,
                        'save_content':None,
                        'save_errors':None,
                        'proxyfunction': proxyfunction,
                        'header' :header

                }
            }"""

resultsdict = {}
workingproxies = 0
checkedproxies = 0


def regex_path_splitter(path):
    return regex.split(r"[\\/]+", path)


def regex_dot_splitter(path):
    return regex.split(r"[.]+", path)


def regex_get_filename_with_extension(path):
    return regex_path_splitter(path)[-1]


def regex_get_filename_without_extension(path):
    return regex_dot_splitter(path=regex_path_splitter(path)[-1])[0]


def make_folder_for_excel_and_pkl(saveproxydataframexlsx, saveproxydataframepkl):
    saveproxydataframexlsxfolder = f"{os.sep}".join(
        regex_path_splitter(saveproxydataframexlsx)[:-1]
    )
    saveproxydataframepklfolder = f"{os.sep}".join(
        regex_path_splitter(saveproxydataframepkl[:-1])
    )
    if not os.path.exists(saveproxydataframexlsxfolder):
        os.makedirs(saveproxydataframexlsxfolder)
    if not os.path.exists(saveproxydataframepklfolder):
        os.makedirs(saveproxydataframepklfolder)
    return saveproxydataframexlsxfolder, saveproxydataframepklfolder


def get_filepath_for_xlsx_and_pkl(save_proxy_dataframe):
    regex_fuer_pickle = regex.compile(r"\.(?:(?:pkl)|(?:xlsx))$")
    saveproxydataframexlsx = regex_fuer_pickle.sub("", save_proxy_dataframe) + ".xlsx"
    saveproxydataframepkl = regex_fuer_pickle.sub("", save_proxy_dataframe) + ".pkl"

    return saveproxydataframexlsx, saveproxydataframepkl


def read_proxies_xlsx(excelpath):
    df = pd.read_excel(excelpath)
    df = df.drop(columns=[x for x in df.columns if ":" in x]).copy()
    if "aa_fake_header" in df.columns:
        df = df.assign(aa_fake_header=lambda x_: x_.aa_fake_header.apply(eval))
    if "aa_proxyDict" in df.columns:
        df = df.assign(aa_proxyDict=lambda x__: x__.aa_proxyDict.apply(eval)).copy()
    return df


def download_with_requests(key, item):
    global resultsdict
    global workingproxies
    global checkedproxies
    checkedproxies = checkedproxies + 1
    response = None
    try:
        response = requests.get(
            url=item.aa_downloadlink,
            headers=item.aa_fake_header,
            timeout=item.aa_timeout,
            proxies=item.aa_proxyDict,
        )
    except Exception as Fehler:
        pass
        # print(Fehler)
        try:
            response.close()
        except Exception as Fehler2:
            pass
            # print(Fehler2)
    if response is not None:
        if response.status_code == 200:
            try:
                response_wiki = None
                webcheckproxy_url_check = re.sub(
                    fr"^{webcheckproxy_start}", item.aa_howtoconnect, webcheckproxy_url
                )
                try:
                    response_wiki = requests.get(
                        url=webcheckproxy_url_check,
                        timeout=item.aa_timeout,
                        headers=item.aa_fake_header,
                        proxies=item.aa_proxyDict,
                    )
                except Exception as fe:
                    pass
                    # print(fe)
                if response_wiki is not None:
                    res_ = str(response.text).strip()
                    if myipaddressregex.search(res_) is None:
                        if ipaddressformat_regex.search(res_) is not None:
                            if (
                                webcheckproxy_regex.search(
                                    str(response_wiki.text)
                                    .replace("\n", " ")
                                    .replace("\r", " ")
                                )
                                is not None
                            ):
                                pdp(item.to_frame())
                                resultsdict[key] = {
                                    "aa_item": item.copy(),
                                    "aa_response_ip": response,
                                    "aa_response_wiki": response_wiki,
                                }
                                workingproxies = workingproxies + 1
                                print(
                                    f"Working Proxies: {workingproxies} / {checkedproxies}"
                                )
            except Exception as Fehler:
                pass
                # print(Fehler)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PROXY DOWNLOAD")
    parser.add_argument(
        "-p", "--proxy_xlsx", type=str, help=f'Input for proxy text (xlsx)"""',
    )
    parser.add_argument(
        "-t", "--timeout", type=int, default=30, help=f'Timeout for each connection"""',
    )

    parser.add_argument(
        "-l",
        "--thread_limit",
        type=int,
        default=200,
        help=f'Thread limit for requests"""',
    )

    parser.add_argument(
        "-s",
        "--save_proxy_dataframe",
        type=str,
        help=f'File to save dataframe, ending pkl / xlsx!"""',
    )

    parser.add_argument(
        "-w",
        "--webcheckproxy_url",
        type=str,
        default="https://wikipedia.org",
        help=f'url for second connection check"""',
    )
    parser.add_argument(
        "-r",
        "--webcheckproxy_regex",
        type=str,
        default=r"Wikimedia\s+Foundation",
        help=f'url for second connection check"""',
    )
    args = parser.parse_args()

    proxies = args.proxy_xlsx
    timeout = args.timeout
    threadlimit = args.thread_limit
    webcheckproxy_url = args.webcheckproxy_url
    webcheckproxy_regex = args.webcheckproxy_regex
    save_proxy_dataframe = args.save_proxy_dataframe
    df = read_proxies_xlsx(proxies)
    timeouts = [timeout] * len(df)

    ipcheckeraddress = df.aa_downloadlink_original.iloc[0]

    webcheckproxy_regex = regex.compile(webcheckproxy_regex, flags=regex.IGNORECASE)
    webcheckproxy_start = re.search(
        r"^https?", webcheckproxy_url, flags=re.IGNORECASE
    ).group()
    myipaddress = requests.get(ipcheckeraddress).text
    myipaddressregex = regex.compile(rf"^{regex.escape(myipaddress.strip())}$")
    ipaddressformat_regex = regex.compile(
        r"^((?:\d{1,3})\.(?:\d{1,3})\.(?:\d{1,3})\.(?:\d{1,3}))$"
    )
    df["aa_timeout"] = timeouts
    tdict = {}
    for key, item in df.iterrows():
        tdict[key] = kthread.KThread(
            target=download_with_requests, name=key, args=(key, item),
        )

    activethreads = []
    maxthreads = threadlimit
    timeoutafterfinish = timeout
    for key, item in tdict.items():
        item.start()
        # sleep(.0001)
        activethreads.append(item)
        take_a_break = True
        while take_a_break:

            # sleep(.0001)
            breakcheck = [x for x in activethreads if x.is_alive()]
            threadsactive = len(breakcheck)
            threadsfinished = len(activethreads) - threadsactive
            # print(f'Threads active: {threadsactive} / Threads finished: {threadsfinished}')
            if threadsactive < maxthreads:
                take_a_break = False

    finaltimeout = time() + timeout
    while finaltimeout > time() and len([x for x in activethreads if x.is_alive()]) > 0:
        sleep(0.05)

    anyalive = [x for x in activethreads if x.is_alive()]
    if any(anyalive):
        for thr in anyalive:
            try:
                thr.kill()
            except Exception as Fehler:
                print(Fehler)
                continue

    df = pd.concat(
        [resultsdict[x]["aa_item"].to_frame() for x in resultsdict.keys()],
        axis=1,
        ignore_index=True,
    ).T.copy()

    saveproxydataframexlsx, saveproxydataframepkl = get_filepath_for_xlsx_and_pkl(
        save_proxy_dataframe
    )
    make_folder_for_excel_and_pkl(saveproxydataframexlsx, saveproxydataframepkl)
    df.to_excel(saveproxydataframexlsx)
    df.to_pickle(saveproxydataframepkl)
    print("\n")
    print((f"Filtered list with proxies: {saveproxydataframexlsx}"))
    print((f"Filtered list with proxies: {saveproxydataframepkl}"))
