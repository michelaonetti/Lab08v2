import copy

from database.DAO import DAO


class Model:
    def __init__(self):
        self._solBest = []
        self._listNerc = self.loadNerc()
        self._listEvents = []
        self.bestPath = []
        self.bestscore= 0
        self.actual_hours = 0





    def worstCase(self, nerc, maxY, maxH):
        # TO FILL
        pass
    def ricorsione(self, parziale, maxY, maxH, pos):
        # TO FILL
        pass

    def loadEvents(self, nerc):
        self._listEvents = DAO.getAllEvents(nerc)

    def loadNerc(self):
        return sorted(DAO.getAllNerc(), key=lambda x: x.value)

    def getInsiemeOttimo(self, X, Y):
        self.bestPath = []
        self.bestscore = 0
        self.actual_hours=0

        parziale = []
        self._ricorsione(parziale, X,Y,0)
        return self.bestPath, self.bestscore, self.actual_hours

    """selezionare il sottoinsieme di eventi di blackout (tabella ‘PowerOutages’) che si sono verificati in un
massimo di X anni, per un totale di Y ore di disservizio massimo, tale da massimizzare il numero
totale di persone coinvolte."""
    def _ricorsione(self, parziale, maxAnni, maxOre, livello):
        #non deve essere di un numero preciso
        if livello >= len(self._listEvents):
            #ho girato tutte le possibilità
            actual_score = self.actual_score_function(parziale)
            if actual_score > self.bestscore:
                self.bestscore= actual_score
                self.bestPath = copy.deepcopy(parziale)
                ore_totali = 0
                for e in self.bestPath:
                    delta = e.date_event_finished - e.date_event_began
                    ore_totali += delta.total_seconds() / 3600
                self.actual_hours = ore_totali
            return

        for e in self._listEvents[livello:]:
            parziale.append(e)
            if self.is_admissible(parziale, maxAnni, maxOre):
                self._ricorsione(parziale, maxAnni, maxOre, self._listEvents.index(e)+1)
            parziale.pop()

    def actual_score_function(self, parziale):
        #for evento in parziale, faccio la somma di tutti i coinvolti
        sum =0
        for e in parziale:
            sum += e.customers_affected
        return sum


    def is_admissible(self,parziale, maxAnni, maxOre):
        #controllo che i vicnoli del massimo di x e y siano rispettati
        ore = 0
        grande = 0
        piccolo =float('inf')
        for e in parziale:
            delta = e.date_event_finished - e.date_event_began
            ore += delta.total_seconds() / 3600  # Converti in ore
            if e.date_event_began.year> grande :
                grande =e.date_event_began.year
            elif e.date_event_began.year< piccolo :
                piccolo =e.date_event_began.year
        anni = grande- piccolo + 1 #altrimenti non considera gli estremi e quindi mi taglia un anno
        if anni <= maxAnni  and (ore) <= maxOre:
            return True
        return False






    @property
    def listNerc(self):
        return self._listNerc