"""Contains class for writing conversion results to file."""
import csv
from datetime import datetime
import tarfile
import tempfile


class ResultWriter():
    """
    Contains writer for writing conversion result to csv files and
    creating tar archives containing them.
    """
    EXTERNAL_DATA_FILE_NAME = "external_data.csv"
    DUMP_INFORMATION_FILE_NAME = "dump_information.csv"
    IDENTIFIER_PROPERTIES_FILE_NAME = "identifier_properties.csv"

    def __init__(self):
        """
        Creates new ResultWriter instance.
        """
        self.external_data_file = tempfile.TemporaryFile()
        self.external_data_writer = csv.writer(self.external_data_file)

        self.dump_information_file = tempfile.TemporaryFile()
        self.dump_information_writer = csv.writer(self.dump_information_file)

        self.identifier_properties_file = tempfile.TemporaryFile()
        self.identifier_properties_writer = csv.writer(self.identifier_properties_file)

    def write_external_value(self, dump_id, external_id,
                             property_id, value):
        """
        Writes single external value to file.
        :param dump_id: Id of the current dump.
        :param external_id: Id of the external entity.
        :param property_id: Id of the Wikidata property.
        :param value: Data value of external entity for the Wikidata property.
        """
        row = (
            dump_id,
            external_id,
            property_id,
            value
        )
        self.external_data_writer.writerow(row)

    def write_dump_information(self, data_source_item_id, language, source_url,
                               size, license_item_id):
        """
        Writes meta information about a single dump to file.
        :param data_source_item_id: Id of the Wikidata item of the data source.
        :param language: Language code.
        :param source_url: Source url.
        :param size: File size in bytes.
        :param license_item_id: Id of the Wikidata item of the license.
        :return:
        """
        row = (
            data_source_item_id,
            datetime.utcnow(),
            language,
            source_url,
            size,
            license_item_id
        )
        self.dump_information_writer.writerow(row)

    def write_identifier_property(self, identifier_property_id, dump_id):
        """
        Writes tuple of identifier property and corresponding dump id to file.
        :param identifier_property_id: Id of the Wikidata identifier property.
        :param dump_id: Id of the dump.
        """
        row = (
            identifier_property_id,
            dump_id
        )
        self.identifier_properties_writer.writerow(row)

    def to_archive(self, file_path):
        """
        Creates tar archive containing written csv files.
        :param file_path: Path of the archive file that is to be created.
        """
        with tarfile.open(file_path, mode="w:gz") as tar_file:
            self.add_file_to_tar(tar_file, self.EXTERNAL_DATA_FILE_NAME,
                                 self.external_data_file)
            self.add_file_to_tar(tar_file, self.DUMP_INFORMATION_FILE_NAME,
                                 self.dump_information_file)
            self.add_file_to_tar(tar_file, self.IDENTIFIER_PROPERTIES_FILE_NAME,
                                 self.identifier_properties_file)

    @staticmethod
    def add_file_to_tar(tar_file, name, fileobj):
        """
        Adds file to a tar archive.
        :param tar_file: Tar archive.
        :param name: Name of the file that is to be added.
        :param fileobj: File object that is to be added.
        """
        fileobj.flush()
        fileobj.seek(0)

        tar_info = tar_file.gettarinfo(arcname=name, fileobj=fileobj)
        tar_file.addfile(tar_info, fileobj)

    def close(self):
        """
        Close opened csv files.
        """
        self.external_data_file.close()
        self.dump_information_file.close()
        self.identifier_properties_file.close()
