import os
import subprocess
import sys
from tempfile import TemporaryDirectory
from random import shuffle
import regex
from typing import Union

joinfolder_with_cwd = lambda x: os.path.join(
    f"{os.sep}".join(regex.split(r"[\\/]+", __file__)[:-1]), x
)

pythonpath = sys.executable
regex_fuer_pickle = regex.compile(r"\.(?:(?:pkl)|(?:xlsx))$")

list_with_json_file_proxies = (
    "https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list",
    "https://raw.githubusercontent.com/hookzof/socks5_list/master/tg/mtproto.json",
    "https://raw.githubusercontent.com/hookzof/socks5_list/master/tg/socks.json",
)

list_with_txt_file_proxies = (
    "https://raw.githubusercontent.com/BlackSnowDot/proxylist-update-every-minute/main/http.txt",
    "https://raw.githubusercontent.com/BlackSnowDot/proxylist-update-every-minute/main/socks.txt",
    "https://raw.githubusercontent.com/BlackSnowDot/proxylist-update-every-minute/main/https.txt",
    "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt",
    "https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/raw.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/proxy.txt",
    "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt",
    "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
    "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
    "https://raw.githubusercontent.com/zeynoxwashere/proxy-list/main/socks5.txt",
    "https://raw.githubusercontent.com/zeynoxwashere/proxy-list/main/socks4.txt",
    "https://raw.githubusercontent.com/zeynoxwashere/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/proxy.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_geolocation_anonymous/socks5.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_geolocation_anonymous/http.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_geolocation_anonymous/socks4.txt",
    "https://raw.githubusercontent.com/Volodichev/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
    "https://raw.githubusercontent.com/almroot/proxylist/master/list.txt",
    "https://raw.githubusercontent.com/ryanhaticus/superiorproxy.com/main/proxies.txt",
    "https://raw.githubusercontent.com/manuGMG/proxy-365/main/SOCKS5.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt",
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt",
    "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/proxy.txt",
    "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt",
    "https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/socks5.txt",
    "https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/socks4.txt",
    "https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/manuGMG/proxy-365/main/SOCKS5.txt",
    "https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks4.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks5.txt",
    "https://raw.githubusercontent.com/UserR3X/proxy-list/main/online/all.txt",
    "https://raw.githubusercontent.com/hendrikbgr/Free-Proxy-Repo/master/proxy_list.txt",
    "https://www.ipaddress.com/proxy-list/",
    "http://www.proxz.com/proxy_list_high_anonymous_0.html",
    "https://socks-proxy.net/",
    "https://www.proxy-list.download/api/v1/get?type=http",
    "https://us-proxy.org/",
    "https://www.proxy-list.download/api/v1/get?type=https",
    "https://www.proxy-list.download/api/v1/get?type=socks4",
    "https://www.proxy-list.download/api/v1/get?type=socks5",
    "http://proxydb.net/",
    "http://free-proxy.cz/en/",
    "https://www.my-proxy.com/free-proxy-list.html",
    "http://www.httptunnel.ge/ProxyListForFree.aspx",
    "https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-1",
    "https://spys.one/proxies/",
    "https://www.proxynova.com/proxy-server-list/",
    "http://api.foxtools.ru/v2/Proxy.txt?page=1",
    "https://www.marcosbl.com/lab/proxies/",
    "http://free-proxy-list.net/anonymous-proxy.html",
    "http://free-proxy-list.net/",
    "http://proxy-daily.com/",
    "http://sslproxies.org/",
    "http://free-proxy-list.net/uk-proxy.html",
    "http://us-proxy.org/",
    "http://proxyscrape.com/",
    "http://checkerproxy.net/",
    "http://proxy50-50.blogspot.com/",
    "http://hidester.com/",
    "http://awmproxy.net/",
    "http://openproxy.space/",
    "http://aliveproxy.com/",
    "http://community.aliveproxy.com/",
    "http://hidemy.name/en",
    "http://proxy11.com/",
    "http://spys.me/proxy.txt",
    "http://proxysearcher.sourceforge.net/",
    "http://static.fatezero.org/tmp/proxy.txt",
    "http://pubproxy.com/",
    "http://www.proxylists.net/http_highanon.txt",
    "http://ab57.ru/downloads/proxylist.txt",
    "http://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt",
    "http://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
    "http://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt",
    "http://multiproxy.org/txt_all/proxy.txt",
    "http://rootjazz.com/proxies/proxies.txt",
    "http://www.proxyscan.io/api/proxy?format=txt&ping=500&limit=10000&type=http,https",
    "http://www.proxy-list.download/api/v0/get?l=en&t=http",
    "http://list.proxylistplus.com/SSL-List-1",
    "http://www.proxyhub.me/ru/all-https-proxy-list.html",
    "http://www.proxylist4all.com/",
    "http://www.proxynova.com/proxy-server-list",
    "http://www.xiladaili.com/https",
    "https://xseo.in/proxylist",
)


