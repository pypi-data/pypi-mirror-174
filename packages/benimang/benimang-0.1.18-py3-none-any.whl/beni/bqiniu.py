import uuid
import asyncio
from pathlib import Path
from typing import Any, NamedTuple

from beni import bexecute, bfile, bpath, bhttp, bzip

_isInited = False
_initLock = asyncio.Lock()
_name: str = ''
_ak: str = ''
_sk: str = ''


class QiniuItem(NamedTuple):
    key: str
    size: int
    qetag: str
    time: int


def init(name: str, ak: str, sk: str):
    global _name, _ak, _sk
    _name = name
    _ak = ak
    _sk = sk


async def uploadFile(bucket: str, key: str, localFile: Path | str):
    await _run(
        'rput',
        bucket,
        f'{key}',
        localFile,
        '--resumable-api-v2',
    )


async def getPrivateFileUrl(url: str):
    resultBytes = await _run(
        'privateurl',
        url,
    )
    result = resultBytes.decode()
    result = result[result.find('{') + 1:result.rfind('}')]
    return result


async def downloadPrivateFile(url: str, localFile: Path | str):
    url = await getPrivateFileUrl(url)
    await bhttp.download(url, localFile)


async def downloadSevenUnzipPrivateFile(url: str, outputDir: Path | str):
    localZipFile = bpath.getWorkspace(str(uuid.uuid4()) + '.7z')
    downloadDir = bpath.getWorkspace(str(uuid.uuid4()))
    bpath.make(downloadDir)
    try:
        await downloadPrivateFile(url, localZipFile)
        await bzip.sevenUnzip(localZipFile, downloadDir)
        for file in bpath.listFile(downloadDir, True):
            if type(outputDir) is not Path:
                outputDir = bpath.get(outputDir)
            toFile = outputDir.joinpath(file.relative_to(downloadDir))
            bpath.remove(toFile)
            bpath.move(file, toFile)
    finally:
        bpath.remove(downloadDir)
        bpath.remove(localZipFile)


async def getFileList(bucket: str, prefix: str):
    resultBytes = await _run(
        'listbucket2',
        bucket,
        f'-p {prefix}',
        '--show-fields Key,FileSize,Hash,PutTime',
    )
    ary = resultBytes.decode().strip().split('\n')[1:]
    ary = [x.split('\t') for x in ary]
    ary = [
        QiniuItem(x[0], int(x[1]), x[2], int(x[3]))
        for x in ary
    ]
    return ary


async def deleteFiles(bucket: str, *keyList: str):
    tempFile = bpath.getWorkspace(f'qiniu_batchdelete_{uuid.uuid4()}.txt')
    bpath.remove(tempFile)
    await bfile.writeText(
        tempFile,
        '\n'.join(keyList),
    )
    try:
        await _run(
            'batchdelete',
            bucket,
            f'-i {tempFile}',
        )
    finally:
        bpath.remove(tempFile)


async def hashFile(file: Path | str):
    resultBytes = await _run(
        'qetag',
        file,
    )
    return resultBytes.decode().strip()


async def _init():
    global _isInited
    await _initLock.acquire()
    if not _isInited:
        assert _ak and _sk and _name, '需要先调用bqiniu.init传入参数初始化'
        await bexecute.runQuiet(f"qshell user clean")
        await bexecute.runQuiet(f"qshell account {_ak} {_sk} {_name}")
        _isInited = True
    _initLock.release()


async def _run(*parList: Any):
    if not _isInited:
        await _init()
    resultBytes, errorBytes = await bexecute.runQuiet('qshell', *parList)
    assert not errorBytes, errorBytes.decode()
    return resultBytes
