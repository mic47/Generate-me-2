class Graph:
    
    def __init__(self, sentences):
        self.vertices = list()
        self.ref = dict()
        self.edges = list()
        for sentence in sentences:
            self.getVertexId(sentence.lower(), "original")
    
    def getVertexId(self, sentence, tp="internal"):
        if sentence not in self.ref:
            newID = len(self.vertices)
            self.vertices.append((sentence, tp))
            self.ref[sentence] = newID
        return self.ref[sentence]
    
    def getVertex(self, ID):
        return self.vertices[ID]
            
    def addEdge(self, fr, to, distance):
        self.edges.append((fr, to, distance))
        
    def write(self, fp):
        fp.write("digraph G{\n")
        
        for ID in range(len(self.vertices)):
            se = self.vertices[ID][0]
            tp = self.vertices[ID][1]
            if tp == "original":
                tp = "house"
            else:
                tp = "rectangle"
            fp.write("""
                node [shape = {tp}]; L{ID} [shape = {tp}, label="{label}"];
            """.format(tp=tp, ID=ID, label=se.replace(chr(28), "*").replace(chr(29), "+")))
        for (fr, to, dist) in self.edges:
            fp.write("""
                L{fr} -> L{to} [label="{dist}"];
            """.format(fr=fr, to=to, dist=dist))
        fp.write("}\n")
        
    def getIDs(self):
        return [x for x in range(len(self.vertices))]
    
    def getAllInternalNodes(self):
        return [x for (x, tp) in self.vertices if tp == "internal"]
