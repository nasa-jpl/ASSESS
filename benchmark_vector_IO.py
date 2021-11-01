import numpy as np
import pickle
import datetime
import sys

d = 1000                      # dimension
nb = 1000000                      # database size
np.random.seed(1234)             # make reproducible
xb_32 = np.random.random((nb, d)).astype('float32')

print(xb_32.shape)
print('xb_32: memory size in bytes:', xb_32.itemsize)

save_to_disk=datetime.datetime.now()
with open('test.pk', 'wb') as vec:
    pickle.dump(xb_32, vec)
print('save_to_disk time:',datetime.datetime.now()-save_to_disk)

load_from_disk=datetime.datetime.now()
xb_32_=pickle.load(open('test.pk', 'rb'))
print('load_from_disk time:',datetime.datetime.now()-load_from_disk)

convert_to_dict=datetime.datetime.now()
dict_xb_32={}
for i, item in enumerate(xb_32):
    dict_xb_32[i]=item
print('convert_to_dict time:',datetime.datetime.now()-convert_to_dict)

print(len(dict_xb_32))
print('dict_xb_32: memory size in mega bytes:', sys.getsizeof(dict_xb_32)/(1024*1024))

save_to_disk=datetime.datetime.now()
with open('test.pk', 'wb') as vec:
    pickle.dump(dict_xb_32, vec)
print('save_to_disk time:',datetime.datetime.now()-save_to_disk)

load_from_disk=datetime.datetime.now()
dict_xb_32_=pickle.load(open('test.pk', 'rb'))
print('load_from_disk time:',datetime.datetime.now()-load_from_disk)

convert_to_np_array=datetime.datetime.now()
xb_32=[]
for ES_id, vector in dict_xb_32_.items():
    xb_32.append(vector)
xb_32=np.array(xb_32)
print(xb_32.shape)
print('convert_to_np_array time:',datetime.datetime.now()-convert_to_np_array)
