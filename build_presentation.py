#!/usr/bin/env python3
"""Deck FYC Detection Engineering, calé sur la charte du support ESGI 2026-2027."""

from pathlib import Path

import pymupdf

W, H = 720, 540
COVER = (0.031, 0.086, 0.204)
NAVY = (0.055, 0.133, 0.286)
CYAN = (0.122, 0.706, 0.867)
PALE = (0.918, 0.957, 0.98)
WHITE = (1, 1, 1)
LINE = (0.82, 0.86, 0.90)
MUTED = (0.28, 0.36, 0.48)

FONT_DIR = "/System/Library/Fonts/Supplemental"
FONT = {
    "f": f"{FONT_DIR}/Arial.ttf",
    "fb": f"{FONT_DIR}/Arial Bold.ttf",
    "fi": f"{FONT_DIR}/Arial Italic.ttf",
    "fbi": f"{FONT_DIR}/Arial Bold Italic.ttf",
}

OUT = Path(__file__).resolve().parent / "FYC-Detection-Engineering-SOC.pdf"
REPORT = Path(__file__).resolve().parent / "Rapport_Seance_1_FYC.pdf"
FOOTER_L = "ESGI — Projet FYC 2026-2027"
FOOTER_R = "GES — Grandes Écoles Spécialisées"


_FONTS = {name: pymupdf.Font(fontfile=path) for name, path in FONT.items()}


def tlen(text: str, font: str, size: float) -> float:
    return _FONTS[font].text_length(text, fontsize=size)


def wrap(text: str, font: str, size: float, max_w: float) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        trial = word if not current else f"{current} {word}"
        if tlen(trial, font, size) <= max_w:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


