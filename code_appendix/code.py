# coding: utf-8

# In[70]:

fa = [l.split(',') for l in open("../data/data_US/FlowUS_customers_SU_all.csv").read().split("\r")]
fb = [l.split(',') for l in open("../data/data_US/Supplier_US_business_SU.csv").read().split("\r")]


# In[70]:




# In[71]:

header1 = fa[0]
print header1, "total records", len(fa[1:])
header2 = fb[0]
print header2, "total records", len(fb[1:])
fa = [{k:v for k, v in zip(header1, line)} for line in fa[1:]]
fb = [{k:v for k, v in zip(header2, line)} for line in fb[1:]]


# In[72]:

def get_edges(data, key, value):
    edges = {}
    for row in data:
        k = key(row)
        if k not in edges:
            edges[k] = 0
        edges[k] += value(row)
    return edges


# In[73]:

A_B = get_edges(fa, key=lambda r: (r['Sold-to party Descr'], r['Mixing Center']), value=lambda r: float(r['Sum of Shipment Count (COF %) (SUM)']))
B_C = get_edges(fb, key=lambda r: (r['Mixing Center'], r['Business']), value=lambda r: float(r['shipments']))
C_D = get_edges(fb, key=lambda r: (r['Business'], r['Plant']), value=lambda r: float(r['shipments']))
print len(A_B), len(B_C), len(C_D)


# In[74]:

#sanity checks
assert(len([k for k in A_B if k in B_C]) == 0)
assert(len([k for k in B_C if k in A_B]) == 0)
assert(len([k for k in A_B if k in C_D]) == 0)
assert(len([k for k in C_D if k in A_B]) == 0)
assert(len([k for k in B_C if k in C_D]) == 0)
assert(len([k for k in C_D if k in B_C]) == 0)


# In[75]:

#merge 
temp_edges = {}
temp_edges.update(A_B)
temp_edges.update(B_C)
temp_edges.update(C_D)
print len(temp_edges)


# In[76]:

nodes = set()
for u, v in temp_edges:
    nodes.add(u)
    nodes.add(v)
nodes = {node_name: node_index for node_index, node_name in enumerate(nodes)}
nodes_id = {v:k for k, v in nodes.items()}
temp = []
for i in sorted(nodes_id.keys()):
    temp.append({"name":nodes_id[i], "index": i})
print {'nodes': temp}


# In[77]:

edges = []
for (x, y), v in temp_edges.items():
     edges.append({"source": nodes[x],"target":nodes[y],"value":round(v,3)})
print edges


# In[ ]:
