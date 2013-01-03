from collections import defaultdict
from algorithm import entropy
import math
import Queue
import json


class Vertex:
    def __init__(self, Id, sentence, tp="internal", memes=defaultdict(int)):
        self.sentence = sentence
        self.tp = tp
        self.memes = defaultdict(int)
        for (k, v) in memes.iteritems():
            self.memes[k] = v
        self.edges = list()
        self.id = Id
        
    def addEdge(self, where, distance):
        self.edges.append((where, distance))
    
    
    def addMemes(self, memes):
        for (k, v) in memes.iteritems():
            self.memes[k] += v


class Graph:    
    
    def __init__(self, sentences):
        self.vertices = list()
        self.ref = dict()
        self.edges = list()
        self.ue = set()
        for kk in sentences:
            if type(kk) == tuple:
                sentence, memetype = kk
            else:
                sentence, memetype = (kk, "")
            d = defaultdict(int)
            d[memetype] = 1
            self.getVertexId(sentence.lower(), "original", d)
    
    def getVertexId(self, sentence, tp="internal", memes=defaultdict(int)):
        if sentence not in self.ref:
            newID = len(self.vertices)
            V = Vertex(newID, sentence, tp, memes)
            self.vertices.append(V)
            self.ref[sentence] = newID
        else:
            V = self.vertices[self.ref[sentence]]
            for (k, v) in memes.iteritems():
                V.memes[k] += v
        return self.ref[sentence]
    
    def getVertex(self, ID):
        return self.vertices[ID]
            
            
    def addEdge(self, fr, to, distance):
        if (fr, to) in self.ue:
            return
        self.ue.add((fr, to))
        self.edges.append((fr, to, distance))
        self.vertices[fr].addEdge(to, distance)
    
    
    def getTopologicalOrder(self):
        order = list()
        was = [False] * len(self.vertices)
        def __topo(v):
            if was[v]:
                return
            was[v] = True
            e = self.vertices[v].edges
            for (where, _) in e:
                __topo(where)
            order.append(v)
                        
        for i in range(len(self.vertices)):
            __topo(i)
        return list(reversed(order))
    
    
    def memeClosure(self):
        for fr in self.getTopologicalOrder():
            d = self.vertices[fr].memes
            #print(fr, d, self.vertices[fr].sentence)
            if len(d) <= 0:
                continue
            for (to, _) in self.vertices[fr].edges:
                if to == fr:
                    continue
                self.vertices[to].addMemes(d)
       
    
    def writeAsJSON(self, fp):
        J = {}
        J["root"] = self.getVertexId("")
        J["graph"] = {}
        G = J["graph"]
    
        G["vertices"] = []
        G["edges"] = defaultdict(list)
        G["reverseEdges"] = defaultdict(list)
        V = G["vertices"]
        E = G["edges"]
        RE = G["reverseEdges"]
        for ID in range(len(self.vertices)):
            se = self.vertices[ID].sentence
            try: 
                se.decode("utf_8")
            except UnicodeDecodeError:
                print("Ignoring: ", se)
                se = "ERROR: not valid utf-8 string" 
            memes = self.vertices[ID].memes
            e = 0.0
            if len(memes) >= 2:
                e = entropy([v for (_, v) in memes.iteritems()]) / math.log(len(memes))
            V.append({
                "id": str(ID),
                "entropy": e,
                "sentence": se,
                "maps": memes
            })
        for (fr, to, dist) in self.edges:
            E[fr].append({"to": to, "dist": dist})
            RE[to].append({"to": fr, "dist": dist})
        json.dump(J, fp, indent=1)
    
        
    def write(self, fp):
        fp.write("digraph G{\n")
        
        for ID in range(len(self.vertices)):
            se = self.vertices[ID].sentence
            tp = self.vertices[ID].tp
            memes = self.vertices[ID].memes
            if len(memes) < 2:
                color = "red"
            else:
                e = entropy([v for (_, v) in memes.iteritems()]) / math.log(len(memes))
                c = hex(int((1 - e) * 255))[2:]
                if len(c) == 1:
                    c = "0" + c
                color = "#{0}ffff".format(c)
            if tp == "original":
                tp = "house"
            else:
                tp = "rectangle"
            label = se.replace(chr(28), "*").replace(chr(29), "+")
            #if len(memes) > 0:
            #    label += " | " + str(memes)
            fp.write("""
                node [shape = {tp}]; L{ID} [shape = {tp}, label="{label}", fillcolor="{color}", style=filled];
            """.format(tp=tp, ID=ID, label=label,
                       color = color ))
        for (fr, to, dist) in self.edges:
            fp.write("""
                L{fr} -> L{to} [label="{dist}"];
            """.format(fr=fr, to=to, dist=dist))
        fp.write("}\n")
        
    def getIDs(self):
        return [x for x in range(len(self.vertices))]
    
    def getAllInternalNodes(self):
        return [x.tp for x in self.vertices if x.tp == "internal"]