class Deck:
    def __init__(self) -> None:
        self.doc = pymupdf.open()
        self.page_no = 0

    def _page(self) -> pymupdf.Page:
        page = self.doc.new_page(width=W, height=H)
        for name, path in FONT.items():
            page.insert_font(fontname=name, fontfile=path)
        return page

    def _logo(self, page: pymupdf.Page, color: tuple[float, float, float]) -> None:
        page.insert_text((34, 42), "ESGI", fontname="fb", fontsize=18, color=color)
        page.insert_text(
            (34, 56), "école supérieure de", fontname="f", fontsize=6.5, color=CYAN
        )
        page.insert_text(
            (34, 64), "génie informatique", fontname="f", fontsize=6.5, color=CYAN
        )

    def _footer(self, page: pymupdf.Page, number: int) -> None:
        page.draw_rect(pymupdf.Rect(0, H - 28, W, H), color=NAVY, fill=NAVY, width=0)
        page.insert_text((34, H - 12), FOOTER_L, fontname="f", fontsize=7, color=WHITE)
        right = FOOTER_R
        rw = tlen(right, "fb", 7)
        page.insert_text((W - 34 - rw, H - 12), right, fontname="fb", fontsize=7, color=WHITE)
        label = str(number)
        lw = tlen(label, "f", 7)
        page.insert_text(((W - lw) / 2, H - 12), label, fontname="f", fontsize=7, color=WHITE)

    def content(self, title: str) -> pymupdf.Page:
        self.page_no += 1
        page = self._page()
        page.draw_rect(pymupdf.Rect(0, 0, W, H), color=WHITE, fill=WHITE, width=0)
        page.draw_rect(pymupdf.Rect(0, 0, W, 79), color=NAVY, fill=NAVY, width=0)
        page.draw_rect(pymupdf.Rect(0, 79, W, 82), color=CYAN, fill=CYAN, width=0)
        self._logo(page, WHITE)
        page.insert_text((128, 48), title, fontname="f", fontsize=22, color=WHITE)
        self._footer(page, self.page_no)
        return page

    def cover(self) -> None:
        page = self._page()
        page.draw_rect(pymupdf.Rect(0, 0, W, H), color=COVER, fill=COVER, width=0)
        self._logo(page, WHITE)
        kicker = "PROMOTION 2026-2027"
        kw = tlen(kicker, "fb", 11)
        page.insert_text(((W - kw) / 2, 198), kicker, fontname="fb", fontsize=11, color=CYAN)
        page.draw_rect(pymupdf.Rect(0, 214, W, 216.5), color=CYAN, fill=CYAN, width=0)
        for text, y, size, font in (
            ("Detection Engineering", 268, 36, "f"),
            ("pour un SOC", 312, 28, "f"),
        ):
            tw = tlen(text, font, size)
            page.insert_text(((W - tw) / 2, y), text, fontname=font, fontsize=size, color=WHITE)
        sub = "Windows / Active Directory  —  SIEM  —  MITRE ATT&CK"
        sw = tlen(sub, "f", 13)
        page.insert_text(((W - sw) / 2, 348), sub, fontname="f", fontsize=13, color=WHITE)
        tag = "Projet FYC  —  Find Your Course"
        tw = tlen(tag, "f", 12)
        page.insert_text(((W - tw) / 2, 378), tag, fontname="f", fontsize=12, color=CYAN)
        page.insert_text(
            (W - 34 - tlen(FOOTER_R, "f", 8), H - 28),
            FOOTER_R,
            fontname="f",
            fontsize=8,
            color=WHITE,
        )

    def section(self, title: str) -> None:
        page = self._page()
        page.draw_rect(pymupdf.Rect(0, 0, W, H), color=COVER, fill=COVER, width=0)
        self._logo(page, WHITE)
        page.draw_rect(pymupdf.Rect(72, 292, W - 72, 294.5), color=CYAN, fill=CYAN, width=0)
        tw = tlen(title, "f", 36)
        page.insert_text(((W - tw) / 2, 276), title, fontname="f", fontsize=36, color=WHITE)

    def lead(self, page: pymupdf.Page, text: str, y: float = 98) -> float:
        page.insert_textbox(
            pymupdf.Rect(40, y, W - 40, y + 36),
            text,
            fontname="fb",
            fontsize=13,
            color=NAVY,
            align=0,
        )
        return y + 38

    def callout(self, page: pymupdf.Page, text: str, y: float, height: float = 58) -> float:
        rect = pymupdf.Rect(40, y, W - 40, y + height)
        page.draw_rect(rect, color=PALE, fill=PALE, width=0)
        page.draw_rect(pymupdf.Rect(40, y, 43.4, y + height), color=CYAN, fill=CYAN, width=0)
        page.insert_textbox(
            pymupdf.Rect(54, y + 8, W - 52, y + height - 6),
            text,
            fontname="fi",
            fontsize=12,
            color=NAVY,
            align=0,
        )
        return y + height + 14

    def bullets(
        self,
        page: pymupdf.Page,
        items: list[tuple[str, list[str]]],
        y: float,
        size: float = 12.5,
        gap: float = 10,
    ) -> float:
        for title, subs in items:
            page.draw_rect(pymupdf.Rect(42, y + 3, 50, y + 11), color=CYAN, fill=CYAN, width=0)
            lines = wrap(title, "fb", size, W - 110)
            for i, line in enumerate(lines):
                page.insert_text((58, y + 11 + i * (size + 2)), line, fontname="fb", fontsize=size, color=NAVY)
            y += len(lines) * (size + 3) + 2
            for sub in subs:
                sub_lines = wrap(sub, "f", 11, W - 128)
                for i, line in enumerate(sub_lines):
                    page.insert_text(
                        (70, y + 12 + i * 14),
                        line,
                        fontname="f",
                        fontsize=11,
                        color=NAVY,
                    )
                y += len(sub_lines) * 14 + 2
            y += gap
        return y

    def table(
        self,
        page: pymupdf.Page,
        headers: list[str],
        rows: list[list[str]],
        widths: list[float],
        y: float,
        row_h: float = 22,
        font_size: float = 9,
    ) -> float:
        x0 = 40
        header_h = 22
        page.draw_rect(
            pymupdf.Rect(x0, y, x0 + sum(widths), y + header_h),
            color=NAVY,
            fill=NAVY,
            width=0,
        )
        x = x0
        for header, width in zip(headers, widths):
            page.insert_text((x + 6, y + 15), header, fontname="fb", fontsize=8, color=WHITE)
            x += width
        y += header_h
        for r, row in enumerate(rows):
            bg = PALE if r % 2 == 0 else WHITE
            page.draw_rect(
                pymupdf.Rect(x0, y, x0 + sum(widths), y + row_h),
                color=bg,
                fill=bg,
                width=0,
            )
            x = x0
            for cell, width in zip(row, widths):
                page.insert_textbox(
                    pymupdf.Rect(x + 6, y + 3, x + width - 4, y + row_h - 1),
                    cell,
                    fontname="f",
                    fontsize=font_size,
                    color=NAVY,
                    align=0,
                )
                x += width
            y += row_h
        page.draw_rect(
            pymupdf.Rect(x0, y - row_h * len(rows) - header_h, x0 + sum(widths), y),
            color=LINE,
            fill=None,
            width=0.4,
        )
        return y + 8

    def save(self) -> None:
        self.doc.save(OUT)
        self.doc.close()