def get_filepath_for_xlsx_and_pkl(save_proxy_dataframe):
    regex_fuer_pickle = regex.compile(r"\.(?:(?:pkl)|(?:xlsx))$")
    saveproxydataframexlsx = regex_fuer_pickle.sub("", save_proxy_dataframe) + ".xlsx"
    saveproxydataframepkl = regex_fuer_pickle.sub("", save_proxy_dataframe) + ".pkl"

    return saveproxydataframexlsx, saveproxydataframepkl


# if getips:
def download_proxy_server_from_web(
    proxy_txt_list,
    proxy_json,
    save_proxy_dataframe,
    silent=False,
    max_proxies_to_check=1000,
):
    save_proxy_dataframe = f"{os.sep}".join(
        regex.split(r"[\\/]+", save_proxy_dataframe)[:-1]
    )
    if not os.path.exists(save_proxy_dataframe):
        os.makedirs(save_proxy_dataframe)
    proxydownload = joinfolder_with_cwd(r"ad_proxy.py")
    subprocesscommand = [
        pythonpath,
        proxydownload,
        "--proxy_txt_list",
        str(proxy_txt_list),
        "--proxy_json",
        str(proxy_json),
        "--save_proxy_dataframe",
        str(save_proxy_dataframe),
        "--max_proxies_to_check",
        str(max_proxies_to_check),
    ]
    print(subprocesscommand)
    subprocess.run(
        subprocesscommand, capture_output=silent,
    )
    saveproxydataframexlsx, saveproxydataframepkl = get_filepath_for_xlsx_and_pkl(
        save_proxy_dataframe
    )
    return saveproxydataframexlsx, saveproxydataframepkl


def do_ping_check_against_proxies(
    proxy_xlsx,
    save_proxy_dataframe,
    maxthreads=100,
    webaddress="https://api.ipify.org",
    silent=False,
):
    pingcheck = joinfolder_with_cwd(r"ad_ping_check.py")
    subprocess.run(
        [
            pythonpath,
            pingcheck,
            "--proxy_xlsx",
            str(proxy_xlsx),
            "--save_proxy_dataframe",
            str(save_proxy_dataframe),
            "--maxthreads",
            str(maxthreads),
            "--webaddress",
            str(webaddress),
        ],
        capture_output=silent,
    )
    saveproxydataframexlsx, saveproxydataframepkl = get_filepath_for_xlsx_and_pkl(
        save_proxy_dataframe
    )
    return saveproxydataframexlsx, saveproxydataframepkl


def do_ip_and_request_check(
    proxy_xlsx,
    save_proxy_dataframe,
    timeout=30,
    thread_limit=200,
    webcheckproxy_url="https://wikipedia.org",
    webcheckproxy_regex=r"Wikimedia\s+Foundation",
    silent=False,
):
    requestcheck = joinfolder_with_cwd(r"aaa_execute_requests_new.py")
    subprocess.run(
        [
            pythonpath,
            requestcheck,
            "--proxy_xlsx",
            str(proxy_xlsx),
            "--save_proxy_dataframe",
            str(save_proxy_dataframe),
            "--timeout",
            str(timeout),
            "--thread_limit",
            str(thread_limit),
            "--webcheckproxy_url",
            str(webcheckproxy_url),
            "--webcheckproxy_regex",
            str(webcheckproxy_regex),
        ],
        capture_output=silent,
    )
    saveproxydataframexlsx, saveproxydataframepkl = get_filepath_for_xlsx_and_pkl(
        save_proxy_dataframe
    )
    return saveproxydataframexlsx, saveproxydataframepkl


def replace_path_sep(path_):
    regexpathcomp = regex.compile(r"[\\/]+")
    regexpathsep = regex.escape(os.sep)
    path_ = regexpathcomp.sub(regexpathsep, path_)
    return path_


