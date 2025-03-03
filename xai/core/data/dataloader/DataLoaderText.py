# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jinkim@seculayer.com
# Powered by Seculayer © 2021 Service Model Team, R&D Center.

from typing import List

from xai.common.Constants import Constants
from dataconverter.core.ConvertAbstract import ConvertAbstract
from xai.core.data.dataloader.DataLoaderAbstract import DataLoaderAbstract


class DataLoaderText(DataLoaderAbstract):

    def __init__(self, job_info, sftp_client):
        super().__init__(job_info, sftp_client)

    def read(self, file_list, fields):
        functions: List[List[ConvertAbstract]] = self.build_functions(fields)
        self.LOGGER.info(functions)

        features = list()
        labels = list()
        origin_data = list()

        for file in file_list:
            self.LOGGER.info("read text file : {}".format(file))
            generator = self.sftp_client.load_json_oneline(
                            filename=file,
                            dataset_format=Constants.DATASET_FORMAT_TEXT
                        )
            while True:
                line: str = next(generator)
                if line == "#file_end#":
                    break
                feature, label, data = self._convert(line, fields, functions)

                features.append(feature), labels.append(label), origin_data.append(data)

        self.make_inout_units(features, fields)
        return [features, labels, origin_data]