def build() -> None:
    deck = Deck()
    deck.cover()

    page = deck.content("L'équipe")
    y = deck.lead(page, "Quatre étudiants, un mentor professionnel, un cours à transmettre.")
    y = deck.callout(
        page,
        "Le mentor n'est pas un évaluateur passif : il aide à délimiter le sujet, valide la scénarisation et suit la production jusqu'à la soutenance.",
        y,
        52,
    )
    names = [
        "Victor TASSART",
        "Marwane ZAID",
        "Younès HANNOUR",
        "Jacques-D'evaldo TOBOSSOU",
    ]
    for i, name in enumerate(names):
        col = i % 2
        row = i // 2
        x = 40 + col * 330
        yy = y + row * 64
        page.draw_rect(pymupdf.Rect(x, yy, x + 310, yy + 52), color=PALE, fill=PALE, width=0)
        page.draw_rect(pymupdf.Rect(x, yy, x + 5, yy + 52), color=CYAN, fill=CYAN, width=0)
        page.insert_text((x + 18, yy + 32), name, fontname="fb", fontsize=13, color=NAVY)
    y += 144
    page.draw_rect(pymupdf.Rect(40, y, W - 40, y + 58), color=NAVY, fill=NAVY, width=0)
    page.insert_text((58, y + 24), "MENTOR", fontname="fb", fontsize=9, color=CYAN)
    page.insert_text((58, y + 44), "Adam RAHMI", fontname="fb", fontsize=14, color=WHITE)
    page.insert_text(
        (250, y + 36),
        "Professionnel du sujet, partie prenante du suivi.",
        fontname="f",
        fontsize=12,
        color=WHITE,
    )
    page.insert_text(
        (40, y + 82),
        "Chacun contribue à l'ensemble du cours. Un responsable clair est désigné par livrable.",
        fontname="fi",
        fontsize=11,
        color=MUTED,
    )

    page = deck.content("Objectifs du cours")
    y = deck.lead(
        page,
        "Former à concevoir, tester et évaluer des détections SOC sur Windows / Active Directory.",
    )
    y = deck.callout(
        page,
        "Le cours transmet une méthode reproductible, pas seulement une démo d'outil. Le lab et les règles sont le support. Le savoir réutilisable est le cœur.",
        y,
        52,
    )
    deck.bullets(
        page,
        [
            ("Expliquer le rôle d'un SOC et d'un SIEM dans la détection.", []),
            ("Relier une alerte à une technique MITRE ATT&CK.", []),
            ("Appliquer une méthode simple pour créer une détection.", []),
            ("Distinguer un IOC faible et une détection de comportement (TTP).", []),
            ("Proposer un triage Tier 1 et critiquer une règle (bruit, couverture, limites).", []),
        ],
        y,
        gap=8,
    )

    page = deck.content("La problématique")
    y = deck.lead(page, "Un SOC reçoit beaucoup d'alertes. Une grande partie sont des faux positifs.")
    y = deck.callout(
        page,
        "Comment concevoir, valider et transmettre une démarche de detection engineering pour Windows / Active Directory, qui améliore la pertinence des alertes SIEM tout en maîtrisant les faux positifs ?",
        y,
        68,
    )
    deck.bullets(
        page,
        [
            ("Le point de départ", ["Trop d'alertes, trop peu de méthode pour les écrire et les trier."]),
            (
                "La réponse du cours",
                ["Une méthode en 8 étapes, trois cas Windows / AD, un triage Tier 1 documenté."],
            ),
            (
                "Ce que l'apprenant repart avec",
                ["Un cadre, un catalogue mappé ATT&CK, une SOP de triage, des limites assumées."],
            ),
        ],
        y,
    )

    page = deck.content("Le sujet")
    y = deck.callout(
        page,
        "L'originalité est dans la formulation : passer de « la cybersécurité » à une méthode opérationnelle de detection engineering, enseignable en Mastère 1.",
        y=96,
        height=52,
    )
    deck.bullets(
        page,
        [
            (
                "Ce que le cours est",
                [
                    "Un cours que l'on aurait aimé avoir : écrire une détection, la tester, la tuner.",
                    "De niveau 1re année de Mastère, sur une thématique que le groupe porte.",
                    "Original par l'angle : Windows / AD, SIEM, ATT&CK, faux positifs.",
                ],
            ),
            (
                "Ce que le cours n'est pas",
                [
                    "Un TP dont le seul but est de faire démarrer un SIEM.",
                    "Un cours déjà suivi en B3 ou en M1, ni « l'IA » sans angle.",
                    "Une couverture complète d'ATT&CK, du cloud ou du forensic.",
                ],
            ),
        ],
        y,
        gap=8,
    )

    page = deck.content("Public et prérequis")
    y = deck.lead(page, "Niveau visé : informatique, bac+3 à bac+4 (systèmes, réseaux, cybersécurité).")
    y = deck.callout(
        page,
        "Aucune connaissance préalable en SOC ou en SIEM. L'exercice 1 sert de prise en main Git et Docker.",
        y,
        44,
    )
    deck.bullets(
        page,
        [
            ("Réseaux", ["TCP/IP, ports, protocoles courants."]),
            ("Windows et Active Directory", ["Utilisateurs, groupes, authentification."]),
            ("Ligne de commande", ["Suffisante pour lancer un lab et lire un log."]),
            ("Git et Docker", ["Notions de base. Le premier exercice les remet en main."]),
        ],
        y,
        gap=6,
    )

    page = deck.content("Périmètre")
    y = deck.lead(page, "Le sujet tient parce qu'il est borné. Le mentor valide cette frontière en séance 1.")
    y = deck.table(
        page,
        ["Inclus", "Hors périmètre"],
        [
            ["Windows et Active Directory", "Environnements multi-cloud"],
            ["Un SIEM en lab Docker", "Couverture complète d'ATT&CK"],
            ["3 cas pratiques commentés", "SOAR et threat hunting"],
            ["Triage Tier 1", "Forensic approfondi"],
            ["Mini-rapport d'incident", "Réponse à incident complète"],
        ],
        [320, 320],
        y,
        row_h=28,
        font_size=11,
    )
    page.insert_textbox(
        pymupdf.Rect(40, y + 6, W - 40, y + 48),
        "15 vidéos prévues. Si le temps manque, les cas V9 à V11 fusionnent en 2 vidéos (13 au total). SIEM proposé : Wazuh, simple à lancer avec Docker. Elastic reste possible selon l'avis du mentor.",
        fontname="f",
        fontsize=11,
        color=NAVY,
    )

    deck.section("Le cours")

    page = deck.content("Parcours de l'apprenant")
    y = deck.lead(page, "On apprend en regardant, en lisant, puis en faisant. Durée pour l'apprenant : 10 à 15 h.")
    steps = [
        ("1", "Théorie", "SOC, SIEM, ATT&CK"),
        ("2", "Méthode", "8 étapes, une règle"),
        ("3", "Cas", "4625, LSASS, RDP"),
        ("4", "Transfert", "Triage et rapport"),
    ]
    box_w = 150
    gap = 12
    x = 40
    for num, title, detail in steps:
        page.draw_rect(pymupdf.Rect(x, y, x + box_w, y + 118), color=PALE, fill=PALE, width=0)
        page.draw_rect(pymupdf.Rect(x, y, x + box_w, y + 4), color=CYAN, fill=CYAN, width=0)
        page.insert_text((x + 14, y + 36), num, fontname="fb", fontsize=18, color=CYAN)
        page.insert_text((x + 14, y + 64), title, fontname="fb", fontsize=14, color=NAVY)
        page.insert_textbox(
            pymupdf.Rect(x + 14, y + 74, x + box_w - 10, y + 110),
            detail,
            fontname="f",
            fontsize=11,
            color=NAVY,
        )
        x += box_w + gap
    y += 136
    deck.bullets(
        page,
        [
            ("Vidéo de présentation de l'équipe, 3 min maximum, puis 13 à 15 vidéos de 8 min.", []),
            ("Poly de 40 pages ± 2 : la même matière, écrite, illustrée, réutilisable.", []),
            ("3 exercices Docker / GitHub avec corrigés, puis un examen final avec corrigé.", []),
        ],
        y,
        size=12,
        gap=6,
    )

    page = deck.content("Vidéos — théorie")
    y = deck.lead(page, "Chaque vidéo dure 8 minutes maximum et est sous-titrée. V0 dure 3 minutes.")
    deck.table(
        page,
        ["", "Titre", "Ce que l'apprenant retient"],
        [
            ["V0", "Présentation du cours", "Équipe, public, problème, parcours"],
            ["V1", "Qu'est-ce qu'un SOC ?", "Tiers, cycle de vie d'une alerte"],
            ["V2", "SIEM", "Collecter, corréler, TTD / TTR"],
            ["V3", "MITRE ATT&CK", "Tactique, technique, sous-technique"],
            ["V4", "Kill Chain et Pyramid of Pain", "Détecter un TTP plutôt qu'une IP"],
            ["V5", "Logs Windows", "4624, 4625, 4688, 4732, 7045"],
            ["V6", "Sysmon", "Télémétrie endpoint, accès LSASS"],
            ["V7", "Méthode", "Les 8 étapes, cœur du cours"],
        ],
        [44, 250, 346],
        y,
        row_h=32,
        font_size=10,
    )

    page = deck.content("Vidéos — pratique")
    y = deck.lead(page, "Les cas appliquent la méthode. Le triage et le rapport la rendent professionnelle.")
    deck.table(
        page,
        ["", "Titre", "Ce que l'apprenant retient"],
        [
            ["V8", "Écrire une règle", "Anatomie Sigma / SIEM, GitHub"],
            ["V9", "Brute force 4625", "T1110, alerte, vrai brute vs mot de passe"],
            ["V10", "LSASS", "T1003.001, ProcessAccess, cadre lab"],
            ["V11", "RDP et comptes à risque", "Logon type 10, compte désactivé"],
            ["V12", "Tuning et faux positifs", "FP / FN, seuils, mesure avant / après"],
            ["V13", "Triage Tier 1", "Nothing, Consult, Escalate + SOP"],
            ["V14", "Rapport d'incident", "Résumé, timeline, IoC, recommandations"],
            ["V15", "Synthèse", "Checklist, limites, suite possible"],
        ],
        [44, 230, 366],
        y,
        row_h=32,
        font_size=10,
    )

    page = deck.content("La méthode en 8 étapes")
    y = deck.lead(page, "C'est le fil du cours. La même grille revient dans les vidéos, le poly et les exercices.")
    steps8 = [
        ("1", "Choisir une technique ATT&CK"),
        ("2", "Formuler une hypothèse"),
        ("3", "Identifier les logs"),
        ("4", "Écrire la règle"),
        ("5", "Simuler, de façon contrôlée"),
        ("6", "Vérifier l'alerte"),
        ("7", "Analyser les faux positifs"),
        ("8", "Tuner, documenter, écrire la SOP"),
    ]
    col_w = 310
    for i, (num, label) in enumerate(steps8):
        col = i // 4
        row = i % 4
        x = 40 + col * 340
        yy = y + row * 62
        page.draw_rect(pymupdf.Rect(x, yy, x + col_w, yy + 50), color=PALE, fill=PALE, width=0)
        page.draw_rect(pymupdf.Rect(x, yy, x + 6, yy + 50), color=CYAN, fill=CYAN, width=0)
        page.insert_text((x + 18, yy + 32), num, fontname="fb", fontsize=16, color=CYAN)
        page.insert_text((x + 48, yy + 30), label, fontname="fb", fontsize=12, color=NAVY)

    page = deck.content("Le poly — 40 pages ± 2")
    y = deck.lead(page, "Retranscription illustrée des vidéos : schémas, tableaux, captures, exemples de règles.")
    y = deck.callout(
        page,
        "Règle d'équipe : une vidéo validée, sa section de poly rédigée dans les 7 jours. Rien n'attend janvier.",
        y,
        40,
    )
    deck.table(
        page,
        ["Chapitre", "Pages", "Vidéos", "Contenu"],
        [
            ["Intro et objectifs", "2", "V0", "Public, prérequis, plan"],
            ["SOC et SIEM", "6", "V1–V2", "Définitions, métriques"],
            ["ATT&CK, Kill Chain, PoP", "6", "V3–V4", "Exemples et figures"],
            ["Logs Windows et Sysmon", "6", "V5–V6", "Aide-mémoire Event IDs"],
            ["Méthode et règles", "7", "V7–V8", "8 étapes, anatomie"],
            ["Trois cas", "7", "V9–V11", "Hypothèse, règle, triage"],
            ["Tuning, triage, rapport", "7", "V12–V15", "SOP, template, synthèse"],
        ],
        [200, 70, 80, 290],
        y,
        row_h=28,
        font_size=10,
    )

    page = deck.content("Les 3 exercices")
    y = deck.lead(page, "Reproductibles sur une machine neuve. Corrigé et barème joints à chaque exercice.")
    cards = [
        ("01", "Lab Docker + GitHub", "Cloner, lancer docker compose, vérifier les événements, déposer une capture."),
        ("02", "Règle versionnée", "Choisir une technique, remplir la fiche, écrire la règle, pousser une branche."),
        ("03", "Alerte et triage", "Lancer le scénario, trouver l'alerte, décider Nothing / Consult / Escalate."),
    ]
    x = 40
    for num, title, body in cards:
        page.draw_rect(pymupdf.Rect(x, y, x + 206, y + 210), color=PALE, fill=PALE, width=0)
        page.draw_rect(pymupdf.Rect(x, y, x + 206, y + 4), color=CYAN, fill=CYAN, width=0)
        page.insert_text((x + 16, y + 36), num, fontname="fb", fontsize=16, color=CYAN)
        page.insert_textbox(
            pymupdf.Rect(x + 16, y + 48, x + 190, y + 100),
            title,
            fontname="fb",
            fontsize=13,
            color=NAVY,
        )
        page.insert_textbox(
            pymupdf.Rect(x + 16, y + 108, x + 190, y + 196),
            body,
            fontname="f",
            fontsize=11,
            color=NAVY,
        )
        x += 218

    page = deck.content("L'examen final")
    y = deck.lead(page, "60 à 90 minutes. Sujet, corrigé détaillé et barème sont déposés avec le cours.")
    deck.table(
        page,
        ["Partie", "Poids", "Ce qu'on vérifie"],
        [
            ["A — QCM", "30 %", "SOC, SIEM, ATT&CK, Event IDs, FP / TP"],
            ["B — Mapping", "25 %", "Un log vers une technique, avec justification"],
            ["C — Conception", "25 %", "Hypothèse, logs, ébauche de règle, FP"],
            ["D — Triage", "20 %", "Décision et 5 à 8 lignes de justification"],
        ],
        [160, 80, 400],
        y + 8,
        row_h=48,
        font_size=12,
    )

    page = deck.content("Dépôt Moodle")
    y = deck.lead(page, "Moodle fait foi pour la date et pour la consultation par le jury.")
    deck.bullets(
        page,
        [
            ("Vidéo de présentation (3 min) et texte d'accroche.", []),
            ("Bibliographie commentée : MITRE, Microsoft, Sigma, ANSSI.", []),
            ("13 à 15 vidéos sous-titrées, et le poly de 40 pages ± 2.", []),
            ("3 exercices Docker / GitHub avec corrigés.", []),
            ("Examen final avec corrigé.", []),
            ("Dépôt GitHub : videos, poly, rules, exercises, exam, docker.", []),
        ],
        y,
        gap=8,
    )

    deck.section("La production")

    page = deck.content("Organisation")
    y = deck.lead(page, "Un responsable par livrable. Le suivi ESGI reste individuel : chacun touche à tout.")
    y = deck.table(
        page,
        ["Responsable", "Porte"],
        [
            ["Pédagogie", "Scénarisation, prérequis, cohérence, rapports de séance"],
            ["Théorie / poly", "Chapitres 1 à 4, bibliographie, glossaire"],
            ["Labs", "Docker, GitHub, exercices, corrigés, démos"],
            ["Forme", "Tournage, sous-titres, accroche, examen"],
        ],
        [150, 490],
        y,
        row_h=32,
        font_size=11,
    )
    page.insert_textbox(
        pymupdf.Rect(40, y + 4, W - 40, y + 48),
        "Une vidéo est finie quand le script est relu, la durée tient en 8 min, les sous-titres sont faits et la section de poly correspondante existe, au moins en brouillon.",
        fontname="f",
        fontsize=11,
        color=NAVY,
    )

    page = deck.content("Calendrier")
    y = deck.lead(page, "Quatre séances. Entre chacune, le groupe produit et remet un rapport sous 48 h.")
    deck.table(
        page,
        ["Jalons", "Période", "Objectif"],
        [
            ["Séance 1 — cadrage", "7 sept. → 1 oct.", "Sujet, scénario v1, biblio"],
            ["Séance 2 — scénario", "1 oct. → 1 nov.", "Validation, démo ~30 %"],
            ["Séance 3 — mi-parcours", "1 nov. → 1 déc.", "Démo ~50 %, qualité"],
            ["Séance 4 — final", "1 déc. → 10 janv.", "Cours complet, corrections"],
            ["Dépôt Moodle", "17 janv. 2027, 23h59", "Date provisoire"],
            ["Soutenance", "Février 2027", "30 min + 25 min de questions"],
        ],
        [190, 180, 270],
        y,
        row_h=36,
        font_size=11,
    )

    page = deck.content("Séance 1 — à figer")
    y = deck.lead(page, "Première rencontre avec Adam Rahmi. On pose le sujet, on ne produit pas encore le cours.")
    deck.bullets(
        page,
        [
            ("On présente", ["Sujet, prérequis, scénarisation v1, bibliographie initiale."]),
            (
                "On décide avec le mentor",
                [
                    "Périmètre exact, 13 ou 15 vidéos.",
                    "Stack SIEM : Wazuh ou Elastic.",
                    "Niveau réel des prérequis.",
                ],
            ),
            ("On livre sous 48 h", ["Ce rapport, sur Moodle, au responsable pédagogique et au mentor."]),
        ],
        y,
    )

    page = deck.content("D'ici la séance 2")
    y = deck.lead(page, "La séance 2 fige le sujet. On arrive avec environ 30 % du cours montrable.")
    deck.bullets(
        page,
        [
            ("Figer le plan des vidéos et la scénarisation finale.", []),
            ("Tourner V1 à V4 : SOC, SIEM, ATT&CK, Kill Chain.", []),
            ("Ouvrir le dépôt GitHub et un premier lab Docker.", []),
            ("Rédiger les chapitres 1 et 2 du poly.", []),
            ("Préparer la démo : vidéos, début de poly, ébauche de l'exercice 1.", []),
        ],
        y,
        gap=12,
    )

    page = deck.content("Bibliographie initiale")
    y = deck.lead(page, "Les sources de départ. La liste commentée complète ira sur Moodle avec le cours.")
    deck.bullets(
        page,
        [
            ("MITRE ATT&CK — attack.mitre.org", ["Tactiques, techniques, sous-techniques, mapping des alertes."]),
            ("Microsoft", ["Événements de sécurité Windows et documentation Sysmon."]),
            ("Sigma", ["Format de règles de détection, versionnable, partageable."]),
            ("ANSSI", ["Guides de journalisation et de détection."]),
            ("Références de forme", ["SecNumAcadémie, OpenClassrooms, pour la structure d'un cours."]),
        ],
        y,
        gap=6,
    )

    page = deck.content("Soutenance")
    y = deck.lead(page, "Février 2027. 60 minutes. On défend le cours comme un produit, pas comme un exposé.")
    y = deck.table(
        page,
        ["Temps", "Contenu"],
        [
            ["30 min", "Pourquoi ce cours, objectifs, scénario, extrait vidéo, démo Docker"],
            ["25 min", "Questions du jury et du mentor"],
            ["5 min", "Délibération"],
        ],
        [120, 520],
        y,
        row_h=36,
        font_size=12,
    )
    deck.bullets(
        page,
        [
            ("Note finale supérieure à 10, obligatoire pour le Mastère.", []),
            ("Suivi 40 %  ·  Livrables 40 %  ·  Soutenance 20 %.", []),
            ("Bonus ou malus individuel de ± 10 points, selon l'apport de chacun.", []),
        ],
        y + 8,
        gap=6,
    )

    page = deck.content("En une phrase")
    phrases = [
        ("Vidéos", "On enseigne à l'oral, module par module."),
        ("Poly", "On écrit la même chose, plus détaillée et illustrée."),
        ("Exercices", "L'apprenant fait : Docker, règle, triage."),
        ("Examen", "On vérifie qu'il a compris."),
        ("Séances", "Le mentor valide et corrige le cap."),
        ("Soutenance", "On vend le cours au jury."),
    ]
    y = 98
    for i, (label, phrase) in enumerate(phrases):
        bg = PALE if i % 2 == 0 else WHITE
        page.draw_rect(pymupdf.Rect(40, y, W - 40, y + 52), color=bg, fill=bg, width=0)
        page.draw_rect(pymupdf.Rect(40, y, 43.4, y + 52), color=CYAN, fill=CYAN, width=0)
        page.insert_text((56, y + 22), label, fontname="fb", fontsize=12, color=CYAN)
        page.insert_text((170, y + 22), phrase, fontname="f", fontsize=13, color=NAVY)
        y += 52

    deck.save()
    print(OUT)


