class HermiteInterpolation:
    def __init__(self):
        self.x_values = []
        self.f_values = []
        self.df_values = []
        self.z_values = []
        self.q_values = []

    def construct_table(self, n):
        """Construye la tabla de diferencias divididas de Hermite."""
        size = 2 * n
        self.z_values = []
        self.q_values = [[0] * size for _ in range(size)]

        # Duplicamos los valores para cada punto base
        for i in range(n):
            self.z_values.append(self.x_values[i])
            self.z_values.append(self.x_values[i])

        # Primera columna: valores de f(x)
        for i in range(size):
            self.q_values[i][0] = self.f_values[i // 2]

        # Segunda columna: valores de las derivadas
        for i in range(1, size):
            if i % 2 == 1:
                self.q_values[i][1] = self.df_values[i // 2]
            else:
                self.q_values[i][1] = (self.q_values[i][0] - self.q_values[i - 1][0]) / (self.z_values[i] - self.z_values[i - 1])

        # Resto de la tabla
        for j in range(2, size):
            for i in range(j, size):
                self.q_values[i][j] = (self.q_values[i][j - 1] - self.q_values[i - 1][j - 1]) / (self.z_values[i] - self.z_values[i - j])

    def get_polynomial(self):
        """Construye el polinomio de Hermite como una representación simplificada."""
        polynomial_terms = [f"{self.q_values[i][i]}" for i in range(len(self.z_values))]
        return " + ".join(polynomial_terms)