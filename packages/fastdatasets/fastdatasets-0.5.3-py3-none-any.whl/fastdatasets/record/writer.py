# @Time    : 2022/9/18 23:07
# @Author  : tk
# @FileName: simple_record.py
import json
import pickle
import typing
import data_serialize
from tfrecords import TFRecordOptions,TFRecordCompressionType,TFRecordWriter,RECORD

__all__ = [
    "data_serialize",
    'pickle',
    'json',
    'RECORD',
    "DataType",
    "TFRecordOptions",
    "TFRecordCompressionType",
    "TFRecordWriter",
    "WriterObject",
    "StringWriter",
    "BytesWriter",
    "PickleWriter",
    "FeatureWriter",
]

class DataType:
    int64_list = 0
    float_list = 1
    bytes_list = 2


class WriterObject:
    def __init__(self, filename, options=TFRecordOptions(compression_type=TFRecordCompressionType.NONE)):
        self.filename = filename
        self.options = options
        self.file_writer = TFRecordWriter(filename, options=options)

    def __del__(self):
        self.close()

    def close(self):
        if self.file_writer is not None:
            self.file_writer.close()

    def write(self, data, *args, **kwargs):
        self.file_writer.write(data)

    def flush(self):
        self.file_writer.flush()

    def __enter__(self):
        if  self.file_writer is None:
            self.file_writer = TFRecordWriter(self.filename, options=self.options)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def write_index_for_RandomDataset(self,display=-1):
        from fastdatasets.record import load_dataset as Loader
        datasets = Loader.RandomDataset(self.filename)
        if display > 0:
            for i in range(len(datasets)):
                if (i + 1) % display == 0:
                    print(i, datasets[i])

class StringWriter(WriterObject):
    def write(self, data,*args, **kwargs):
        self.file_writer.write(data)

class BytesWriter(WriterObject):
    def write(self, data,*args, **kwargs):
        self.file_writer.write(data)

class PickleWriter(WriterObject):
    def write(self, data,*args, **kwargs):
        self.file_writer.write(pickle.dumps(data,*args,**kwargs))


class JsonWriter(WriterObject):
    def write(self, data,*args, **kwargs):
        self.file_writer.write(json.dumps(data,*args,**kwargs))

class FeatureWriter(WriterObject):
    def write(self,feature : typing.Dict,*args, **kwargs):
        assert feature is not None
        dict_data = {}
        for k,v in feature.items():
            val = v['data']
            if v['dtype'] == DataType.int64_list:
                dict_data[k] = data_serialize.Feature(int64_list=data_serialize.Int64List(value=val))
            elif v['dtype'] == DataType.float_list:
                dict_data[k] = data_serialize.Feature(float_list=data_serialize.FloatList(value=val))
            elif v['dtype'] == DataType.bytes_list:
                dict_data[k] = data_serialize.Feature(bytes_list=data_serialize.BytesList(value=val))
            else:
                raise Exception('bad dtype')

        feature = data_serialize.Features(feature=dict_data)
        example = data_serialize.Example(features=feature)
        self.file_writer.write(example.SerializeToString())

