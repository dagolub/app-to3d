import os
import uuid
import aiohttp
import asyncio
import boto3
from app import crud

AWS_ACCESS_KEY_ID = "VG7WONEHRGNFPHIIXLSN" # noqa
AWS_SECRET_ACCESS_KEY = "6FG+T6STRNmaoQZ/zF9SX9gxsK13tBHzgfMSBKV6mUg" # noqa
AWS_BUCKET = 'cdn3d' # noqa
AWS_REGION = 'fra1' # noqa
AWS_ENDPOINT = 'https://fra1.digitaloceanspaces.com' # noqa


def set_public(file):
    s3 = boto3.resource('s3',
                        region_name=AWS_REGION,
                        endpoint_url=AWS_ENDPOINT,
                        aws_access_key_id=AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    s3_object = s3.Bucket(AWS_BUCKET).Object(file)
    s3_object.Acl().put(ACL='public-read')

async def async_download(data, db):
    item = crud.item.create(db=db, obj_in=data)
    if not os.path.exists("downloads"):
        os.mkdir("downloads")
    if not os.path.exists("downloads/images"):
        os.mkdir("downloads/images")

    if not os.path.exists("downloads/files"):
        os.mkdir("downloads/files")

    object_id = uuid.uuid4().__str__()

    if not os.path.exists(f"downloads/images/{object_id}"):
        os.mkdir(f"downloads/images/{object_id}")

    if not os.path.exists(f"downloads/files/{object_id}"):
        os.mkdir(f"downloads/files/{object_id}")

    headers = {}

    # async with aiohttp.ClientSession(headers=headers, trust_env=False) as session:
    #     async_result = await asyncio.gather(*[get_async(url, session) for url in data['images']])
    #     for result, file_name in async_result:
    #         image_file = f"{uuid.uuid4().__str__()}.jpg"
    #         with open(f"downloads/images/{object_id}/{image_file}", 'wb') as local_file:
    #             print(f"{file_name} - downloads/images/{object_id}/{image_file}")
    #             local_file.write(result)

    s3_client = boto3.client('s3',
                             region_name=AWS_REGION,
                             endpoint_url=AWS_ENDPOINT,
                             aws_access_key_id=AWS_ACCESS_KEY_ID,
                             aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    result = s3_client.list_objects_v2(AWS_BUCKET, "1000444.zip")

    print(data)
    headers = data['files'][0]['headers']
    async with aiohttp.ClientSession(headers=headers, trust_env=False) as session:
        async_result = await asyncio.gather(*[get_async(url, session) for url in data['files']])
        for result, file_name in async_result:
            file = f"{file_name}"
            with open(f"downloads/files/{object_id}/{file}", 'wb') as local_file:
                print(f"{file_name} - downloads/files/{object_id}/{file}")
                local_file.write(result)


async def get_async(url, session):
    file_name = url['name'] if 'name' in url else url.split("/")[-1]
    if 'download_url' in url:
        url = url['download_url']
    try:
        async with session.get(url=url, ssl=False) as response:
            return await response.read(), file_name
    except Exception as e:
        print("Unable to get url {} due to {}.".format(url, e.__class__))
        return False, False
