from datetime import datetime
from database.DAO import DAO
import networkx as nx

from model import arco


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._idMapCountries = DAO.getAllNodes()

    def buildGraph(self, anno_selezionato):
        self._grafo.clear()

        # Aggiungi TUTTI i nodi (paesi) prima degli archi
        for country in self._idMapCountries.values():
            self._grafo.add_node(country)

        # Poi aggiungi gli archi
        self.addEdges(anno_selezionato)

    def addEdges(self, anno_selezionato):
        """
        faccio una query unica che prende tutti gli archi, e poi ciclo qui.
        Returns:

        """
        allEdges = DAO.getArchi(anno_selezionato)
        for arco in allEdges:
            u = self._idMapCountries[arco.CCode1]
            v = self._idMapCountries[arco.CCode2]
            self._grafo.add_edge(u, v)

    def getNumNodi(self):
        return len(self._grafo.nodes)

    def getNumArchi(self):
        return len(self._grafo.edges)

    def getGradoStati(self):
        # Ottieni la lista di tuple (nome_stato, grado)
        gradi = [(nazione.StateNme, self._grafo.degree[nazione]) for nazione in self._grafo.nodes]

        # Ordina alfabeticamente per nome dello stato
        gradi_ordinati = sorted(gradi, key=lambda x: x[0])

        return gradi_ordinati

    def getNumComponentiConnesse(self):
        return nx.number_connected_components(self._grafo)

    def getNodiConnessi(self, stato):
        for componente in nx.connected_components(self._grafo):
            if any(nazione.StateNme == stato for nazione in componente):
                return componente
        return []

    def getNodes(self):
        return self._grafo.nodes

