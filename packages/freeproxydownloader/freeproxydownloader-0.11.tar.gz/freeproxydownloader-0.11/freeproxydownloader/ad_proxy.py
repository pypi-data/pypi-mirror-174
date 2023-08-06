import argparse
import os
from random import randrange
from time import sleep, strftime

import regex
import requests
import pandas as pd
import ujson
from fake_headers import Headers
from flatten_everything import flatten_everything
from downloader_cpr import ClearPrinter


def get_random_time(start, end):
    return randrange(int(start * 1000), int(end * 1000)) / 1000


def get_json_dict(x):
    clearp = ClearPrinter(softwrap=100, lines=120)
    try:
        return ujson.loads(x)
    except Exception as Fe:
        clearp.c_red(str(Fe))


def get_fake_header(debug=True):
    clearp = ClearPrinter(softwrap=100, lines=120)

    header = Headers(headers=False).generate()
    agent = header["User-Agent"]

    headers = {
        "User-Agent": f"{agent}",
    }
    if debug:
        clearp.c_orange(headers)
    return headers


def regex_path_splitter(path):
    return regex.split(r"[\\/]+", path)


def regex_dot_splitter(path):
    return regex.split(r"[.]+", path)


def regex_get_filename_with_extension(path):
    return regex_path_splitter(path)[-1]


def regex_get_filename_without_extension(path):
    return regex_dot_splitter(path=regex_path_splitter(path)[-1])[0]


clearp = ClearPrinter(softwrap=100, lines=120)


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


def get_timestamp():
    return strftime("%Y_%m_%d_%H_%M_%S")


def openfile_andstrip(path):
    with open(path, mode="r", encoding="utf-8") as f:
        data = [x.strip() for x in f.readlines() if len(x.strip()) > 9 and "//" in x]
    return data


def get_filepath_for_xlsx_and_pkl(save_proxy_dataframe):
    regex_fuer_pickle = regex.compile(r"\.(?:(?:pkl)|(?:xlsx))$")
    saveproxydataframexlsx = regex_fuer_pickle.sub("", save_proxy_dataframe) + ".xlsx"
    saveproxydataframepkl = regex_fuer_pickle.sub("", save_proxy_dataframe) + ".pkl"

    return saveproxydataframexlsx, saveproxydataframepkl


def get_proxys_from_json(webaddress, header=None, debug=False):

    if not os.path.exists(webaddress):
        if header is None:
            dada2 = requests.get(webaddress)
        else:
            dada2 = requests.get(webaddress, headers=header)
        if dada2.status_code != 200:
            if debug:
                clearp.c_red(f"{webaddress=}  {dada2.status_code=}")
            return ""
        if debug:
            clearp.c_lightgreen(f"{webaddress=}  {dada2.status_code=}")

        dada2 = dada2.content.decode("utf-8", "ignore")
    else:
        with open(webaddress, encoding="utf-8") as f:
            dada2 = f.read()
    convertedjson = [
        get_json_dict(x)
        for x in regex.split(
            r"(?:(?:[\n]+)|(?<=\})\s*,\s*(?=\{))",
            dada2.replace("\n", " ").replace("\r", " ").strip("[]"),
        )
    ]

    convertedjson = [x for x in convertedjson if x is not None]
    convertedjson1 = (
        pd.DataFrame.from_records(convertedjson).dropna().reset_index(drop=True)
    )
    convertedjson1.columns = [str(x).lower().strip() for x in convertedjson1.columns]
    for col in convertedjson1.columns:
        convertedjson1[col] = convertedjson1[col].astype("string")
    keydict = {}
    itisover = False
    returnvalue = ""
    for key, item in convertedjson1[:1].iterrows():
        if itisover:
            break
        for row in convertedjson1.columns:
            search = item[row]
            try:
                anything = regex.findall(
                    r"^\s*((?:\d{1,3})\.(?:\d{1,3})\.(?:\d{1,3})\.(?:\d{1,3})(:\d{1,3})?)\s*$",
                    f"{search}".strip(),
                )
                if any(anything):
                    if not ":" in (anything[0][1]):
                        keydict["aa_ip"] = row
                        for x in convertedjson1.columns.to_list():
                            regsuche = any(regex.findall(r"port", x))
                            if regsuche and row != x:
                                keydict["aa_port"] = x
                                break

                    elif ":" in (anything[0][1]):
                        keydict["aa_ip"] = row
                        keydict["aa_port"] = row
                if len(keydict) == 2:
                    itisover = True
                    if debug:
                        clearp.c_lightgreen(f"{keydict=}")

                    break
            except Exception as Fe:
                clearp.pri(Fe)
    formateddataframe = convertedjson1.drop(
        columns=[
            x
            for x in convertedjson1.columns.to_list()
            if x not in [keydict["aa_ip"], keydict["aa_port"]]
        ]
    )
    if keydict["aa_ip"] == keydict["aa_port"]:
        returnvalue = "\n".join(formateddataframe[keydict["aa_ip"]].to_list())
    elif keydict["aa_ip"] != keydict["aa_port"]:
        formateddataframe["newt"] = (
            formateddataframe[keydict["aa_ip"]]
            + ":"
            + formateddataframe[keydict["aa_port"]]
        )
        returnvalue = "\n".join(formateddataframe["newt"])

    return returnvalue  # ,formateddataframe


