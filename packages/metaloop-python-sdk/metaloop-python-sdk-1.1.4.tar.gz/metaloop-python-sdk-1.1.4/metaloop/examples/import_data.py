import time

from metaloop.client import MDS

if __name__ == '__main__':
    mds_client = MDS("0c02ca70e142b75a75ca4118ce33dbb0", "http://192.168.100.71:30301")

    date_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
    dataset_name = f"test_dataset_{date_time}"

    # create dataset
    dataset = mds_client.create_dataset(
        dataset_name,
        "image",
        ["screw"],
        comment="this is a test dataset for mds"
    )

    # import zip file
    dataset.import_data("import_test/sample_test.zip")
    dataset.summary()

    # import directory
    dataset.import_data("import_test/sample_test")
    dataset.summary()

    # import directory and save data to external cloud storage
    dataset.import_data("import_test/sample_test", storage_type="cos")
    dataset.summary()

    # create a new version and inherit data from a previous version
    dataset.create_version(0, "this is a inherited test version")
    dataset.summary()

    mds_client.delete_dataset(dataset_name)
