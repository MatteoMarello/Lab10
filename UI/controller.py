import flet as ft
from model import model
from UI import view

class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model
        self._currentCountry = None

    def handleCalcola(self, e):
        anno = self._view._txtAnno.value
        if not anno.isdigit():
            self._show_error("Please provide a valid year.")
            return

        self._model.buildGraph(int(anno))
        self._fillDD()

        gradi = self._model.getGradoStati()
        comp = self._model.getNumComponentiConnesse()
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Componenti connesse: {comp}"))
        for nome, grado in gradi:
            self._view._txt_result.controls.append(ft.Text(f"{nome}: {grado} vicini"))
        self._view.update_page()

    def handleCalcolaComponenteConnessa(self, e):
        anno = self._view._txtAnno.value
        if not anno.isdigit():
            self._show_error("Please provide a valid year.")
            return

        # Se _currentCountry è None, prova a leggerlo dal valore attuale del dropdown
        if not self._currentCountry:
            selected_value = self._view._DDstato.value  # restituisce il testo (nome dello stato)
            for option in self._view._DDstato.options:
                if option.text == selected_value:
                    self._currentCountry = option.data
                    break

        if not self._currentCountry:
            self._show_error("Seleziona prima uno stato dal dropdown.")
            return

        self._model.buildGraph(int(anno))
        connessi = self._model.getNodiConnessi(self._currentCountry.StateNme)
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(
            ft.Text(f"Dallo stato {self._currentCountry.StateNme} puoi andare via terra in:")
        )
        for stato in connessi:
            self._view._txt_result.controls.append(ft.Text(stato.StateNme))
        self._view.update_page()

    def _fillDD(self):
        # Popola in un colpo solo
        self._view._DDstato.options = [
            ft.dropdown.Option(text=c.StateNme, data=c)
            for c in self._model.getNodes()
        ]
        # Aggiorna _currentCountry al cambio
        self._view._DDstato.on_change = lambda e: setattr(self, "_currentCountry", e.control.data)
        self._view.update_page()

    def _show_error(self, msg: str):
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(msg))
        self._view.update_page()