class GetProxiesGIT:
    def __init__(self, debug=True):
        self.debug = debug
        self.proxies = []
        self.fakeheader = get_fake_header(debug=debug)
        self.proxydf = pd.DataFrame()

    def load_txt_proxys(self, proxylist=None, sleeptime=(0.1, 0.7)):
        if proxylist is None:
            return self
        proxylist = list(dict.fromkeys(proxylist))

        for p in proxylist:
            try:
                if os.path.exists(p):
                    with open(p, encoding="utf-8") as f:
                        item = f.read()
                else:
                    filedownload = requests.get(p)
                    status = filedownload.status_code
                    if status != 200:
                        if self.debug:
                            clearp.c_red(f"{p} -> {status=}")
                        continue

                    if self.debug:
                        clearp.c_lightgreen(f"{p} -> {status=}")
                    item = filedownload.content.decode("utf-8", "ignore")
                self.proxies.append(item)
                try:
                    downloadedproxies = []
                    proxylistwithport = []

                    siteproxies = item.replace("\n", " ").replace("\r", " ")
                    anything = regex.findall(
                        r"\s*((?:\d{1,3})\.(?:\d{1,3})\.(?:\d{1,3})\.(?:\d{1,3}))(?:(?:<[^>]+?>)|(?::))?(\d{2,4})\s*",
                        siteproxies,
                    )
                    if anything:
                        print(str(anything)[:80], end="\r")
                        downloadedproxies.append(anything)
                        for __ in anything:
                            proxylistwithport.append(f"{__[0]}:{__[1]}")
                    print(str(downloadedproxies)[:80], end="\r")
                    proxylistwithport = list(dict.fromkeys(proxylistwithport))
                    if any(proxylistwithport):
                        self.proxies.append("\n".join(proxylistwithport))
                except Exception as Fehler:
                    print(Fehler)

            except Exception as Fe:
                if self.debug:
                    clearp.c_red(Fe)
            sleep(get_random_time(sleeptime[0], sleeptime[1]))
        return self

    def load_json_proxys(self, proxylist=None, sleeptime=(0.1, 0.7)):
        if proxylist is None:
            return self
        proxylist = list(dict.fromkeys(proxylist))
        for prox in proxylist:
            try:
                prox_result = get_proxys_from_json(
                    prox, header=self.fakeheader, debug=self.debug
                )
                if len(prox_result) > 10:
                    self.proxies.append(prox_result)
                    if self.debug:
                        clearp.c_lightgreen(f"{prox}")
                else:
                    if self.debug:

                        clearp.c_red(f"{prox}")

            except Exception as Fe:
                if self.debug:
                    clearp.c_red(Fe)
            sleep(get_random_time(sleeptime[0], sleeptime[1]))
        return self

    def prepare_proxy_dataframe(self):
        dfproxy = pd.DataFrame(
            flatten_everything([x.splitlines() for x in self.proxies])
        )
        dfproxy = (
            dfproxy.drop_duplicates()
            .astype("string")[0]
            .str.extract(r"((?:\d{1,3})\.(?:\d{1,3})\.(?:\d{1,3})\.(?:\d{1,3})):(\d+)")
            .dropna()
            .reset_index(drop=True)
            .rename(columns={0: "aa_ip", 1: "aa_port"})
        )
        dfproxy["aa_address"] = dfproxy.aa_ip + ":" + dfproxy.aa_port

        self.proxydf = (
            dfproxy.dropna()
            .drop_duplicates(subset="aa_ip")
            .copy()
            .reset_index(drop=True)
        )
        self.proxydf = self.proxydf.loc[
            self.proxydf.aa_address.str.contains(r"\d+\.\d+\.\d+\.\d+:\d+")
        ].copy()
        return self


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="PROXY DOWNLOAD")
    parser.add_argument(
        "-p", "--proxy_txt_list", type=str, help=f'Input for proxy text (txt files)"""',
    )

    parser.add_argument(
        "-j", "--proxy_json", type=str, help=f'Input for proxy test (json files)"""',
    )

    parser.add_argument(
        "-s",
        "--save_proxy_dataframe",
        type=str,
        help=f'File to save dataframe, ending pkl / xlsx!"""',
    )

    parser.add_argument(
        "-m",
        "--max_proxies_to_check",
        type=int,
        default=1000,
        help=f'Max number of proxies to save"""',
    )

    args = parser.parse_args()
    proxy_json = args.proxy_json
    proxy_txt_list = args.proxy_txt_list
    max_proxies_to_check = args.max_proxies_to_check

    save_proxy_dataframe = args.save_proxy_dataframe
    self = GetProxiesGIT(debug=False)
    self.load_txt_proxys(openfile_andstrip(path=proxy_txt_list))
    self.load_json_proxys(openfile_andstrip(path=proxy_json))
    timest = get_timestamp()
    self.prepare_proxy_dataframe()
    saveproxydataframexlsx, saveproxydataframepkl = get_filepath_for_xlsx_and_pkl(
        save_proxy_dataframe
    )
    make_folder_for_excel_and_pkl(saveproxydataframexlsx, saveproxydataframepkl)
    self.proxydf[:max_proxies_to_check].to_excel(saveproxydataframexlsx)
    self.proxydf[:max_proxies_to_check].to_pickle(saveproxydataframepkl)
    print("\n")
    print((f"Excellist with proxies: {saveproxydataframexlsx}"))
    print((f"PKLlist with proxies: {saveproxydataframepkl}"))