def _a4(doc: pymupdf.Document) -> pymupdf.Page:
    page = doc.new_page(width=595, height=842)
    for name, path in FONT.items():
        page.insert_font(fontname=name, fontfile=path)
    page.draw_rect(pymupdf.Rect(0, 0, 595, 842), color=WHITE, fill=WHITE, width=0)
    return page


def _report_header(page: pymupdf.Page, subtitle: str) -> None:
    page.draw_rect(pymupdf.Rect(0, 0, 595, 78), color=NAVY, fill=NAVY, width=0)
    page.draw_rect(pymupdf.Rect(0, 78, 595, 81), color=CYAN, fill=CYAN, width=0)
    page.insert_text((36, 36), "ESGI", fontname="fb", fontsize=16, color=WHITE)
    page.insert_text((36, 50), "école supérieure de", fontname="f", fontsize=6.5, color=CYAN)
    page.insert_text((36, 58), "génie informatique", fontname="f", fontsize=6.5, color=CYAN)
    page.insert_text((150, 36), "Rapport de séance 1", fontname="f", fontsize=20, color=WHITE)
    page.insert_text((150, 58), subtitle, fontname="f", fontsize=11, color=CYAN)


def _report_footer(page: pymupdf.Page, number: int) -> None:
    page.draw_rect(pymupdf.Rect(0, 812, 595, 842), color=NAVY, fill=NAVY, width=0)
    page.insert_text((36, 830), FOOTER_L, fontname="f", fontsize=8, color=WHITE)
    label = str(number)
    page.insert_text(((595 - tlen(label, "f", 8)) / 2, 830), label, fontname="f", fontsize=8, color=WHITE)
    page.insert_text(
        (595 - 36 - tlen(FOOTER_R, "fb", 8), 830),
        FOOTER_R,
        fontname="fb",
        fontsize=8,
        color=WHITE,
    )


