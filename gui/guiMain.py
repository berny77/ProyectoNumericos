import tkinter as tk
from modules.hermite import HermiteInterpolation

class GuiMain:
    def __init__(self, root):
        self.root = root
        self.root.title("Interpolación de Hermite")
        self.root.geometry("800x600")
        self.centrar_ventana(800, 600)

        # Variables para almacenar los valores ingresados
        self.num_puntos = tk.IntVar()
        self.x_values = []
        self.f_values = []
        self.df_values = []
        self.resultado = tk.StringVar()

        # Sección de título
        self.label_intro = tk.Label(root, text="Interpolación de Hermite", font=("Arial", 14))
        self.label_intro.pack(pady=10)

        # Entrada para número de puntos
        self.lbl_num_puntos = tk.Label(root, text="Cantidad de puntos base (ejemplo: 2 para x₀, x₁):")
        self.lbl_num_puntos.pack()
        self.entry_num_puntos = tk.Entry(root, textvariable=self.num_puntos)
        self.entry_num_puntos.pack()

        # Botón para generar entradas
        self.btn_generar = tk.Button(root, text="Generar Entradas", command=self.generar_campos)
        self.btn_generar.pack(pady=10)

        # Contenedor dinámico para las entradas
        self.frame_campos = tk.Frame(root)
        self.frame_campos.pack()

        # Botón de cálculo
        self.btn_calcular = tk.Button(root, text="Calcular Hermite", command=self.calcular_hermite)
        self.btn_calcular.pack(pady=10)

        # Etiqueta de resultado
        self.lbl_resultado = tk.Label(root, textvariable=self.resultado, wraplength=600, justify="left")
        self.lbl_resultado.pack(pady=10)

        # Frame para la tabla de resultados con botones
        self.frame_tabla = tk.Frame(root)
        self.frame_tabla.pack(pady=10)

    def centrar_ventana(self, ancho, alto):
        """Centra la ventana en la pantalla"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - ancho) // 2
        y = (screen_height - alto) // 2
        self.root.geometry(f"{ancho}x{alto}+{x}+{y}")

    def generar_campos(self):
        """Genera los campos de entrada para los valores de x, f(x) y f'(x)."""
        for widget in self.frame_campos.winfo_children():
            widget.destroy()

        self.x_values.clear()
        self.f_values.clear()
        self.df_values.clear()

        n = self.num_puntos.get()
        for i in range(n):
            tk.Label(self.frame_campos, text=f"x_{i}:").grid(row=i, column=0)
            entry_x = tk.Entry(self.frame_campos)
            entry_x.grid(row=i, column=1)
            self.x_values.append(entry_x)

            tk.Label(self.frame_campos, text=f"f(x_{i}):").grid(row=i, column=2)
            entry_f = tk.Entry(self.frame_campos)
            entry_f.grid(row=i, column=3)
            self.f_values.append(entry_f)

            tk.Label(self.frame_campos, text=f"f'(x_{i}):").grid(row=i, column=4)
            entry_df = tk.Entry(self.frame_campos)
            entry_df.grid(row=i, column=5)
            self.df_values.append(entry_df)

    def calcular_hermite(self):
        """Recupera los datos ingresados, ejecuta el cálculo de Hermite y muestra el resultado."""
        hermite = HermiteInterpolation()

        try:
            hermite.x_values = [float(entry.get()) for entry in self.x_values if entry.get()]
            hermite.f_values = [float(entry.get()) for entry in self.f_values if entry.get()]
            hermite.df_values = [float(entry.get()) for entry in self.df_values if entry.get()]

            if len(hermite.x_values) != self.num_puntos.get() or len(hermite.f_values) != self.num_puntos.get():
                raise ValueError("⚠️ Error: Debes ingresar todos los valores antes de calcular.")

            hermite.construct_table(len(hermite.x_values))
            self.resultado.set(f"Polinomio de Hermite:\n{hermite.get_polynomial()}")

            self.mostrar_tabla(hermite)  # Llamar a la actualización de la tabla

        except ValueError:
            self.resultado.set("⚠️ Error: Asegúrate de ingresar solo números válidos en todos los campos.")

    def mostrar_tabla(self, hermite):
        """Llena la tabla con los resultados usando botones para mejor visualización."""
        for widget in self.frame_tabla.winfo_children():
            widget.destroy()

        encabezados = ["k", "z_k", "f(z_k)", "Diferencias"]
        for j, header in enumerate(encabezados):
            tk.Button(self.frame_tabla, text=header, width=15, height=2, state="disabled").grid(row=0, column=j)

        for i in range(len(hermite.z_values)):
            diffs = ", ".join(str(hermite.q_values[i][j]) for j in range(i + 1))

            tk.Button(self.frame_tabla, text=str(i), width=15, height=2, state="disabled").grid(row=i + 1, column=0)
            tk.Button(self.frame_tabla, text=str(hermite.z_values[i]), width=15, height=2, state="disabled").grid(row=i + 1, column=1)
            tk.Button(self.frame_tabla, text=str(hermite.q_values[i][0]), width=15, height=2, state="disabled").grid(row=i + 1, column=2)
            tk.Button(self.frame_tabla, text=diffs, width=15, height=2, state="disabled").grid(row=i + 1, column=3)