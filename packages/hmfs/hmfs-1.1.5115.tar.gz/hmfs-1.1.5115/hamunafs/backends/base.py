import os
from aiohttp_retry import RetryClient, ExponentialRetry
from aiofile import async_open
import wget

class BackendBase:
    def __init__(self, cfg) -> None:
        self.cfg = cfg
        
    def put(self, filename, bucket, bucket_name):
        pass
    
    def put_buffer(self, buffer, bucket, bucket_name):
        pass

    async def put_async(self, filename, bucket, bucket_name):
        pass
    
    async def put_buffer_async(self, buffer, bucket, bucket_name):
        pass
    
    def get(self, filename, bucket, bucket_name):
        pass
    
    def geturl(self, entrypoint):
        return entrypoint

    async def get_async(self, filename, bucket, bucket_name):
        pass

    async def cleanup_old_files(self):
        pass

    async def download_file(self, url, path, buffer_size=4096):
        retry_opts = ExponentialRetry(attempts=3)
        async with RetryClient(retry_options=retry_opts) as session:
            async with session.get(url) as response:
                if response.status == 200:
                    with open(path, mode='wb') as f:
                        while True:
                            chunk = await response.content.read(buffer_size)
                            if not chunk:
                                break
                            f.write(chunk)
                else:
                    raise ValueError()
        # wget.download(url, path)

    def create_dir_if_not_exists(self, path):
        os.makedirs(os.path.split(path)[0], exist_ok=True)
    