#!/data/data/com.termux/files/usr/bin/python3
# -*- coding: utf-8 -*-

"""
🎯 AIMBOT HEADSHOT - SHIZUKU EDITION
Utilise Shizuku pour les commandes privilégiées sans ADB
"""

import cv2
import numpy as np
import subprocess
import time
import os
import sys
import math
import urllib.request

# ==================== CONFIGURATION ====================
SCREEN_W = 1080
SCREEN_H = 2400
CENTER_X = SCREEN_W // 2
CENTER_Y = SCREEN_H // 2

DELAY_BETWEEN_SHOTS = 0.05
SMOOTH_FACTOR = 0.3
UPDATE_THRESHOLD = 10
HEAD_MIN_SIZE = 20

HAAR_FILE = "/sdcard/haarcascade_frontalface_default.xml"
TEMP_SCREEN = "/sdcard/temp_screen.png"

# ==================== FONCTIONS SHIZUKU ====================
def shizuku_command(cmd):
    """
    Exécute une commande via Shizuku (privilèges élevés sans root)
    """
    try:
        # On utilise shizuku pour exécuter la commande
        full_cmd = f"shizuku {cmd}"
        result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"⚠️ Shizuku error: {result.stderr}")
            return None
        return result.stdout.strip()
    except Exception as e:
        print(f"❌ Shizuku error: {e}")
        return None

def capture_screen():
    """
    Capture d'écran via Shizuku (beaucoup plus rapide que ADB)
    """
    try:
        # Capture via screencap avec Shizuku
        cmd = f"screencap -p {TEMP_SCREEN}"
        result = shizuku_command(cmd)
        if result is None:
            return None
        
        # Lire le fichier directement depuis /sdcard
        if not os.path.exists(TEMP_SCREEN):
            return None
        
        img = cv2.imread(TEMP_SCREEN)
        if img is None:
            return None
        
        # Nettoyer le fichier temporaire
        try:
            os.remove(TEMP_SCREEN)
        except:
            pass
        
        return cv2.resize(img, (SCREEN_W, SCREEN_H))
    except Exception as e:
        print(f"❌ Erreur capture: {e}")
        return None

def swipe_screen(x1, y1, x2, y2, duration=30):
    """
    Glissé via Shizuku avec input swipe
    """
    x1 = max(0, min(SCREEN_W, int(x1)))
    y1 = max(0, min(SCREEN_H, int(y1)))
    x2 = max(0, min(SCREEN_W, int(x2)))
    y2 = max(0, min(SCREEN_H, int(y2)))
    cmd = f"input swipe {x1} {y1} {x2} {y2} {duration}"
    result = shizuku_command(cmd)
    return result is not None

def get_screen_size():
    """
    Récupère la résolution via wm size avec Shizuku
    """
    result = shizuku_command("wm size")
    if result:
        try:
            # Format: "Physical size: 1080x2400"
            size_str = result.split(":")[1].strip()
            w, h = size_str.split("x")
            return int(w), int(h)
        except:
            pass
    return 1080, 2400

def check_shizuku():
    """
    Vérifie que Shizuku est bien installé et en cours d'exécution
    """
    try:
        # Vérifier si shizuku est installé
        result = subprocess.run("which shizuku", shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Shizuku non installé dans le PATH")
            print("   Installez Shizuku depuis: https://shizuku.rikka.app/")
            return False
        
        # Vérifier si Shizuku tourne
        result = shizuku_command("echo test")
        if result is None:
            print("❌ Shizuku ne répond pas")
            print("   Assurez-vous que Shizuku est en cours d'exécution")
            print("   Activez le débogage sans fil dans les options développeur")
            return False
        
        print("✅ Shizuku est actif")
        return True
    except Exception as e:
        print(f"❌ Erreur vérification Shizuku: {e}")
        return False

# ==================== DÉTECTION ====================
def download_haar():
    url = "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml"
    urllib.request.urlretrieve(url, HAAR_FILE)
    print("✅ HAAR téléchargé")

def detect_faces(img):
    if not os.path.exists(HAAR_FILE):
        download_haar()
        return []
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(HAAR_FILE)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(HEAD_MIN_SIZE, HEAD_MIN_SIZE))
    heads = []
    for (x, y, w, h) in faces:
        heads.append((x, y, w, h, w * h))
    return heads

def find_best_head(heads):
    if not heads:
        return None
    heads.sort(key=lambda t: t[4], reverse=True)
    x, y, w, h, _ = heads[0]
    return (x, y, w, h)

