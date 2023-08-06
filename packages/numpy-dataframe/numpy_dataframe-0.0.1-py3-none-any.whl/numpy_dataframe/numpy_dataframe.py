import numpy as np
import pandas as pd
from copy import deepcopy
import numpy_groupies as npg
import time
from collections import defaultdict
import numba as nb

int_array = nb.types.int64[:]
int_list = nb.types.ListType(nb.types.int64)

@nb.jit(nopython=True)
def ordered_clusters_group_by(l,current_type):
    indices = nb.typed.Dict.empty(
        key_type=current_type,
        value_type=int_list
    )

    for i in np.arange(l.shape[0]):
        if l[i] in indices:
        # try:
            indices[l[i]].append(i)
        else:
        # except:
            indices[l[i]] = nb.typed.List([i])

    indices_list = np.empty_like(l,np.int64)
    i = 0
    ks = np.empty(len(indices.keys()))
    for k in indices.keys():
        ks[i] = k
        for h in indices[k]:
            indices_list[h] = i
        i += 1
    return ks,indices_list


class DataFrame:
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)
    def __init__(self):
        super(DataFrame, self).__setattr__('d', {})
        super(DataFrame, self).__setattr__('ncol', 0)
        super(DataFrame, self).__setattr__('nrow', 0)
    def __getattr__(self, key):
        return self.d[key]
    def __setattr__(self, name, value):
        if type(value) == list:
            value = np.array(value)
        self.d[name] = value
        super(DataFrame, self).__setattr__('ncol', self.ncol + 1)
        if self.nrow == 0:
            super(DataFrame, self).__setattr__('nrow', len(value))
    def __getitem__(self,args):
        if type(args) == tuple:
            rows,key=args
            if len(key) == 1:
                if type(key) == list:
                    t_ = DataFrame()
                    for k in key:
                        DataFrame.__setattr__(t_,k,self.d[k][rows])
                    return t_
                else:
                    return self.d[key][rows]
            else:
                t_ = DataFrame()
                for k in key:
                    DataFrame.__setattr__(t_,k,self.d[k][rows])
                return t_
        else:
            key = args
            if type(key) == str:
                return self.d[key]
            else:
                if len(key) == 1:
                    if type(key) == list:
                        t_ = DataFrame()
                        for k in key:
                            DataFrame.__setattr__(t_,k,self.d[k])
                        return t_
                    else:
                        return self.d[key]
                else:
                    t_ = DataFrame()
                    for k in key:
                        DataFrame.__setattr__(t_,k,self.d[k])
                    return t_
    def __setitem__(self,key,values):
        DataFrame.__setattr__(self,key,values)

    def shape(self):
        return self.ncol,self.nrow

    def sort(self,order):
        for k in self.d.keys():
            self.d[k] = self.d[k][order]

    def sort_by_column(self,name):
        order = np.argsort(self.d[name])
        self.sort(order)
    def temp_sort_by_column(self,name):
        order = np.argsort(self.d[name])
        super(DataFrame, self).__setattr__('order_', order[order])
        self.sort(order)
    def unsort_temp_order(self):
        self.sort(self.order_)

    def groups(self,keys):
        # create a test array
        records_array = self.d[keys]

        # creates an array of indices, sorted by unique element
        idx_sort = np.argsort(records_array)

        # sorts records array so all unique elements are together
        sorted_records_array = records_array[idx_sort]

        # returns the unique values, the index of the first occurrence of a value, and the count for each element
        vals, count = np.unique(sorted_records_array, return_counts=True)

        # splits the indices into separate arrays
        res = np.split(idx_sort, idx_start[1:])
        return res
    def aggregate(self,columns,key,function):
        clusters = ordered_clusters_group_by(self.d[key],nb.typeof(self.d[key][0]))
        values = npg.aggregate(clusters[1],self.d[columns],func = function)
        t_ = DataFrame()
        t_.key = clusters[0]
        t_.values = values
        return t_

    def names(self):
        return self.d.keys()
    
    def read_pandas(self,df):
        t = DataFrame()
        names = df.columns
        for name in names:
            t[name] = df[name].values
        return t
    
    def to_pandas(self):
        df = pd.DataFrame()
        for k in self.d.keys():
            df[k] = self.d[k]
        return df
