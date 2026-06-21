import flet as ft

from model.nerc import Nerc


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._idMap = {}
        self.fillIDMap()
        self.max_anni = 0
        self.max_ore = 0

    def handleWorstCase(self, e):
        self._view._txtOut.controls.clear()

        X = self._view._txtYears.value
        Y = self._view._txtHours.value
        if X is None or X == "" or Y is None or Y == "":
            self._view.create_alert("Inserire un un numero massimo di anni in cui si sono verificati blackout e un numero massimo di ore")
            return
        self._model.loadEvents(self._view._ddNerc.value)#carico tutti i blackout di quel nerc che ho scelto
        self.max_anni = int(X)
        self.max_ore = int(Y)

        """selezionare il sottoinsieme di eventi di blackout (tabella ‘PowerOutages’) che si sono verificati in un
massimo di X anni, per un totale di Y ore di disservizio massimo, tale da massimizzare il numero
totale di persone coinvolte."""
        insieme, n_coinvolti, actual_hours = self._model.getInsiemeOttimo(self.max_anni, self.max_ore)
        self._view._txtOut.controls.append(ft.Text(f"Tot people affected: {n_coinvolti}"))
        self._view._txtOut.controls.append(ft.Text(f"Tot hours of outgages: {actual_hours}"))
        for e in insieme:
            self._view._txtOut.controls.append(ft.Text(f"id={e.id}, customer_affected={e.customers_affected}, start_time={e.date_event_began}, end_time={e.date_event_finished}"))

        self._view.update_page()


    def fillDD(self):
        nercList = self._model.listNerc

        for n in nercList:
            self._view._ddNerc.options.append(ft.dropdown.Option(
                text=str(n),  # Visualizza il nome (toString dell'oggetto)
                key=(n.id)
            ))
        self._view.update_page()

    def fillIDMap(self):
        values = self._model.listNerc
        for v in values:
            self._idMap[v.value] = v
