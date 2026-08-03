
-

```markdown
# 🎯 AIMBOT HEADSHOT - Termux/Shizuku Edition

> Script automatisé de visée pour Free Fire sur Android, utilisant Shizuku pour contrôler l'écran sans ADB.

---

## 📋 Prérequis

- **Android 8+** avec débogage USB activé
- **Termux** installé depuis F-Droid
- **Shizuku** installé depuis [F-Droid](https://f-droid.org/packages/moe.shizuku.privileged.api/)
- **Espace de stockage** : 100 MB minimum

---

## 🔧 Installation

### 1. Installer les dépendances Termux

```bash
pkg update -y
pkg install python opencv android-tools -y
pip install opencv-python numpy pillow readchar
termux-setup-storage
```

2. Activer Shizuku

1. Ouvre Shizuku et suis les instructions
2. Active Débogage sans fil dans les options développeur
3. Lance Shizuku → "Start" (attends "Shizuku is running")

3. Télécharger le script

```bash
git clone https://github.com/Terror404-hacker/panelff.git
cd panelff
python mypanel.py
```

Sauvegarde : CTRL+X → O → ENTRÉE

---

Contrôles

· ESPACE : Activer/Désactiver le suivi
· CTRL+C : Quitter le script

---
