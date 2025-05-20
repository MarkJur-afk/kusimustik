import random
import smtplib
from email.message import EmailMessage

# Loeme küsimused ja vastused failist
def loe_kusimused():
    with open('kusimused_vastused.txt', 'r') as file:
        return dict(line.strip().split(':') for line in file)

# Küsitluse läbiviimine
def kuula_kusimusi(kus_vas, kasutaja_nimi, num_kusimusi=5):
    print(f"Tere, {kasutaja_nimi}! Alustame küsimustiku.")
    valitud_kusimused = random.sample(list(kus_vas.keys()), min(num_kusimusi, len(kus_vas)))
    return sum(input(f"{kysimus}: ").lower() == kus_vas[kysimus].lower() for kysimus in valitud_kusimused)

# Kontrollimine, kas kasutajat on juba küsitletud
vastajad = {}

def salvesta_vastaja(nimi, õiged_vastused, email):
    vastajad[nimi] = {"õiged_vastused": õiged_vastused, "email": email}

# Emaili saatmine
def saada_email(kasutaja_email, kasutaja_nimi, õiged_vastused):
    status = "Palju õnne, olete testi edukalt läbinud!" if õiged_vastused > 2 else "Kahjuks testi ei läbitud."
    msg = EmailMessage()
    msg.set_content(f"Tere {kasutaja_nimi}!\nÕigete vastuste arv: {õiged_vastused}\n{status}")
    msg['Subject'] = 'Küsimustiku tulemused'
    msg['From'] = 'markjurgennn@gmail.com'
    msg['To'] = kasutaja_email

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.ehlo()
        server.starttls()
        server.login("markjurgennn@gmail.com", "tvus kxfs vtpn nwee") 
        server.send_message(msg)

# Tulemuste salvestamine failidesse
def salvesta_failidesse():
    def korrektne_vastus(x):
        return x[1]['õiged_vastused']
    
    with open('koik.txt.txt', 'w', encoding='utf-8') as f_koik, open('oiged.txt.txt', 'w', encoding='utf-8') as f_oiged, open('valed.txt.txt', 'w', encoding='utf-8') as f_valed:
        for nimi, info in sorted(vastajad.items(), key=korrektne_vastus, reverse=True):
            email = info['email']
            õiged_vastused = info['õiged_vastused']
            f_koik.write(f"{nimi}, {õiged_vastused}, {email}\n")
            target = f_oiged if õiged_vastused > 2 else f_valed
            target.write(f"{nimi} – {õiged_vastused} õigesti\n")

# Main Menu
def main():
    kus_vas = loe_kusimused()

    while True:
        print("\nMenu:")
        print("1. Alusta küsitlus")
        print("2. Lisa uus küsimus")
        print("3. Välja")
        valik = input("Valge valik: ")

        if valik == "1":
            kasutaja_nimi = input("Sisestage oma nimi: ")
            if kasutaja_nimi in vastajad:
                print(f"{kasutaja_nimi} juba läbinud küsitluse.")
            else:
                õiged_vastused = kuula_kusimusi(kus_vas, kasutaja_nimi)
                kasutaja_email = input("Sisestage oma emaili, et tulemused vaadata: ")
                salvesta_vastaja(kasutaja_nimi, õiged_vastused, kasutaja_email)
                saada_email(kasutaja_email, kasutaja_nimi, õiged_vastused)
        elif valik == "2":
            kysimus = input("Lisa uus küsimus: ")
            vastus = input("Lisa õige vastus: ")
            with open('kusimused_vastused.txt.txt', 'a') as file:
                file.write(f"{kysimus}:{vastus}\n")
        elif valik == "3":
            salvesta_failidesse()
            print("Küsitluse tulemused on säilinud.")
            break
        else:
            print("Vale valik. Proovi uuesti.")

if __name__ == "__main__":
    main()
