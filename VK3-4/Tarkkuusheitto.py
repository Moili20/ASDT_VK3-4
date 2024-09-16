import tkinter as tk
import random
import pygame

class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Kernesti ja maalitaulu")

        #Ikkunan koko
        self.root.geometry("1440x1080")

        #Luodaan Canvas
        self.canvas = tk.Canvas(self.root, width=1200, height=700)
        self.canvas.pack()

        #Kernestin ja Ernestin kuvien lataaminen
        self.kernest_img = tk.PhotoImage(file="kerne.png")
        self.ernest_img = tk.PhotoImage(file="erne.png")

        #Maalitaulun kuvan lataaminen
        self.target_img = tk.PhotoImage(file="maalitaulu.png")

        #Tomaatin ja splatin lataaminen
        self.tomato_img = tk.PhotoImage(file="tomaatti.png")
        self.spalt_img = tk.PhotoImage(file="splat.png")

        #Laitetaan maalitaulu keskelle ikkunaa
        self.target_x = 600
        self.target_y = 300
        self.canvas.create_image(self.target_x, self.target_y, image=self.target_img)

        #Maalitaulun y-askelin osuma-alueen laajennus (+/- 50 pixeliä)
        self.target_hitbox_min_y = self.target_y - 50
        self.target_hitbox_max_y = self.target_y + 50

        #Laitetaan kernestin kuva vasempaan laitaan satunnaiseen kohtaan
        self.kernest_x = random.randint(10, 150)
        self.kernest_y = random.randint(10, 550) #Laajennettu y-akseli
        self.kernest = self.canvas.create_image(self.kernest_x, self.kernest_y, image=self.kernest_img, anchor=tk.NW)

        #Laitetaan ernestin kuva oikeaan laitaan satunnaiseen kohtaan
        self.ernest_x = random.randint(900, 1100)
        self.ernest_y = random.randint(50,550) #Laajennettu y-akseli
        self.ernest = self.canvas.create_image(self.ernest_x, self.ernest_y, image=self.ernest_img, anchor=tk.NW)

        #Laitetaan äänet heitolle sekä osumiselle
        pygame.mixer.init()
        self.throw_sound = pygame.mixer.Sound("mixkit-quick-rope-throw-730.mp3")
        self.hit_sound = pygame.mixer.Sound("mixkit-soft-quick-punch-2151.wav")

        #Sanakirja osumistietojen tallentamiselle
        self.hit_data = {"kernest": 0, "ernest": 0}

        #Luodaan osumislaskuri maalitaulun yläpuolelle
        self.kernest_hits_label = tk.Label(self.root, text="Kernestin osumat: 0", font=("Arial", 16))
        self.kernest_hits_label.pack()

        self.ernest_hits_label = tk.Label(self.root, text=" Ernestin osumat: 0", font=("Arial", 16))
        self.ernest_hits_label.pack()

        #Napit Ernestin ja Kernestin tomaatin heitolle
        self.button_ernest = tk.Button(self.root, text="Heitä tomaatti Ernestillä", command=self.throw_tomato_from_ernest)
        self.button_ernest.pack()

        self.button_kernest = tk.Button(self.root, text="Heitä tomaatti Kernestillä", command=self.throw_tomato_from_kernest)
        self.button_kernest.pack()

        #Napit ernestin ja kernestin liikuttelulle
        self.move_ernest_button = tk.Button(self.root, text="Liikuta Ernestiä", command=self.move_ernest)
        self.move_ernest_button.pack()

        self.move_kernest_button = tk.Button(self.root, text="Liikuta Kernestiä", command=self.move_kernest)
        self.move_kernest_button.pack()

        #Reset-painike
        self.reset_button = tk.Button(self.root, text="Nollaa tulokset", command=self.reset_score)
        self.reset_button.pack()

    def animate_tomato(self, tomato, start_x, start_y, end_x, step=0, thrower=""):

        #Lasketaan uudet koordinaatit 
        new_x = start_x + step * (end_x - start_x) / 100

        #Päivitetään tomaatin sijainti
        self.canvas.coords(tomato, new_x, start_y)

        #Jatketaan animaatiota, jos step on alle 100
        if step < 100:
            self.root.after(10, self.animate_tomato, tomato, start_x, start_y, end_x, step + 1, thrower)

        else:
            #Tarkistetaan osuuko tomaatti tauluun osuma-alueen sisälle
            if self.target_hitbox_min_y <= start_y <= self.target_hitbox_max_y:
                #poistetaan tomaatti ja lisätään splat kuva
                self.canvas.delete(tomato)
                self.canvas.create_image(self.target_x, self.target_y, image=self.spalt_img, anchor=tk.CENTER)

                #Soita osumaääni
                self.hit_sound.play()

                #Tallenna osuma
                self.hit_data[thrower] += 1
                print(f"{thrower} Osuit! Osumia yhteensä: {self.hit_data[thrower]}")

                #Päivitetään osuma näytölle
                self.update_hit_labels()

            else:
                #jos heitto menee ohi, poistetaan tomaatti
                self.canvas.delete(tomato)
                print(f"{thrower} Huti")

    def throw_tomato(self, start_x, start_y, thrower):

        #Tomaatin lentorata x akselilla
        tomato = self.canvas.create_image(start_x, start_y, image=self.tomato_img)

        #Soita heittoääni
        self.throw_sound.play()

        #Aloitetaan animaatio x-akselin suuntaisesti
        self.animate_tomato(tomato, start_x, start_y, self.target_x, thrower=thrower)
    
    def throw_tomato_from_ernest(self):
        self.throw_tomato(self.ernest_x + 50, self.ernest_y + 50, "ernest")

    def throw_tomato_from_kernest(self):
        self.throw_tomato(self.kernest_x + 50, self.kernest_y + 50, "kernest")

    def move_ernest(self):
        #Ernestin siirto satunnaiseen y koordinaattiin
        new_y = random.randint(50, 550)
        self.canvas.coords(self.ernest, self.ernest_x, new_y)
        self.ernest_y = new_y

    def move_kernest(self):
        #Kernestin siirto satunnaiseen y koordinaattiin
        new_y = random.randint(50, 550)
        self.canvas.coords(self.kernest, self.kernest_x, new_y)
        self.kernest_y = new_y
    
    #Päivitetään osumien määrä näytölle
    def update_hit_labels(self):
        self.kernest_hits_label.config(text=f"Kernestin osumat: {self.hit_data['kernest']}")
        self.ernest_hits_label.config(text=f"Ernestin osumat: {self.hit_data['ernest']}")
    #Nollataan osumatiedot
    def reset_score(self):
        self.hit_data = {"kernest": 0, "ernest": 0}

        #Päivitetään laskuri
        self.update_hit_labels()

        print("Tulokset nollattu.")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()
                


    