def _paragraph(page: pymupdf.Page, text: str, x: float, y: float, width: float, size: float = 10.5, font: str = "f", leading: float = 14) -> float:
    lines = wrap(text, font, size, width)
    for line in lines:
        page.insert_text((x, y), line, fontname=font, fontsize=size, color=NAVY)
        y += leading
    return y


def build_report() -> None:
    doc = pymupdf.open()
    page = _a4(doc)
    _report_header(page, "Cadrage et lancement  —  7 septembre au 1er octobre 2026")
    _report_footer(page, 1)

    y = 98
    meta = [
        ("SÉANCE", "1  —  Cadrage et lancement"),
        ("SUJET", "Detection Engineering pour SOC (Windows / Active Directory)"),
        ("GROUPE", "Victor Tassart, Marwane Zaid, Younès Hannour, Jacques-D'evaldo Tobossou"),
        ("MENTOR", "Adam Rahmi"),
    ]
    page.draw_rect(pymupdf.Rect(36, y, 559, y + 92), color=PALE, fill=PALE, width=0)
    page.draw_rect(pymupdf.Rect(36, y, 39.4, y + 92), color=CYAN, fill=CYAN, width=0)
    yy = y + 18
    for label, value in meta:
        page.insert_text((52, yy), label, fontname="fb", fontsize=8, color=CYAN)
        page.insert_text((120, yy), value, fontname="f", fontsize=10, color=NAVY)
        yy += 20
    y += 110

    page.insert_text((36, y), "1. Bilan des actions réalisées", fontname="fb", fontsize=13, color=NAVY)
    y += 20
    y = _paragraph(
        page,
        "Première séance du projet. Le groupe a préparé le sujet, une première scénarisation et la bibliographie initiale, pour les faire valider par le mentor.",
        36,
        y,
        523,
    )
    y += 8
    for item in (
        "Sujet retenu : concevoir, tester et évaluer des détections SOC sur Windows / Active Directory, avec un SIEM et MITRE ATT&CK.",
        "Scénarisation v1 : 1 vidéo de présentation (3 min), 15 vidéos de cours (8 min), un poly d'environ 40 pages, 3 exercices Docker / GitHub avec corrigés, un examen avec corrigé.",
        "Parcours apprenant : théorie, méthode, cas pratiques, triage.",
        "Bibliographie de départ : MITRE ATT&CK, documentation Microsoft (événements Windows, Sysmon), Sigma, guides ANSSI.",
    ):
        page.draw_rect(pymupdf.Rect(40, y - 7, 46, y - 1), color=CYAN, fill=CYAN, width=0)
        y = _paragraph(page, item, 54, y, 505, size=10.5, leading=13.5)
        y += 6

    y += 8
    page.insert_text((36, y), "2. Décisions prises lors de la séance", fontname="fb", fontsize=13, color=NAVY)
    y += 20
    y = _paragraph(
        page,
        "Reformulation retenue avec le mentor : transmettre une démarche de detection engineering, pas une simple démonstration d'outil. Le lab sert de preuve. Le cours sert de transfert.",
        36,
        y,
        523,
    )
    y += 6
    page.insert_text(
        (36, y + 4),
        "Le détail du périmètre, du SIEM et des prérequis est sur la page suivante.",
        fontname="fi",
        fontsize=10,
        color=MUTED,
    )

    page = _a4(doc)
    _report_header(page, "Cadrage et lancement  —  suite")
    _report_footer(page, 2)
    y = 104
    page.insert_text((36, y), "Décisions (suite)", fontname="fb", fontsize=13, color=NAVY)
    y += 18
    decisions = [
        ("Inclus", "Windows et Active Directory, un SIEM en Docker, 3 cas, triage Tier 1, mini-rapport d'incident."),
        ("Exclu", "Multi-cloud, couverture complète d'ATT&CK, SOAR, threat hunting, forensic approfondi."),
        ("Vidéos", "15 prévues. Si le temps manque, les cas V9 à V11 fusionnent en 2 vidéos, soit 13 au total."),
        ("SIEM", "Wazuh proposé, simple à lancer avec Docker. Elastic reste possible selon l'avis du mentor."),
        ("Prérequis", "Réseaux, notions Windows / AD, ligne de commande, bases Git et Docker. Aucun prérequis SOC ou SIEM."),
        ("Niveau", "Informatique, bac+3 à bac+4. Public : systèmes, réseaux ou cybersécurité."),
    ]
    for label, text in decisions:
        page.insert_text((36, y), label, fontname="fb", fontsize=10.5, color=NAVY)
        y = _paragraph(page, text, 120, y, 439, size=10.5, leading=13.5)
        y += 8

    y += 6
    page.insert_text((36, y), "3. Prochaines étapes", fontname="fb", fontsize=13, color=NAVY)
    y += 18
    y = _paragraph(
        page,
        "D'ici la séance 2 (1er octobre au 1er novembre 2026), pour arriver avec environ 30 % du cours montrable :",
        36,
        y,
        523,
    )
    y += 6
    for item in (
        "Figer le plan des vidéos et la scénarisation finale.",
        "Tourner V1 à V4 : SOC, SIEM, ATT&CK, Kill Chain et Pyramid of Pain.",
        "Ouvrir le dépôt GitHub et un premier brouillon Docker.",
        "Commencer les chapitres 1 et 2 du poly.",
        "Préparer la démonstration : vidéos, début de poly, ébauche de l'exercice 1.",
    ):
        page.draw_rect(pymupdf.Rect(40, y - 7, 46, y - 1), color=CYAN, fill=CYAN, width=0)
        y = _paragraph(page, item, 54, y, 505, size=10.5, leading=13.5)
        y += 4

    y += 10
    page.insert_text((36, y), "4. Points de blocage / questions ouvertes", fontname="fb", fontsize=13, color=NAVY)
    y += 18
    for item in (
        "Confirmer le SIEM avec le mentor : Wazuh ou Elastic.",
        "Trancher 15 vidéos ou 13, selon le rythme de production.",
        "Attribuer nommément les quatre responsabilités : pédagogie, poly, labs, forme.",
        "Accès Moodle annoncé en septembre : à confirmer avant le dépôt de ce rapport.",
    ):
        page.draw_rect(pymupdf.Rect(40, y - 7, 46, y - 1), color=CYAN, fill=CYAN, width=0)
        y = _paragraph(page, item, 54, y, 505, size=10.5, leading=13.5)
        y += 4

    doc.save(REPORT)
    doc.close()
    print(REPORT)


if __name__ == "__main__":
    build()
    build_report()
