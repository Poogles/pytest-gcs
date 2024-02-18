"""General plugin tests."""
from google.cloud import storage

from pytest_gcs.executor.process import GCSExecutor


def test_gcs_works_mvp(gcs_proc: GCSExecutor, gcslocal: storage.Client) -> None:
    """MVP to ensure everything works."""
    bucket = "test_base"
    gcslocal.create_bucket(bucket)
    buckets = [x.name for x in gcslocal.list_buckets()]

    assert bucket in buckets


def test_gcs_multiple_bucket_sandboxing(
    gcs_proc1: GCSExecutor,
    gcslocal1: storage.Client,
    gcs_proc2: GCSExecutor,
    gcslocal2: storage.Client,
) -> None:
    """Ensure sandboxing between procs."""
    bucket_1 = "test_conflict1"
    bucket_2 = "test_conflict2"
    gcslocal1.create_bucket(bucket_1)
    gcslocal2.create_bucket(bucket_2)

    gcs_local_buckets_1 = [x.name for x in gcslocal1.list_buckets()]
    gcs_local_buckets_2 = [x.name for x in gcslocal2.list_buckets()]

    assert gcs_local_buckets_1 == [bucket_1]
    assert gcs_local_buckets_2 == [bucket_2]


def test_gcs_write_read_files(gcs_proc: GCSExecutor, gcslocal: storage.Client) -> None:
    """Test read/write to bucket."""
    bucket = gcslocal.create_bucket("test_writable")
    test_file = "test"
    blob = bucket.blob(test_file)
    test_string = "potato"
    blob.upload_from_string(test_string)

    assert bucket.get_blob(test_file).download_as_bytes().decode() == test_string
