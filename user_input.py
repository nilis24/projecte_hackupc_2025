import json

class UserInput:
    def __init__(self, json_data):
        # Convertir string JSON a diccionari si es necessari
        if isinstance(json_data, str):
            data = json.loads(json_data)
        else:
            data = json_data
            
        # Informació Bàsica
        self.ubicacio = data.get('ubicacio', '')
        self.nacionalitat = data.get('nacionalitat', '')
        self.data_inici = data.get('data_inici', '')
        self.data_fi = data.get('data_fi', '')
        self.pressupost = data.get('pressupost', '')
        self.durada = data.get('durada', '')
        
        # Preferències Personals
        self.interessos = data.get('interessos', [])
        self.clima = data.get('clima', '')
        self.green_travel = data.get('green_travel', '')
        self.allotjament = data.get('allotjament', '')
        self.activitat_fisica = data.get('activitat_fisica', '')
        self.transport = data.get('transport', '')
        
        # Informació Addicional
        self.idiomes = data.get('idiomes', '')
        self.experiencia = data.get('experiencia', '')
        self.restriccions_alimentaries = data.get('restriccions_alimentaries', [])
        self.restriccions = data.get('restriccions', '')
        self.evitar = data.get('evitar', '')
        self.comentaris = data.get('comentaris', '')
    
    def to_dict(self):
        """Converteix l'objecte a un diccionari"""
        return {
            'ubicacio': self.ubicacio,
            'nacionalitat': self.nacionalitat,
            'data_inici': self.data_inici,
            'data_fi': self.data_fi,
            'pressupost': self.pressupost,
            'durada': self.durada,
            'interessos': self.interessos,
            'clima': self.clima,
            'green_travel': self.green_travel,
            'allotjament': self.allotjament,
            'activitat_fisica': self.activitat_fisica,
            'transport': self.transport,
            'idiomes': self.idiomes,
            'experiencia': self.experiencia,
            'restriccions_alimentaries': self.restriccions_alimentaries,
            'restriccions': self.restriccions,
            'evitar': self.evitar,
            'comentaris': self.comentaris
        }
    
    def to_json(self):
        """Converteix l'objecte a una cadena JSON"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)


