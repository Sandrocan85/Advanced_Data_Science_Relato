import pandas as pd
import csv

# Initializing general variables
address="csv/"
name=" Overtakes - Sheet1.csv"
years=range(1994, 2021)
nodes=[]
nodes_set=set()
edges=[]
edges_set=set()
datasets={}

# Import the csv files
for year in years:
    datasets[year]=pd.read_csv(address+str(year)+name, delimiter=",")

a=input("generale or yearly? (g/y) ")
if a=="g":
    # Creation of nodes and edges of the graph
    for dataset in datasets.values():
        for riga in dataset.itertuples():
            # Extracting usefull data
            overtaker=riga.Overtaker
            overtakee=riga.Overtakee
            # Adding nodes
            if overtaker not in nodes_set:
                nodes_set.add(overtaker)
                nodes.append({"name": overtaker})
            if overtakee not in nodes_set:
                nodes_set.add(overtakee)
                nodes.append({"name": overtakee})
            # Adding edges
            if (overtaker, overtakee) not in edges_set:
                edges_set.add((overtaker, overtakee))
                edges.append({"from": overtaker,
                           "to": overtakee,
                           "weight": 1})
            else:
                for edge in edges:
                    if edge["from"]==overtaker and edge["to"]==overtakee:
                        edge["weight"]+=1
    # Saving nodes and edges files
    with open("nodes.csv", "w", newline='', encoding="utf-8") as file:
        writer=csv.DictWriter(file, fieldnames=["name"])
        writer.writeheader()
        writer.writerows(nodes)
    with open("edges.csv", "w", newline='', encoding="utf-8") as file:
        writer=csv.DictWriter(file, fieldnames=["from", "to", "weight"])
        writer.writeheader()
        writer.writerows(edges)
elif a=="y":
    # Creation of nodes and edges of the graph
    for year, dataset in datasets.items():
        nodes=[]
        nodes_set=set()
        edges=[]
        edges_set=set()
        for riga in dataset.itertuples():
            # Extracting usefull data
            overtaker=riga.Overtaker
            overtakee=riga.Overtakee
            # Adding nodes
            if overtaker not in nodes_set:
                nodes_set.add(overtaker)
                nodes.append({"Name": overtaker})
            if overtakee not in nodes_set:
                nodes_set.add(overtakee)
                nodes.append({"Name": overtakee})
            # Adding edges
            if (overtaker, overtakee) not in edges_set:
                edges_set.add((overtaker, overtakee))
                edges.append({"Overtaker": overtaker,
                           "Overtakee": overtakee,
                           "Weight": 1})
            else:
                for edge in edges:
                    if edge["Overtaker"]==overtaker and edge["Overtakee"]==overtakee:
                        edge["Weight"]+=1
            # Saving nodes and edges files
            with open("yearly/"+str(year)+" nodes.csv", "w", newline='', encoding="utf-8") as file:
                writer=csv.DictWriter(file, fieldnames=["Name"])
                writer.writeheader()
                writer.writerows(nodes)
            with open("yearly/"+str(year)+" edges.csv", "w", newline='', encoding="utf-8") as file:
                writer=csv.DictWriter(file, fieldnames=["Overtaker", "Overtakee", "Weight"])
                writer.writeheader()
                writer.writerows(edges)