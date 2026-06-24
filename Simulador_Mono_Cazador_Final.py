
# Simulador Mono y Cazador - versión mejorada
# Archivo listo para ejecutar

import tkinter as tk
from tkinter import messagebox
import math

class SimuladorMonoCazador:

    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Movimiento Parabólico - Mono y Cazador")
        self.ventana.geometry("1200x750")
        self.ventana.resizable(False, False)
        self.ventana.configure(bg="#111111")

        self.gravedad = 9.81
        self.escala = 8
        self.dt = 0.02

        self.en_ejecucion = False
        self.en_pausa = False

        self.tiempo = 0
        self.estado = "LISTO"

        self.trayectoria_dardo = []
        self.trayectoria_mono = []

        self.crear_interfaz()

    def crear_interfaz(self):

        marco = tk.Frame(self.ventana, bg="#111111")
        marco.pack(pady=10)

        tk.Label(marco,text="Velocidad (m/s)",bg="#111111",fg="white").grid(row=0,column=0)
        self.entrada_velocidad = tk.Entry(marco,width=8)
        self.entrada_velocidad.grid(row=0,column=1)
        self.entrada_velocidad.insert(0,"40")

        tk.Label(marco,text="Distancia (m)",bg="#111111",fg="white").grid(row=0,column=2)
        self.entrada_distancia = tk.Entry(marco,width=8)
        self.entrada_distancia.grid(row=0,column=3)
        self.entrada_distancia.insert(0,"50")

        tk.Label(marco,text="Altura mono (m)",bg="#111111",fg="white").grid(row=0,column=4)
        self.entrada_altura = tk.Entry(marco,width=8)
        self.entrada_altura.grid(row=0,column=5)
        self.entrada_altura.insert(0,"25")

        tk.Button(marco,text="Iniciar",command=self.iniciar).grid(row=0,column=6,padx=5)
        tk.Button(marco,text="Pausar",command=self.pausar_reanudar).grid(row=0,column=7,padx=5)
        tk.Button(marco,text="Reiniciar",command=self.reiniciar).grid(row=0,column=8,padx=5)

        self.estado_label = tk.Label(
            self.ventana,text="LISTO",
            bg="#111111",fg="white",
            font=("Arial",16,"bold")
        )
        self.estado_label.pack()

        self.lienzo = tk.Canvas(
            self.ventana,width=1100,height=550,
            bg="#101010",highlightthickness=0
        )
        self.lienzo.pack()

        self.info = tk.Label(
            self.ventana,
            text="",
            justify="left",
            font=("Consolas",12),
            bg="#111111",
            fg="white"
        )
        self.info.pack(pady=10)

        self.dibujar_escenario()

    def dibujar_escenario(self):

        self.lienzo.delete("all")

        self.lienzo.create_rectangle(0,0,1100,550,fill="#101010",outline="")

        for x in range(0,1100,50):
            self.lienzo.create_line(x,0,x,550,fill="#222222")

        for y in range(0,550,50):
            self.lienzo.create_line(0,y,1100,y,fill="#222222")

        self.lienzo.create_line(0,450,1100,450,fill="white",width=2)

    def iniciar(self):

        if self.en_ejecucion:
            return

        try:
            self.velocidad = float(self.entrada_velocidad.get())
            self.distancia_mono = float(self.entrada_distancia.get())
            self.altura_mono = float(self.entrada_altura.get())

            if self.velocidad <= 0 or self.distancia_mono <= 0 or self.altura_mono <= 0:
                raise ValueError

        except:
            messagebox.showerror("Error","Valores inválidos")
            return

        self.tiempo = 0
        self.trayectoria_dardo.clear()
        self.trayectoria_mono.clear()

        self.angulo = math.atan2(self.altura_mono,self.distancia_mono)

        self.velocidad_x = self.velocidad * math.cos(self.angulo)
        self.velocidad_y = self.velocidad * math.sin(self.angulo)

        self.en_ejecucion = True
        self.en_pausa = False
        self.estado = "EN VUELO"

        self.estado_label.config(text="EN VUELO",fg="cyan")

        self.animar()

    def pausar_reanudar(self):

        if not self.en_ejecucion:
            return

        self.en_pausa = not self.en_pausa

        if self.en_pausa:
            self.estado_label.config(text="PAUSADO",fg="orange")
        else:
            self.estado_label.config(text="EN VUELO",fg="cyan")
            self.animar()

    def reiniciar(self):

        self.en_ejecucion = False
        self.en_pausa = False
        self.tiempo = 0

        self.trayectoria_dardo.clear()
        self.trayectoria_mono.clear()

        self.estado = "LISTO"
        self.estado_label.config(text="LISTO",fg="white")

        self.info.config(text="")
        self.dibujar_escenario()

    def animar(self):

        if not self.en_ejecucion or self.en_pausa:
            return

        self.tiempo += self.dt
        t = self.tiempo

        x_dardo = self.velocidad_x * t
        y_dardo = self.velocidad_y * t - 0.5 * self.gravedad * t**2

        x_mono = self.distancia_mono
        y_mono = self.altura_mono - 0.5 * self.gravedad * t**2

        distancia = math.sqrt((x_dardo-x_mono)**2 + (y_dardo-y_mono)**2)

        self.trayectoria_dardo.append((x_dardo,y_dardo))
        self.trayectoria_mono.append((x_mono,y_mono))

        self.dibujar_escenario()
        self.dibujar_objetos(x_dardo,y_dardo,x_mono,y_mono)

        vv = self.velocidad_y - self.gravedad*t
        vt = math.sqrt(self.velocidad_x**2 + vv**2)

        self.info.config(
            text=f"Estado: {self.estado}\n"
                 f"Tiempo: {t:.2f} s\n"
                 f"Ángulo: {math.degrees(self.angulo):.2f}°\n"
                 f"Dardo: ({x_dardo:.2f},{y_dardo:.2f})\n"
                 f"Mono: ({x_mono:.2f},{y_mono:.2f})\n"
                 f"Velocidad: {vt:.2f} m/s\n"
                 f"Distancia: {distancia:.6f} m"
        )

        if distancia < 0.001:
            self.estado = "IMPACTO"
            self.estado_label.config(text="IMPACTO",fg="yellow")

            self.lienzo.create_text(
                900,50,
                text="OBJETIVO IMPACTADO",
                fill="yellow",
                font=("Arial",18,"bold")
            )

            self.en_ejecucion = False
            messagebox.showinfo("Choque","¡Choque detectado!")
            return

        if y_dardo < 0:
            self.estado = "FALLO"
            self.estado_label.config(text="FALLO",fg="red")
            self.en_ejecucion = False
            return

        self.ventana.after(int(self.dt*1000),self.animar)

    def dibujar_objetos(self,x_dardo,y_dardo,x_mono,y_mono):

        bx = 60
        by = 450

        xd = bx + x_dardo*self.escala
        yd = by - y_dardo*self.escala

        xm = bx + x_mono*self.escala
        ym = by - y_mono*self.escala

        for i in range(len(self.trayectoria_dardo)-1):
            x1 = bx + self.trayectoria_dardo[i][0]*self.escala
            y1 = by - self.trayectoria_dardo[i][1]*self.escala
            x2 = bx + self.trayectoria_dardo[i+1][0]*self.escala
            y2 = by - self.trayectoria_dardo[i+1][1]*self.escala
            self.lienzo.create_line(x1,y1,x2,y2,fill="red",width=2)

        for i in range(len(self.trayectoria_mono)-1):
            x1 = bx + self.trayectoria_mono[i][0]*self.escala
            y1 = by - self.trayectoria_mono[i][1]*self.escala
            x2 = bx + self.trayectoria_mono[i+1][0]*self.escala
            y2 = by - self.trayectoria_mono[i+1][1]*self.escala
            self.lienzo.create_line(x1,y1,x2,y2,fill="#00aaff",dash=(3,2))

        self.lienzo.create_rectangle(xm-6,ym,xm+6,by,fill="#777777",outline="")
        self.lienzo.create_oval(xm-18,ym-20,xm+18,ym+10,fill="#555555",outline="")

        self.lienzo.create_oval(xm-4,ym-4,xm+4,ym+4,fill="white")

        self.lienzo.create_rectangle(35,420,60,450,fill="#cccccc")

        vv = self.velocidad_y - self.gravedad*self.tiempo
        ang = math.atan2(vv,self.velocidad_x)

        self.lienzo.create_line(
            xd,yd,
            xd+20*math.cos(ang),
            yd-20*math.sin(ang),
            fill="#00ffff",
            width=3
        )

        self.lienzo.create_line(xd,yd,xd,yd+30,fill="white",arrow=tk.LAST)

        x2 = xd + 18*math.cos(ang)
        y2 = yd - 18*math.sin(ang)

        self.lienzo.create_line(xd,yd,x2,y2,fill="red",width=4)

        self.lienzo.create_text(
            150,30,
            text=f"Ángulo: {math.degrees(self.angulo):.2f}°",
            fill="white",
            font=("Arial",12,"bold")
        )

if __name__ == "__main__":
    ventana = tk.Tk()
    SimuladorMonoCazador(ventana)
    ventana.mainloop()
