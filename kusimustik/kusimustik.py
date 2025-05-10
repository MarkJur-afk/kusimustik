import random
import smtplib
from email.message import EmailMessage

N = 5  # mitu küsimust korraga

vastajad = {}  # siia lähevad kõik vastajad

# emaili seaded
SAATJA_EMAIL = "markjurgennn@gmail.com"
SAATJA_PAROOL = "tvus kxfs vtpn nwee"  # app password

def loe_kusimused():
    with open('kusimused_vastused.txt', 'r', encoding='utf-8') as f:
        return dict(line.strip().split(':', 1) for line in f if ':' in line)

def gen_email(nimi):
    osad = nimi.strip().split()
    if len(osad) >= 2:
        eesnimi, perenimi = osad[0], osad[1]
    else:
        eesnimi = osad[0]
        perenimi = "kasutaja"
    return f"{eesnimi.lower()}.{perenimi.lower()}@example.com"

def kuula_kusimusi(kus_vas, nimi):
    print(f"\nTere, {nimi}! Alustame küsimustikku.")
    kysimused = random.sample(list(kus_vas.keys()), min(N, len(kus_vas)))
    oiged = 0
    for k in kysimused:
        vastus = input(f"{k}: ").lower().strip()
        if vastus == kus_vas[k].lower():
            oiged += 1
    return oiged

def salvesta_vastaja(nimi, oiged, email):
    vastajad[nimi] = {"õiged_vastused": oiged, "email": email}

def saada_email(email, nimi, oiged):
    sisu = f"Tere {nimi}!\nSul oli {oiged} vastust õigesti.\n"
    if oiged > N // 2:
        sisu += "Test sooritatud edukalt!"
    else:
        sisu += "Kahjuks test jäi sooritamata."

    msg = EmailMessage()
    msg.set_content(sisu)
    msg['Subject'] = 'Testi tulemus'
    msg['From'] = SAATJA_EMAIL
    msg['To'] = email

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(SAATJA_EMAIL, SAATJA_PAROOL)
        server.send_message(msg)

def saada_email_tootajale():
    if not vastajad:
        return

    msg = EmailMessage()
    msg['Subject'] = "Testi tulemused"
    msg['From'] = SAATJA_EMAIL
    msg['To'] = "tootaja@firma.ee"

    sisu = "Tere!\n\nTulemused:\n"
    for nimi, info in vastajad.items():
        staatus = "SOBIS" if info['õiged_vastused'] > N // 2 else "EI SOBINUD"
        sisu += f"{nimi} – {info['õiged_vastused']} – {info['email']} – {staatus}\n"

    parim = max(vastajad.items(), key=lambda x: x[1]['õiged_vastused'])
    sisu += f"\nParim vastaja: {parim[0]} ({parim[1]['õiged_vastused']})\n\nLugupidamisega,\nSüsteem"

    msg.set_content(sisu)

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(SAATJA_EMAIL, SAATJA_PAROOL)
        server.send_message(msg)

def salvesta_failidesse():
    with open('koik.txt', 'w', encoding='utf-8') as f1, \
         open('oiged.txt', 'w', encoding='utf-8') as f2, \
         open('valed.txt', 'w', encoding='utf-8') as f3:

        for nimi, info in sorted(vastajad.items(), key=lambda x: x[1]['õiged_vastused'], reverse=True):
            email = info['email']
            oiged = info['õiged_vastused']
            f1.write(f"{nimi}, {oiged}, {email}\n")
            if oiged > N // 2:
                f2.write(f"{nimi} – {oiged} õigesti\n")
            else:
                f3.write(f"{nimi} – {oiged} õigesti\n")

def main():
    kus_vas = loe_kusimused()

    while True:
        print("\n1. Alusta test")
        print("2. Lisa küsimus")
        print("3. Lõpeta ja salvesta")
        valik = input("Valik: ")

        if valik == "1":
            nimi = input("Nimi (eesnimi perekonnanimi): ").title()
            if nimi in vastajad:
                print("See inimene on juba vastanud.")
                continue
            oiged = kuula_kusimusi(kus_vas, nimi)
            email = gen_email(nimi)
            salvesta_vastaja(nimi, oiged, email)
            saada_email(email, nimi, oiged)

        elif valik == "2":
            k = input("Küsimus: ")
            v = input("Õige vastus: ")
            with open('kusimused_vastused.txt', 'a', encoding='utf-8') as f:
                f.write(f"{k}:{v}\n")
            print("Lisatud.")

        elif valik == "3":
            salvesta_failidesse()
            saada_email_tootajale()
            print("Salvestatud. Tšau!")
            break

        else:
            print("Tundmatu valik.")

if __name__ == "__main__":
    main()
