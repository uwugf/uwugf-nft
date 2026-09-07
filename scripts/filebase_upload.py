"""Upload a CAR to a Filebase IPFS bucket and return the root CID it pins.

Filebase pins a CAR when the object carries `x-amz-meta-import: car`, and then
reports the resulting root CID back on the object's metadata as `cid`.
"""
import os, sys, boto3
from botocore.config import Config

car, key = sys.argv[1], sys.argv[2]
s3 = boto3.client(
    "s3",
    endpoint_url=os.environ["FILEBASE_ENDPOINT"],
    aws_access_key_id=os.environ["FILEBASE_KEY"],
    aws_secret_access_key=os.environ["FILEBASE_SECRET"],
    region_name="us-east-1",
    config=Config(signature_version="s3v4", retries={"max_attempts": 5}),
)
bucket = os.environ["FILEBASE_BUCKET"]
size = os.path.getsize(car)
print(f"uploading {car} ({size/1073741824:.2f} GB) -> s3://{bucket}/{key}", flush=True)

seen = [0]
def progress(n):
    seen[0] += n
    pct = seen[0] / size * 100
    if int(pct) % 5 == 0:
        print(f"  {pct:5.1f}%  {seen[0]/1073741824:.2f} GB", flush=True)

with open(car, "rb") as f:
    s3.upload_fileobj(f, bucket, key,
                      ExtraArgs={"Metadata": {"import": "car"}},
                      Callback=progress)

head = s3.head_object(Bucket=bucket, Key=key)
print("done. object metadata:", head.get("Metadata"))
