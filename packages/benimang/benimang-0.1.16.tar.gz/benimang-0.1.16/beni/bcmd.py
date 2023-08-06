import asyncio
import json
import os
import sys
import time
from datetime import datetime as Datetime
from datetime import timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import nest_asyncio
import typer
from colorama import Fore

from beni import bcolor, bfile, bpath

_app = typer.Typer()


def main():
    nest_asyncio.apply()
    _app()


def exit(errorMsg: str):
    print(errorMsg)
    sys.exit(errorMsg and 1 or 0)


# ------------------------------------------------------------------------


@_app.command('time')
def showtime(
    value: str = typer.Argument('', help='时间戳（支持整形和浮点型）或日期（格式: 2021-11-23）', show_default=False, metavar='[Timestamp or Date]'),
    value2: str = typer.Argument('', help='时间（格式: 09:20:20），只有第一个参数为日期才有意义', show_default=False, metavar='[Time]')
):
    '''
    格式化时间戳

    beni showtime

    beni showtime 1632412740

    beni showtime 1632412740.1234

    beni showtime 2021-9-23

    beni showtime 2021-9-23 09:47:00
    '''

    timestamp: float | None = None
    if not value:
        timestamp = time.time()
    else:
        try:
            timestamp = float(value)
        except:
            try:
                if value2:
                    timestamp = Datetime.strptime(f'{value} {value2}', '%Y-%m-%d %H:%M:%S').timestamp()
                else:
                    timestamp = Datetime.strptime(f'{value}', '%Y-%m-%d').timestamp()
            except:
                pass

    if timestamp is None:
        color = typer.colors.BRIGHT_RED
        typer.secho('参数无效', fg=color)
        typer.secho('\n可使用格式: ', fg=color)
        msgAry = str(showtime.__doc__).strip().replace('\n\n', '\n').split('\n')[1:]
        msgAry = [x.strip() for x in msgAry]
        typer.secho('\n'.join(msgAry), fg=color)
        raise typer.Abort()

    print()
    print(timestamp)
    print()
    localtime = time.localtime(timestamp)
    tzname = time.tzname[(time.daylight and localtime.tm_isdst) and 1 or 0]
    bcolor.printx(time.strftime('%Y-%m-%d %H:%M:%S %z', localtime), tzname, colorList=[Fore.YELLOW])
    print()

    # pytz版本，留作参考别删除
    # tzNameList = [
    #     'Asia/Tokyo',
    #     'Asia/Kolkata',
    #     'Europe/London',
    #     'America/New_York',
    #     'America/Chicago',
    #     'America/Los_Angeles',
    # ]
    # for tzName in tzNameList:
    #     tz = pytz.timezone(tzName)
    #     print(Datetime.fromtimestamp(timestamp, tz).strftime(fmt), tzName)

    datetime_utc = Datetime.fromtimestamp(timestamp, tz=timezone.utc)
    tzname_list = [
        'Australia/Sydney',
        'Asia/Tokyo',
        'Asia/Kolkata',
        'Africa/Cairo',
        'Europe/London',
        'America/Sao_Paulo',
        'America/New_York',
        'America/Chicago',
        'America/Los_Angeles',
    ]
    for tzname in tzname_list:
        datetime_tz = datetime_utc.astimezone(ZoneInfo(tzname))
        dstStr = ''
        dst = datetime_tz.dst()
        if dst:
            dstStr = f'(DST+{dst})'
        print(f'{datetime_tz} {tzname} {dstStr}')

    print()

# ------------------------------------------------------------------------


@_app.command()
def format_json_file(file_path: str, encoding: str = 'utf8'):
    file = bpath.get(file_path)
    content = file.read_text(encoding=encoding)
    data = json.loads(content)
    file.write_text(json.dumps(data, indent=4, ensure_ascii=False, sort_keys=True), encoding=encoding)


# ------------------------------------------------------------------------


@_app.command()
def fetch_bin(
    name: str = typer.Argument(None, help="如果有多个使用,分割"),
    is_file: bool = typer.Option(False, '--is-file', '-f', help="文件形式指定参数，行为单位"),
    ak: str = typer.Option(..., help="七牛云账号AK"),
    sk: str = typer.Option(..., help="七牛云账号SK"),
    output: Path = typer.Option(None, '--output', '-o', help="本地保存路径")
):
    from beni.bqiniusdk import QiniuBucket
    try:
        bucketName = 'pytask'
        bucketUrl = 'http://qiniu-cdn.pytask.com'
        if output is None:
            output = Path(os.curdir)
        bucket = QiniuBucket(bucketName, bucketUrl, ak, sk)
        targetList: list[str] = []
        if is_file:
            content = asyncio.run(
                bfile.readText(Path(name))
            )
            targetList.extend(content.replace('\r\n', '\n').split('\n'))
        else:
            targetList.extend(name.strip().split(','))
        for target in targetList:
            file = output.joinpath(target).resolve()
            if file.exists():
                print(f'exists {file}')
            else:
                key = f'bin/{target}.zip'
                bucket.downloadUnzipPrivateFile(key, output)
                bcolor.printGreen(f'added  {file}')
    except Exception as e:
        print(e)


# @_app.command()
# def synclib():
#     '''
#     src -> lib
#     '''
#     _sync_path(
#         _getpath_src(),
#         _getpath_lib(),
#     )


# @_app.command()
# def syncsrc():
#     '''
#     lib -> src
#     '''
#     _sync_path(
#         _getpath_lib(),
#         _getpath_src(),
#     )


# def _getpath_lib():
#     return getpath_user(r'AppData\Local\Programs\Python\Python310\Lib\site-packages\beni')


# def _getpath_src():
#     KEY_SRC: Final = 'beni_src'
#     path_src = get_storage(KEY_SRC, '')
#     is_update_storage = False
#     while True:
#         print()
#         print('-' * 50)
#         print()
#         print(f'lib: {_getpath_lib()}')
#         print(f'src: {path_src}')
#         print()
#         print('确认输入[ok]')
#         print('退出输入[exit]')
#         print('修改src路径直接输入路径')
#         print()
#         value = hold('输入', False, '*')
#         match(value):
#             case 'ok':
#                 break
#             case 'exit':
#                 exit('主动退出')
#             case _:
#                 print('go here')
#                 if value != path_src:
#                     is_update_storage = True
#                 path_src = value
#     if is_update_storage:
#         print('go save')
#         set_storage(KEY_SRC, str(path_src))
#     return getpath(path_src)


# def _sync_path(path_from: Path, path_to: Path):

#     print()
#     print('-' * 50)
#     print()
#     print('确认当前操作')
#     print(path_from)
#     print('->')
#     print(path_to)
#     print()

#     match(hold('确认输入[ok] 退出输入[exit]', False, 'exit', 'ok')):
#         case 'ok':
#             pass
#         case 'exit':
#             exit('主动退出')
#         case _:
#             pass

#     clear_dirs(path_to)
#     for file_from in path_from.glob('**/*'):
#         if file_from.is_file():
#             file_to = path_to / file_from.relative_to(path_from)
#             copy(file_from, file_to)


# # ------------------------------------------------------------------------
