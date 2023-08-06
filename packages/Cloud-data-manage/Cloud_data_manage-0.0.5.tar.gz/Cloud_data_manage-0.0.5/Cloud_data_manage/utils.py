from typing import Union
import os


class FileRelated(object):
    @staticmethod
    def get_onprem_file_md5(onprem_file_name: str, format='hex') -> Union[str, bytearray]:
        pass

    @staticmethod
    def get_onprem_file_sha256(onprem_file_name):
        pass

    @staticmethod
    def findfile(path, target_file_name):
        pass


class Bioinformatics(object):
    @staticmethod
    def bam2fq(samtools: str, bam_file: str, r1_out: str, r2_out: str, thread_num: int = 8) -> None:
        pass
