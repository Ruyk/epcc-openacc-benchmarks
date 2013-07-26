import numpy as np
import matplotlib.pyplot as plt

level_0 = ['ContigH2D', 'ContigD2H', 'SlicedD2H', 'SlicedH2D', 'Kernels_If', 'Parallel_If', 'Parallel_private', 'Parallel_1stprivate', 'Kernels_combined', 'Parallel_combined', 'Update_Host', 'Kernels_Invocation', 'Parallel_Invocation', 'Parallel_Reduction', 'Kernels_Reduction',]
 
level_1 = ['2MM','3MM','ATAX', 'MVT','SYRK','COV','COR','GESUMMV','GEMM','2DCONV',]

level_2 = ['27S',]

# The following list of kernels does not compute time but difference between two different syntax

diff = ['Kernels_combined', 'Kernels_If', 'Parallel_If', 'Parallel_private', 'Parallel_1stprivate', 'Parallel_Reduction', 'Kernels_Reduction', 'Update_Host', 'Kernels_Invocation', 'Parallel_Invocation',]


labels = ('1','2','4','8','16','32','64','128','256','512','1024')

all_levels = level_0  + level_1 + level_2
        
with open("time") as f:
    data = f.read()

data = data.split('\n')

x = []
y = {}
y_d = {}
y_l1 = {}

for key in level_0:
   if not key in diff:
      y[key] = []
   else:
      y_d[key] = []

for key in level_1:
   y_l1[key] = []

for row in data:
   elems = row.split()
   if len(elems) < 5:
      continue
   b = int(elems[2])
   if not b in x:
      x.append(b)
   if elems[1] in y.keys():
      y[elems[1]].append(elems[3])
   elif elems[1] in y_d.keys():
      y_d[elems[1]].append(elems[3])
   elif elems[1] in y_l1.keys():
      y_l1[elems[1]].append(elems[3])
      


print str(x)

ds = np.zeros( (len(x),1) )
datasizes = sorted(x)
print datasizes
for i in range(0,len(datasizes)):
     ds[i][0] = int(datasizes[i])

ds2 = np.log(ds)/np.log(2)

args_l0 = []
for elem in y.keys():
   times = np.zeros( (len(datasizes),1) )
   for i in range(0, len(y[elem])):
      times[i][0] = y[elem][i]
   args_l0 += [ ds2, times, '-', ]

if np.amax(times) > 1000:
   times = times / 1000
   unit = r'$ms$'


if np.amax(times) > 1000000:
   times = times / 1000000
   unit = r'$s$'  


fig, axs = plt.subplots(2, 1, sharex=False, sharey=False)
fig.set_size_inches(10,10)

ax1 = axs[0]
ax1.set_title("Level 0 - Execution times")    
ax1.semilogy(*args_l0, linewidth=2)

leg = ax1.legend()

locs = ax1.get_xticks()
lmax = max(locs)+1
lmin = min(locs)
# print "min %d  max %d "%(lmin,lmax)
# print " arange %s"%(np.arange(lmin,lmax))
ax1.set_xticks(np.arange(lmin,lmax))
ax1.set_xticklabels(labels)
xmin,xmax = ax1.get_xlim()
ax1.set_xlim(xmin*0.99,xmax*1.01)
ax1.set_ylabel('Run time (' + unit + ')')
ax1.set_xlabel('Size (MB)')

args_diff = []
for elem in y_l1.keys():
   times = np.zeros( (len(datasizes),1) )
   for i in range(0, len(y_l1[elem])):
      times[i][0] = y_l1[elem][i]
   args_diff += [ ds2, times, '-', ]

if np.amax(times) > 1000:
   times = times / 1000
   unit = r'$ms$'


if np.amax(times) > 1000000:
   times = times / 1000000
   unit = r'$s$'  

ax2 = axs[1]
ax2.set_title("Level 1 - Execution times ")    
ax2.semilogy(*args_diff, linewidth=2)

locs = ax2.get_xticks()
lmax = max(locs)+1
lmin = min(locs)
# print "min %d  max %d "%(lmin,lmax)
# print " arange %s"%(np.arange(lmin,lmax))
ax2.set_xticks(np.arange(lmin,lmax))
ax2.set_xticklabels(labels)
xmin,xmax = ax2.get_xlim()
ax2.set_xlim(xmin*0.99,xmax*1.01)
ax2.set_ylabel('Run time (' + unit + ')')

ax1.legend(level_0, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
ax2.legend(level_1, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
ax2.set_xlabel('Size (MB)')

#plt.show()
plt.savefig('results.png', bbox_inches='tight', pad_inches=1) # dpi=600)