def get_proxies(
    list_with_txt_file_links: Union[None, list, tuple] = None,
    list_with_json_file_links: Union[None, list, tuple] = None,
    save_path_proxies_all_filtered: Union[None, str] = None,
    http_check_timeout: int = 10,
    threads_httpcheck: int = 20,
    threads_ping: int = 10,
    silent: bool = False,
    max_proxies_to_check: int = 1000,
):
    r"""
    Example
    from freeproxydownloader.downloader import get_new_proxies
    get_new_proxies(
    list_with_txt_file_links=None,
    list_with_json_file_links=None,
    save_path_proxies_all_filtered='f:\\testproxy',
    http_check_timeout=10,
    threads_httpcheck=20,
    threads_ping=10,
    silent=False,
    max_proxies_to_check=1000
)
     from freeproxydownloader import get_proxies
     get_proxies()
    :param list_with_txt_file_links:
            Example
                ["https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt",
                "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt",
                "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
                "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
                "c:\\proxylist.txt"]
            (default=None) #Will choose randomly from list_with_txt_file_proxies
    :param list_with_json_file_links:
            Example
                ["https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list",
                "https://raw.githubusercontent.com/hookzof/socks5_list/master/tg/mtproto.json",
                "https://raw.githubusercontent.com/hookzof/socks5_list/master/tg/socks.json",]
            (default=None) #Will choose randomly from list_with_json_file_proxies

    :param save_path_proxies_all_filtered:
            Folder for output
            (default=None) #Will create a folder in the root of your env, called "freeproxydownloader_results"

    :param http_check_timeout:
            Timeout for http check with requests
            (default=10)

    :param threads_httpcheck:
            How many threads when doing the http check with requests
            (default=20)

    :param threads_ping:
            How many threads when doing the ping check
            (default=10)

    :param silent:
            verbose or not
            (default=False)

    :param max_proxies_to_check:
            stop checking after n checked proxies in total! (Not positive results!!)
            (default=False)

    :return: filtered_proxies_xlsx, filtered_proxies_pkl #can be opened com pandas
    """
    max_proxies_to_check = max_proxies_to_check // 3
    if save_path_proxies_all_filtered is None:
        outputfilesresultsfolder = os.path.join(
            f"{os.sep}".join(regex.split(r"[\\/]+", sys.executable)[:-1]),
            "freeproxydownloader_results",
        )
    else:
        outputfilesresultsfolder = save_path_proxies_all_filtered
    if not os.path.exists(outputfilesresultsfolder):
        os.makedirs(outputfilesresultsfolder)

    if list_with_txt_file_links is None:
        list_with_txt_file_links = list(
            set([x.strip() for x in list_with_txt_file_proxies])
        )
        shuffle(list_with_txt_file_links)
    if list_with_json_file_links is None:
        list_with_json_file_links = list(
            set([x.strip() for x in list_with_json_file_proxies])
        )
        shuffle(list_with_json_file_links)

    tempfolder = TemporaryDirectory()
    save_path_proxies_not_filtered = os.path.join(
        tempfolder.name, "downloaded_proxiesneu.xlsx"
    )
    save_path_proxies_ping_filtered = os.path.join(
        tempfolder.name, "pingcheckfilter.xlsx"
    )
    if save_path_proxies_all_filtered is None:
        save_path_proxies_all_filtered = os.path.join(
            outputfilesresultsfolder, "results_good_proxies.xlsx"
        )

    tempfile____txtlist = replace_path_sep(
        os.path.join(tempfolder.name, "allright.txt")
    )
    tempfile____jsonlist = replace_path_sep(
        os.path.join(tempfolder.name, "notallright.txt")
    )
    if not os.path.exists(tempfolder.name):
        os.makedirs(tempfolder.name)

    list_with_txt_file_links = "\n".join(
        [x.strip() for x in list_with_txt_file_links]
    ).strip()
    list_with_json_file_links = "\n".join(
        [x.strip() for x in list_with_json_file_links]
    ).strip()
    with open(tempfile____txtlist, mode="w", encoding="utf-8") as f:
        f.write(list_with_txt_file_links)
    with open(tempfile____jsonlist, mode="w", encoding="utf-8") as f:
        f.write(list_with_json_file_links)
    downloaded_proxies_xlsx, downloaded_proxies_pkl = download_proxy_server_from_web(
        proxy_txt_list=tempfile____txtlist,
        proxy_json=tempfile____jsonlist,
        save_proxy_dataframe=save_path_proxies_not_filtered,
        silent=silent,
        max_proxies_to_check=max_proxies_to_check,
    )

    ping_checked_proxies_xlsx, ping_checked_proxies_pkl = do_ping_check_against_proxies(
        proxy_xlsx=downloaded_proxies_xlsx,
        save_proxy_dataframe=save_path_proxies_ping_filtered,
        maxthreads=threads_ping,
        webaddress="https://api.ipify.org",
        silent=silent,
    )

    filtered_proxies_xlsx, filtered_proxies_pkl = do_ip_and_request_check(
        proxy_xlsx=ping_checked_proxies_xlsx,
        save_proxy_dataframe=save_path_proxies_all_filtered,
        timeout=http_check_timeout,
        thread_limit=threads_httpcheck,
        webcheckproxy_url="https://wikipedia.org",
        webcheckproxy_regex=r"Wikimedia\s+Foundation",
        silent=silent,
    )
    return filtered_proxies_xlsx, filtered_proxies_pkl
