class IntegrationPoint:
    def __init__(self, ksi: float, eta: float):
        self.ksi = ksi
        self.eta = eta
        self.nShape = []
        self.dNdKsi = []
        self.dNdEta = []

    def calculateShape(self):
        N1 = 0.25 * (1 - self.ksi) * (1 - self.eta)
        N2 = 0.25 * (1 + self.ksi) * (1 - self.eta)
        N3 = 0.25 * (1 + self.ksi) * (1 + self.eta)
        N4 = 0.25 * (1 - self.ksi) * (1 + self.eta)
        
        self.nShape = [N1, N2, N3, N4]   
    
    def calculateNdEta(self):
        N1 = -0.25 * (1 - self.eta)
        N2 = 0.25 * (1 - self.eta)
        N3 = 0.25 * (1 + self.eta)
        N4 = -0.25 * (1 + self.eta)

        self.dNdEta = [N1, N2, N3, N4]   

    def calculateNdKsi(self):
        N1 = -0.25 * (1 - self.ksi)
        N2 = -0.25 * (1 + self.ksi)
        N3 = 0.25 * (1 + self.ksi)
        N4 = 0.25 * (1 - self.ksi)

        self.dNdKsi = [N1, N2, N3, N4]   

    def __str__(self) -> str:
        return f'--Integration Point-- \n ksi: {self.ksi}, eta: {self.eta} N: {self.nShape}, dNdKsi: {self.dNdKsi}, dNdEta: {self.dNdEta}\n'
    
    def __repr__(self):
        return str(self)