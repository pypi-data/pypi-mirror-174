import argparse
import asyncio
import os
import re
from time import strftime

import pandas as pd
import regex
from fake_headers import Headers

from downloader_cpr import ClearPrinter
from flatten_everything import ProtectedTuple, flatten_everything
import numpy as np

regexsearch = regex.compile(r"\((0)%[^\)]+\).*?=\s+\b(\d+)ms\b")


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


def to_utf8(string_):
    try:
        return string_.decode("utf-8", "ignore")
    except Exception as Fehler:
        print(Fehler)
    return string_


def read_proxies_xlsx(excelpath):
    df = pd.read_excel(excelpath)
    df = df.drop(columns=[x for x in df.columns if ":" in x]).copy()
    if "aa_fake_header" in df.columns:
        df = df.assign(aa_fake_header=lambda x_: x_.aa_fake_header.apply(eval))
    if "aa_proxyDict" in df.columns:
        df = df.assign(aa_proxyDict=lambda x__: x__.aa_proxyDict.apply(eval)).copy()
    return df


def get_filepath_for_xlsx_and_pkl(save_proxy_dataframe):
    regex_fuer_pickle = regex.compile(r"\.(?:(?:pkl)|(?:xlsx))$")
    saveproxydataframexlsx = regex_fuer_pickle.sub("", save_proxy_dataframe) + ".xlsx"
    saveproxydataframepkl = regex_fuer_pickle.sub("", save_proxy_dataframe) + ".pkl"

    return saveproxydataframexlsx, saveproxydataframepkl


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


def get_timestamp():
    return strftime("%Y_%m_%d_%H_%M_%S")


async def request(cmd, aa_ip, aa_port, aa_address, indeno):
    try:
        proc = await asyncio.create_subprocess_shell(
            cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout = ""
        stderr = ""
        stdout, stderr = await proc.communicate()
        stdoututf = " ".join(to_utf8(stdout).splitlines())
        if regexsearch.search(stdoututf) is None:
            return ProtectedTuple(("", "", "", cmd, aa_ip, aa_port, aa_address, indeno))

        return ProtectedTuple(
            (
                proc.returncode,
                stdoututf,
                to_utf8(stderr),
                cmd,
                aa_ip,
                aa_port,
                aa_address,
                indeno,
            )
        )
    except Exception as Fehler:
        return ProtectedTuple(("", "", "", cmd, aa_ip, aa_port, aa_address, indeno))


def main(proxlist):
    allgroupsx.append(
        asyncio.gather(
            *[
                request(
                    f"ping {i.aa_ip} -n 1", i.aa_ip, i.aa_port, i.aa_address, indeno
                )
                for indeno, i in proxlist.iterrows()
            ]
        )
    )
    all_groups = asyncio.gather(*allgroupsx)
    results = loop.run_until_complete(all_groups)
    results = [x for x in results if not isinstance(x, tuple)]
    results = flatten_everything(results)
    df2 = pd.DataFrame.from_records(results)
    df = df2[1].str.extract(r"\((0)%[^\)]+\).*?=\s+\b(\d+)ms\b").copy()
    df.columns = ["is_good", "aa_time"]
    df["aa_ip"] = df2[4].copy()
    df["aa_port"] = df2[5].copy()

    df["aa_address"] = df2[6].copy()
    df = df.loc[
        (~df.aa_ip.str.contains("127.0.0.1")) | (~df.aa_ip.str.contains("192.168.0.1"))
    ]
    df = (
        df.dropna()
        .sort_values(by="aa_time")
        .reset_index(drop=True)
        .drop(columns=["is_good"])
    )
    df["aa_weights"] = 1

    df = pd.concat(
        [
            df.copy().assign(aa_address=lambda x: "http:http://" + x.aa_address),
            df.copy().assign(aa_address=lambda x: "https:https://" + x.aa_address),
            df.copy().assign(aa_address=lambda x: "http:socks5://" + x.aa_address),
            df.copy().assign(aa_address=lambda x: "https:socks5://" + x.aa_address),
        ]
    ).reset_index(drop=True)
    df["aa_fake_header"] = [get_fake_header(debug=False) for _ in range(len(df))]

    print(f"VALID IP-ADDRESSES:\n{df.aa_ip.__array__()}")

    return df


def get_proxy_dict(proxyserver):
    howtoconnect = proxyserver.split(":", maxsplit=1)[0]
    serverandport = proxyserver.split(":", maxsplit=1)[-1].strip('"')
    proxyDict = {howtoconnect: serverandport}
    return howtoconnect, serverandport, proxyDict


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PING CHECK")
    parser.add_argument(
        "-p", "--proxy_xlsx", type=str, help=f'Input for proxy Text"""',
    )

    parser.add_argument(
        "-s",
        "--save_proxy_dataframe",
        type=str,
        help=f'Filename to save dataframe! Without file ending, pkl and xlsx will be added!"""',
    )

    parser.add_argument(
        "-m", "--maxthreads", type=int, default=100, help=rf"MAX PINGS AT SAME TIME",
    )

    parser.add_argument(
        "-w",
        "--webaddress",
        type=str,
        default="https://api.ipify.org",
        help=rf"For requests check later on, default=https://api.ipify.org",
    )

    args = parser.parse_args()
    webaddress = args.webaddress
    save_proxy_dataframe = args.save_proxy_dataframe
    proxy_xlsx = args.proxy_xlsx
    maxthreads = args.maxthreads
    timest = get_timestamp()

    loop = asyncio.get_event_loop()
    allgroupsx = []
    proxydf = read_proxies_xlsx(proxy_xlsx)
    proxyrawlist_ = proxydf.aa_ip.to_list().copy()
    if len(proxyrawlist_) > maxthreads:
        proxyrawlist_ = np.array_split(proxydf, len(proxyrawlist_) // maxthreads)
    else:
        proxyrawlist_ = [proxydf]

    alldfs = []
    for sublist in proxyrawlist_:
        dfa = main(sublist)
        alldfs.append(dfa.copy())
    loop.close()
    df = (
        pd.concat(alldfs, ignore_index=True)
        .drop_duplicates("aa_address")
        .sort_values("aa_time")
        .reset_index(drop=True)
    )

    dfproxy = pd.merge(
        df,
        df.apply(
            lambda x: pd.Series(
                get_proxy_dict(x.aa_address),
                index=["aa_howtoconnect", "aa_serverandport", "aa_proxyDict"],
            ),
            axis=1,
        ),
        left_index=True,
        right_index=True,
    ).copy()

    dfproxy["aa_downloadlink_original"] = [webaddress] * len(dfproxy)

    dfproxy["aa_downloadlink"] = (
        dfproxy.aa_howtoconnect
        + dfproxy.aa_downloadlink_original.str.replace(
            r"^[^:]+(?=:)", "", regex=True, flags=re.IGNORECASE
        ).copy()
    )
    dfproxy["aa_timeout"] = [1] * len(df)

    saveproxydataframexlsx, saveproxydataframepkl = get_filepath_for_xlsx_and_pkl(
        save_proxy_dataframe
    )
    make_folder_for_excel_and_pkl(saveproxydataframexlsx, saveproxydataframepkl)
    dfproxy.to_excel(saveproxydataframexlsx)
    dfproxy.to_pickle(saveproxydataframepkl)
    print("\n")
    print((f"Excellist with proxies: {saveproxydataframexlsx}"))
    print((f"PKLlist with proxies: {saveproxydataframepkl}"))
    print(f"CHECKED PROXIES: {saveproxydataframepkl}")