# ==================== BANNER ====================
def afficher_banner():
    """
    Affiche un banner stylé avec "SORRY" en VERT dans un rectangle CYAN
    """
    os.system('clear')
    
    largeur = 60
    bord = "█"
    
    # Ligne du haut
    print("\033[46m" + bord * largeur + "\033[0m")
    
    # Lignes vides
    for i in range(2):
        print("\033[46m" + bord + "\033[0m" + " " * (largeur - 2) + "\033[46m" + bord + "\033[0m")
    
    # "SORRY" en VERT
    texte = "   ███████╗ ██████╗ ██████╗ ██████╗ ██╗   ██╗   "
    print("\033[46m" + bord + "\033[0m" + "\033[92m" + texte + "\033[0m" + "\033[46m" + bord + "\033[0m")
    
    texte2 = "   ██╔════╝██╔═══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝   "
    print("\033[46m" + bord + "\033[0m" + "\033[92m" + texte2 + "\033[0m" + "\033[46m" + bord + "\033[0m")
    
    texte3 = "   ███████╗██║   ██║██████╔╝██║  ██║ ╚████╔╝    "
    print("\033[46m" + bord + "\033[0m" + "\033[92m" + texte3 + "\033[0m" + "\033[46m" + bord + "\033[0m")
    
    texte4 = "   ╚════██║██║   ██║██╔══██╗██║  ██║  ╚██╔╝     "
    print("\033[46m" + bord + "\033[0m" + "\033[92m" + texte4 + "\033[0m" + "\033[46m" + bord + "\033[0m")
    
    texte5 = "   ███████║╚██████╔╝██║  ██║██████╔╝   ██║      "
    print("\033[46m" + bord + "\033[0m" + "\033[92m" + texte5 + "\033[0m" + "\033[46m" + bord + "\033[0m")
    
    texte6 = "   ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝    ╚═╝      "
    print("\033[46m" + bord + "\033[0m" + "\033[92m" + texte6 + "\033[0m" + "\033[46m" + bord + "\033[0m")
    
    # Lignes vides
    for i in range(2):
        print("\033[46m" + bord + "\033[0m" + " " * (largeur - 2) + "\033[46m" + bord + "\033[0m")
    
    # Ligne du bas
    print("\033[46m" + bord * largeur + "\033[0m")
    
    print("\n" + "═" * 60)
    print("\033[92m🔫 AIMBOT HEADSHOT - Shizuku Edition\033[0m")
    print("\033[96m📱 Appuyez sur ESPACE pour activer/désactiver\033[0m")
    print("\033[91m⛔ CTRL+C pour quitter\033[0m")
    print("═" * 60 + "\n")

# ==================== BOUCLE ====================
last_target = None
running = True

def viser_et_glisser():
    global last_target

    img = capture_screen()
    if img is None:
        return

    heads = detect_faces(img)
    head = find_best_head(heads)
    if head is None:
        return

    x, y, w, h = head

    # Visée = haut du crâne (25% du rectangle)
    aim_x = x + w // 2
    aim_y = y + int(h * 0.25)

    if last_target is not None:
        lx, ly = last_target
        aim_x = int(lx + (aim_x - lx) * (1 - SMOOTH_FACTOR))
        aim_y = int(ly + (aim_y - ly) * (1 - SMOOTH_FACTOR))
        if math.hypot(aim_x - lx, aim_y - ly) < UPDATE_THRESHOLD:
            return

    if last_target is None:
        start_x, start_y = CENTER_X, CENTER_Y
    else:
        start_x, start_y = last_target

    distance = math.hypot(aim_x - start_x, aim_y - start_y)
    duration = int(15 + distance * 0.08)
    duration = max(15, min(80, duration))

    swipe_screen(start_x, start_y, aim_x, aim_y, duration)
    last_target = (aim_x, aim_y)
    print(f"✅ Glissé: ({start_x}, {start_y}) -> ({aim_x}, {aim_y}) en {duration}ms")

def main():
    global SCREEN_W, SCREEN_H, running, last_target

    # AFFICHE LE BANNER
    afficher_banner()

    print("🔍 Vérification Shizuku...")
    if not check_shizuku():
        print("\n💡 Pour résoudre :")
        print("   1. Activez le débogage sans fil dans les options développeur")
        print("   2. Lancez Shizuku et suivez les instructions")
        print("   3. Dans Termux : adb connect 127.0.0.1:5555")
        print("   4. Puis : shizuku")
        sys.exit(1)

    w, h = get_screen_size()
    SCREEN_W, SCREEN_H = w, h
    global CENTER_X, CENTER_Y
    CENTER_X = SCREEN_W // 2
    CENTER_Y = SCREEN_H // 2

    print(f"✅ Résolution détectée : {SCREEN_W}x{SCREEN_H}")
    print("🎯 AIMBOT PRÊT !\n")

    suivi_actif = True
    try:
        import readchar
        while running:
            try:
                key = readchar.readkey()
                if key == ' ':
                    suivi_actif = not suivi_actif
                    status = "\033[92mON\033[0m" if suivi_actif else "\033[91mOFF\033[0m"
                    print(f"[!] Suivi : {status}")
            except:
                pass

            if suivi_actif:
                viser_et_glisser()
            time.sleep(DELAY_BETWEEN_SHOTS)

    except KeyboardInterrupt:
        print("\n\n\033[91m⛔ Arrêt demandé\033[0m")
    except ImportError:
        print("❌ Installez 'readchar' : pip install readchar")
    finally:
        running = False
        print("\033[92m✅ Nettoyage terminé. À bientôt !\033[0m")

if __name__ == "__main__":
    main()
