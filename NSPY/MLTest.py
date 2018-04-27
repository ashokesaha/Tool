from sklearn.datasets import load_iris
import numpy as np

data = load_iris()
features = data.data
feature_names = data.feature_names
target = data.target
target_names = data.target_names

t0idx = [target==0]
t1idx = [target==1]
t2idx = [target==2]
t3idx = [target==3]


c1_f1_min = features[t0idx][:,0].min()
c1_f1_max = features[t0idx][:,0].max()
c1_f2_min = features[t0idx][:,1].min()
c1_f2_max = features[t0idx][:,1].max()
c1_f3_min = features[t0idx][:,2].min()
c1_f3_max = features[t0idx][:,2].max()
c1_f4_min = features[t0idx][:,3].min()
c1_f4_max = features[t0idx][:,3].max()


c2_f1_min = features[t1idx][:,0].min()
c2_f1_max = features[t1idx][:,0].max()
c2_f2_min = features[t1idx][:,1].min()
c2_f2_max = features[t1idx][:,1].max()
c2_f3_min = features[t1idx][:,2].min()
c2_f3_max = features[t1idx][:,2].max()
c2_f4_min = features[t1idx][:,3].min()
c2_f4_max = features[t1idx][:,3].max()


c3_f1_min = features[t2idx][:,0].min()
c3_f1_max = features[t2idx][:,0].max()
c3_f2_min = features[t2idx][:,1].min()
c3_f2_max = features[t2idx][:,1].max()
c3_f3_min = features[t2idx][:,2].min()
c3_f3_max = features[t2idx][:,2].max()
c3_f4_min = features[t2idx][:,3].min()
c3_f4_max = features[t2idx][:,3].max()



print '{}    {}    {}    {}'.format(c1_f1_min,c1_f2_min,c1_f3_min,c1_f4_min)
print '{}    {}    {}    {}'.format(c1_f1_max,c1_f2_max,c1_f3_max,c1_f4_max)
print '\n\n'
print '{}    {}    {}    {}'.format(c2_f1_min,c2_f2_min,c2_f3_min,c2_f4_min)
print '{}    {}    {}    {}'.format(c2_f1_max,c2_f2_max,c2_f3_max,c2_f4_max)
print '\n\n'
print '{}    {}    {}    {}'.format(c3_f1_min,c3_f2_min,c3_f3_min,c3_f4_min)
print '{}    {}    {}    {}'.format(c3_f1_max,c3_f2_max,c3_f3_max,c3_f4_max)

