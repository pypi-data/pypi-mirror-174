import asyncio
from pathlib import Path

from qiniu import Auth, BucketManager, build_batch_delete, etag, put_file

from beni import bhttp, bpath, bzip
from beni.bqiniu import QiniuItem


class QiniuBucket():

    def __init__(self, bucket: str, baseUrl: str, ak: str, sk: str) -> None:
        self.q = Auth(ak, sk)
        self.bucket = bucket
        self.baseUrl = baseUrl

    def uploadFile(self, key: str, localFile: Path | str):
        token = self.q.upload_token(self.bucket, key)
        _, info = put_file(token, key, localFile, version='v2')
        assert info.exception is None
        assert info.status_code == 200

    def getPrivateFileUrl(self, key: str):
        return self.q.private_download_url(f'{self.baseUrl}/{key}')

    def downloadPrivateFile(self, key: str, localFile: Path | str):
        url = self.getPrivateFileUrl(key)
        tempFile = bpath.getTempFile()
        asyncio.run(bhttp.download(url, tempFile))
        assert tempFile.exists()
        localFile = bpath.get(localFile)
        bpath.move(tempFile, localFile, True)

    def downloadUnzipPrivateFile(self, key: str, outputDir: Path | str):
        url = self.getPrivateFileUrl(key)
        tempFile = bpath.getTempFile()
        asyncio.run(bhttp.download(url, tempFile))
        assert tempFile.exists()
        tempDir = bpath.getTempDir()
        try:
            bzip.unzip(tempFile, tempDir)
            for file in bpath.listFile(tempDir, True):
                toFile = bpath.changeRelative(file, tempDir, outputDir)
                bpath.move(file, toFile, True)
        finally:
            bpath.remove(tempDir)
            bpath.remove(tempFile)

    def getFileList(self, prefix: str, limit: int = 100) -> tuple[list[QiniuItem], str | None]:
        bucket = BucketManager(self.q)
        result, _, _ = bucket.list(self.bucket, prefix, None, limit)
        assert type(result) is dict
        fileList = [QiniuItem(x['key'], x['fsize'], x['hash'], x['putTime']) for x in result['items']]
        return fileList, result.get('marker', None)

    def getFileListByMarker(self, marker: str, limit: int = 100):
        bucket = BucketManager(self.q)
        result, _, _ = bucket.list(self.bucket, None, marker, limit)
        assert type(result) is dict
        fileList = [QiniuItem(x['key'], x['fsize'], x['hash'], x['putTime']) for x in result['items']]
        return fileList, result.get('marker', None)

    def deleteFiles(self, *keyList: str):
        bucket = BucketManager(self.q)
        result, _ = bucket.batch(
            build_batch_delete(self.bucket, keyList)
        )
        assert result

    def hashFile(self, file: Path | str):
        return etag(file)
