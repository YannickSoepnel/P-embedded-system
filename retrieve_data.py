from connection import Connectie


class ReadData:
    temperatuur_data = []
    licht_data = []
    afstand_data = []
    count_data_afstand = []
    count_data_licht = []
    count_data_temperatuur = []
    count = 0

    def __init__(self):
        pass

    def update_data(self):
        data = Connectie.data_licht(Connectie)      # Zet seriële waarde in data
        if data == 0xf0:                            # Check of de data 0x0f is
            data = Connectie.data_licht(Connectie)  # Zet seriële waarde na de 0xff in data
            self.afstand_data.append(data)          # Voeg data toe in de afstand lijst
            self.count_data_afstand.append(self.count)
        data = Connectie.data_licht(Connectie)
        if data == 0x0f:                            # Check of de data 0x0f is
            data = Connectie.data_licht(Connectie)  # Zet seriële waarde na de 0x0f in data
            self.licht_data.append(data)            # Voeg data toe in de lichtintensiteit lijst
            self.count_data_licht.append(self.count)
        data = Connectie.data_temp(Connectie)
        if data == 0xff:                            # Kijk of de data 0xff is
            data = Connectie.data_temp(Connectie)   # Zet seriële waarde na 0xff in data
            data = data / 10                        # Deel de data door 10 omdat hij vanuit de arduino met 10 is vermenigvuldigd
            self.count_data_temperatuur.append(self.count)
            self.temperatuur_data.append(data)      # Voeg de data toe in de temperatuur lijst
            self.count += 1