import pygame
import random
import math

pygame.init()

LARGEUR = 600
HAUTEUR = 600
HUD = 80                          # hauteur du panneau en bas
ZONE_JEU = HAUTEUR - HUD          # la pomme ne depasse jamais cette limite
TAILLE_CASE = 20

screen = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Snake Turbo")
clock = pygame.time.Clock()
font = pygame.font.SysFont("monospace", 22)
font_grand = pygame.font.SysFont("monospace", 48)
font_bouton = pygame.font.SysFont("monospace", 20)


def couleur_arc_en_ciel(index, temps):
    offset = temps + index * 0.3
    r = int(127 + 127 * math.sin(offset))
    g = int(127 + 127 * math.sin(offset + 2.094))
    b = int(127 + 127 * math.sin(offset + 4.189))
    return (r, g, b)


def nouvelle_pomme():
    return [
        random.randint(0, (LARGEUR // TAILLE_CASE) - 1) * TAILLE_CASE,
        random.randint(0, (ZONE_JEU // TAILLE_CASE) - 1) * TAILLE_CASE,
    ]


def lire_meilleur_score():
    try:
        with open("meilleur_score.txt", "r") as f:
            return int(f.read())
    except:
        return 0


def sauvegarder_score(score):
    with open("meilleur_score.txt", "w") as f:
        f.write(str(score))


def reinitialiser():
    return [[300, 240], [280, 240], [260, 240]], [TAILLE_CASE, 0], 0, 10


def dessiner_bouton(texte, x, y, largeur, hauteur, survol):
    couleur_fond = (60, 60, 80) if not survol else (90, 90, 130)
    couleur_bord = (100, 100, 200) if not survol else (150, 150, 255)
    pygame.draw.rect(screen, couleur_fond, (x, y, largeur, hauteur), border_radius=10)
    pygame.draw.rect(screen, couleur_bord, (x, y, largeur, hauteur), 2, border_radius=10)
    label = font_bouton.render(texte, True, (255, 255, 255))
    screen.blit(label, (x + largeur // 2 - label.get_width() // 2,
                        y + hauteur // 2 - label.get_height() // 2))


def dessiner_hud(score, meilleur, fps, temps):
    # Fond du panneau
    pygame.draw.rect(screen, (20, 20, 35), (0, ZONE_JEU, LARGEUR, HUD))
    pygame.draw.line(screen, (60, 60, 100), (0, ZONE_JEU), (LARGEUR, ZONE_JEU), 2)

    # Score avec couleur arc-en-ciel
    couleur_score = couleur_arc_en_ciel(0, temps)
    t_score = font.render(f"Score", True, (150, 150, 180))
    t_score_val = font.render(str(score), True, couleur_score)

    t_best = font.render(f"Meilleur", True, (150, 150, 180))
    t_best_val = font.render(str(meilleur), True, (255, 200, 0))

    t_fps = font.render(f"FPS", True, (150, 150, 180))
    t_fps_val = font.render(str(fps), True, (0, 220, 100))

    # Colonne Score
    screen.blit(t_score, (60 - t_score.get_width() // 2, ZONE_JEU + 12))
    screen.blit(t_score_val, (60 - t_score_val.get_width() // 2, ZONE_JEU + 38))

    # Separateur
    pygame.draw.line(screen, (60, 60, 100), (200, ZONE_JEU + 15), (200, HAUTEUR - 15), 1)

    # Colonne Meilleur
    screen.blit(t_best, (310 - t_best.get_width() // 2, ZONE_JEU + 12))
    screen.blit(t_best_val, (310 - t_best_val.get_width() // 2, ZONE_JEU + 38))

    # Separateur
    pygame.draw.line(screen, (60, 60, 100), (430, ZONE_JEU + 15), (430, HAUTEUR - 15), 1)

    # Colonne FPS
    screen.blit(t_fps, (530 - t_fps.get_width() // 2, ZONE_JEU + 12))
    screen.blit(t_fps_val, (530 - t_fps_val.get_width() // 2, ZONE_JEU + 38))


meilleur = lire_meilleur_score()
serpent, direction, score, vitesse = reinitialiser()
pomme = nouvelle_pomme()
compteur = 0
game_over = False
temps = 0

# Dimensions du bouton Rejouer
btn_x = LARGEUR // 2 - 100
btn_y = 370
btn_w = 200
btn_h = 50

running = True
while running:
    mx, my = pygame.mouse.get_pos()
    survol_bouton = btn_x < mx < btn_x + btn_w and btn_y < my < btn_y + btn_h

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if game_over and event.key == pygame.K_r:
                serpent, direction, score, vitesse = reinitialiser()
                pomme = nouvelle_pomme()
                compteur = 0
                game_over = False
            if not game_over:
                if event.key == pygame.K_UP and direction[1] == 0:
                    direction = [0, -TAILLE_CASE]
                if event.key == pygame.K_DOWN and direction[1] == 0:
                    direction = [0, TAILLE_CASE]
                if event.key == pygame.K_LEFT and direction[0] == 0:
                    direction = [-TAILLE_CASE, 0]
                if event.key == pygame.K_RIGHT and direction[0] == 0:
                    direction = [TAILLE_CASE, 0]

        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_over and survol_bouton:
                serpent, direction, score, vitesse = reinitialiser()
                pomme = nouvelle_pomme()
                compteur = 0
                game_over = False

    if not game_over:
        temps += 0.05
        compteur += 1

        if compteur >= vitesse:
            compteur = 0
            nouvelle_tete = [serpent[0][0] + direction[0],
                             serpent[0][1] + direction[1]]

            if (nouvelle_tete[0] < 0 or nouvelle_tete[0] >= LARGEUR or
                    nouvelle_tete[1] < 0 or nouvelle_tete[1] >= ZONE_JEU):
                game_over = True

            elif nouvelle_tete in serpent:
                game_over = True

            else:
                serpent.insert(0, nouvelle_tete)
                if serpent[0] == pomme:
                    score += 10
                    vitesse = max(4, vitesse - 1)
                    pomme = nouvelle_pomme()
                else:
                    serpent.pop()

        if game_over and score > meilleur:
            meilleur = score
            sauvegarder_score(meilleur)

    screen.fill((15, 15, 25))

    if game_over:
        t1 = font_grand.render("GAME OVER", True, (220, 50, 50))
        t2 = font.render(f"Score: {score}     Meilleur: {meilleur}", True, (255, 255, 255))
        screen.blit(t1, (LARGEUR // 2 - t1.get_width() // 2, 200))
        screen.blit(t2, (LARGEUR // 2 - t2.get_width() // 2, 300))
        dessiner_bouton("Rejouer", btn_x, btn_y, btn_w, btn_h, survol_bouton)

        hint = font_bouton.render("ou appuie sur R", True, (80, 80, 100))
        screen.blit(hint, (LARGEUR // 2 - hint.get_width() // 2, 435))

    else:
        pygame.draw.rect(screen, (220, 50, 50),
                         (pomme[0], pomme[1], TAILLE_CASE - 2, TAILLE_CASE - 2))

        for i, segment in enumerate(serpent):
            couleur = (255, 255, 255) if i == 0 else couleur_arc_en_ciel(i, temps)
            pygame.draw.rect(screen, couleur,
                             (segment[0], segment[1], TAILLE_CASE - 2, TAILLE_CASE - 2))

    dessiner_hud(score, meilleur, int(clock.get_fps()), temps)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
