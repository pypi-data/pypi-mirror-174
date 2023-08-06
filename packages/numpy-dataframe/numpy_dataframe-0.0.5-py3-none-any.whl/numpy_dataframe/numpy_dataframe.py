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
        super(DataFrame, self).__setattr__('shape', (0,0))
        super(DataFrame, self).__setattr__('columns', [])
    def __repr__(self):
        df = DataFrame.to_pandas(self)
        return df.__repr__()
    def __str__(self):
        df = DataFrame.to_pandas(self)
        return df.__repr__()
    def __getattr__(self, key):        
        return self.d[key]
    def __setattr__(self, name, value):
        if type(value) == list:
            value = np.array(value)        
        self.d[name] = value
        self.names()
        super(DataFrame, self).__setattr__('ncol', len(self.d.keys()))
        if self.nrow == 0:
            super(DataFrame, self).__setattr__('nrow', len(value))
        super(DataFrame, self).__setattr__('shape', (len(self.d[list(self.d.keys())[0]]),len(self.d.keys())))
    def __getitem__(self,args):
        if type(args) == tuple:
            rows,key=args
            if type(key) == slice:
                
                if key.start is None:
                    start = 0
                else:
                    start = key.start
                if key.stop is None:
                    stop = len(self.d.keys())
                else:
                    stop = key.stop
                if key.step is None:
                    step = 1                    
                else:
                    step = key.step
                return DataFrame.__getitem__(self,(rows,range(start,stop,step)))
            else:
                if type(key) == str:
                    return self.d[key][rows]
                else:
                    if type(key) == list or type(key) == np.array or type(key) == range:                    
                            t_ = DataFrame()
                            for k in key:
                                if type(k) == int:
                                    k = list(self.d.keys())[k]
                                DataFrame.__setattr__(t_,k,self.d[k][rows])
                            return t_
                    elif type(key) == int:
                        k = list(self.d.keys())[key]
                        return self.d[k][rows]
        else:
            key = args
            if type(key) == slice:
                if key.start is None:
                    start = 0
                else:
                    start = key.start
                if key.stop is None:
                    stop = len(self.d.keys())
                else:
                    stop = key.stop
                if key.step is None:
                    step = 1                    
                else:
                    step = key.step                
                return DataFrame.__getitem__(self,(rows,range(start,stop,step)))
            else:
                if type(key) == str:
                    return self.d[key]
                else:
                    if type(key) == list or type(key) == np.array or type(key) == range:                    
                            t_ = DataFrame()
                            for k in key:
                                if type(k) == int:
                                    k = list(self.d.keys())[k]
                                DataFrame.__setattr__(t_,k,self.d[k])
                            return t_
                    elif type(key) == int:
                        k = list(self.d.keys())[key]
                        return self.d[k]
    def __setitem__(self,args,values):
        if type(args) == tuple:
            rows,key = args
            if type(key) == str or type(key) == int:
                if type(key) == int:
                    key = list(self.d.keys())[key]
                self.d[key][rows] = values
            else:
                if type(key) == slice:
                    if key.step is not None:
                        return DataFrame.__setitem__(self,(rows,range(key.start,key.stop,key.step)))
                    else:
                        return DataFrame.__setitem__(self,(rows,range(key.start,key.stop)))
                else:
                    if len(key) == 1:                    
                        for k in key:
                            if type(k) == int:
                                k = list(self.d.keys())[k]
                            self.d[k][rows] = values
                    else:
                        raise Exception("Cannot set more than row")
        else:
            if type(args) == str or type(args) == int:
                if type(args) == int:
                    key = list(self.d.keys())[args]
                DataFrame.__setattr__(self,args,values)
            else:
                if len(args) == 1:
                    for k in args:
                        if type(k) == int:
                            k = list(self.d.keys())[k]
                        self.d[k] = values
                else:
                    raise Exception("Cannot set more than row")

        self.names()
    
    def rename(self,keys,new_keys):

        new_d = {}
        if type(keys) == str or type(keys) == int:
            if type(keys) == int:
                keys = [self.columns[keys]]
            else:
                keys = [keys]
        else:
            keys_ = []
            for k in keys:
                if type(k) == int:
                    k = self.columns[k]
                keys_.append(k)
            keys = keys_
        if type(new_keys) == str:
            new_keys = [new_keys]
        
        failed = False
        for name in self.columns:
            if name in keys:
                
                index = int(np.where(np.array(keys) == name)[0][0])
                if not new_keys[index] in self.columns or new_keys[index] == name:
                    new_d[new_keys[index]] = self.d[name]
                else:
                    failed = True
                    print("Keys not unique. This operation would delete an existing column, aborting")
                    break
                    
            else:
                new_d[name] = self.d[name]
        if not failed:
            super(DataFrame, self).__setattr__('d', new_d)
            self.names()

    def __shape__(self):
        if len(self.d.keys()) > 0:
            shape = (len(self.d[list(self.d.keys())[0]]),len(self.d.keys()))
        else:
            shape = (0,0)
        
        return shape

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
        # self.columns = list(self.d.keys())
        super(DataFrame, self).__setattr__('columns', list(self.d.keys()))
        return self.columns
    
    def from_pandas(self,df):                  
        for name in df.columns:
            DataFrame.__setattr__(self,name , df[name].values)
    
    def to_pandas(self):
        df = pd.DataFrame()
        for k in self.d.keys():
            df[k] = self.d[k]
        
        return df

    def to_csv(self,path):
        df = self.to_pandas()
        df.to_csv(path,index = False)
    
    def read_csv(self,path):
        df = pd.read_csv(path)
        return self.from_pandas(df)

def from_pandas(df):                  
    t = DataFrame()
    for name in df.columns:
        t[name] = df[name].values
    return t

def read_csv(path):
    df = pd.read_csv(path)
    return from_pandas(df)