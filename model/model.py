from database.distributore_DAO import DistributoreDAO

'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class Model:
    def __init__(self):
        self._distributori = None
        self.load_distributori()

        self.__sequenza_ottima = []
        self.__costo_ottimo = -1

    def load_distributori(self):
        """ Carica tutti i distributori e li setta nella variabile self._distributori """
        self._distributori = DistributoreDAO.get_distributori()

    def get_prezzo_medio(self, mese:int):
        """
        Calcola, per ogni distributore, il prezzo medio al litro per il mese selezionato.
        :param mese: Mese selezionato (un intero da 1 a 12)
        :return: lista di tuple --> (nome del distributore, media), es. (Distributore A, 1.789)
        """
        # TODO
        self._lista_media = []
        somma = 0
        n=0
        for distributore in self._distributori:
            lista_prezzi_stesso_id = distributore.get_prezzi()
            for i in lista_prezzi_stesso_id:
                if int(i.data.month) == mese:
                    somma = somma + i.prezzo_litro
                    n += 1
            media = (somma / n)
            self._lista_media.append((distributore.nome, media))
        return self._lista_media

    def get_sequenza_ottima(self, mese:int):
        """
        Calcola la sequenza ottimale di rifornimenti nei primi 7 giorni
        :return: sequenza di nomi distributore ottimale
        :return: costo ottimale (cioè quello minimizzato dalla sequenza scelta)
        """
        self.__sequenza_ottima = []
        self.__costo_ottimo = -1
        prezzi_settimana = self.__get_prezzi_prima_settimana_mese(mese)

        self.__ricorsione([], 1, None, 0, prezzi_settimana)

        # Traduci gli ID in nomi
        id_to_nome = {distributore.id: distributore.nome for distributore in self._distributori}
        sequenza_nomi = [f"Giorno {giorno}: {id_to_nome[i]}" for giorno, i in enumerate(self.__sequenza_ottima, start=1)]
        return sequenza_nomi, round(self.__costo_ottimo, 2)

    def __ricorsione(self, sequenza_parziale, giorno, ultimo_distributore, costo_corrente, prezzi_settimana):
        """ Implementa la ricorsione """
        # TODO
        if giorno == 8:
            if self.__costo_ottimo == -1 or costo_corrente<self.__costo_ottimo:
                self.__sequenza_ottima = list(sequenza_parziale)
                self.__costo_ottimo = costo_corrente
                return

        for k,p in prezzi_settimana.items():
            costo_giorno = p[giorno-1] * 100
            if giorno > 1 and k != ultimo_distributore:
                costo_giorno = costo_giorno+5
            if self.__costo_ottimo==-1 or costo_corrente + costo_giorno < self.__costo_ottimo:
                sequenza_parziale.append(k)
                self.__ricorsione(sequenza_parziale, giorno+1 , k, costo_corrente+costo_giorno, prezzi_settimana)
                sequenza_parziale.pop()

    def __get_prezzi_prima_settimana_mese(self, mese: int):
        """
        Restituisce i prezzi dei primi 7 giorni del mese selezionato per ciascun distributore.
        :return: un dizionario: {id_distributore: [prezzo_giorno1, ..., prezzo_giorno7]}
        """
        # TODO
        self._dizio = {}
        for distributore in self._distributori:
            self._dizio[distributore.id] = []
            lista_p=distributore.get_prezzi()
            for p in lista_p:
                if int(p.data.month) == mese and 1<=int(p.data.day) <= 7:
                    self._dizio[distributore.id].append(p.prezzo_litro)
        return self._dizio