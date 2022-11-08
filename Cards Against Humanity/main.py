import pygame, sys, random

pygame.init()
Font = pygame.font.Font(None, 24)


def render_textrect(string, font, rect, text_color, background_color, justification=0):
    final_lines = []
    requested_lines = string.splitlines()
    for requested_line in requested_lines:
        if font.size(requested_line)[0] > rect.width:
            words = requested_line.split(' ')
            accumulated_line = ""
            for word in words:
                test_line = accumulated_line + word + " " 
                if font.size(test_line)[0] < rect.width:
                    accumulated_line = test_line 
                else: 
                    final_lines.append(accumulated_line) 
                    accumulated_line = word + " " 
            final_lines.append(accumulated_line)
        else: 
            final_lines.append(requested_line) 
    surface = pygame.Surface(rect.size) 
    surface.fill(background_color) 
    accumulated_height = 0 
    for line in final_lines: 
        if line != "":
            tempsurface = font.render(line, 1, text_color)
            if justification == 0:
                surface.blit(tempsurface, (0, accumulated_height))
            elif justification == 1:
                surface.blit(tempsurface, ((rect.width - tempsurface.get_width()) / 2, accumulated_height))
            elif justification == 2:
                surface.blit(tempsurface, (rect.width - tempsurface.get_width(), accumulated_height))
        accumulated_height += font.size(line)[1]
    return surface

def load_file(file_name):
    phrases = []
    with open(file_name + ".txt", encoding = "utf8") as file_in:
        for line in file_in:
            line = line.strip('\n')
            phrases.append(line)
    return phrases

BlackCards = load_file("black_cards")
WhiteCards = load_file("white_cards")


def SelectBlackCard(previous = "null"):
    card = BlackCards[random.randint(0, len(BlackCards))]
    if not previous == "null":
        BlackCards.append(previous)
    return card
def SelectUsersCards():
    cards = [WhiteCards[random.randint(0, len(WhiteCards))]]
    for i in range(4):
        card = WhiteCards[random.randint(0, len(WhiteCards))]
        while card in cards:
            card = WhiteCards[random.randint(0, len(WhiteCards))]
        cards.append(card)
    for card in cards:
        WhiteCards.remove(card)
    return cards
def swapUserCard(previous_card):
    card = WhiteCards[random.randint(0, len(WhiteCards))]
    WhiteCards.remove(card)
    WhiteCards.append(previous_card)
    return card

def rect_collision(rect, point):
    if point[0] > rect[0] and point[0] < rect[0] + rect[2]:
        if point[1] > rect[1] and point[1] < rect[1] + rect[3]:
            return True
    return False

WIDTH, HEIGHT = int(600 * 1.5), int(450 * 1.5)
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cards Against Humanity")

BlackCardString = SelectBlackCard()
UsersCardsStrings = SelectUsersCards()

class visualCard:
    def __init__(self, position, text):
        self.x, self.y = position[0], position[1]
        self.w, self.h = (WIDTH - 100) / 5, (HEIGHT / 2.5)
        self.colour, self.roundness, self.text_colour = (0, 0, 0), 15, (255, 255, 255)
        self.default = (self.x, self.y, self.w, self.h)
        self.text = text
    def draw(self):
        self.drawBackground()
        self.drawText()
    def drawText(self):
        textRect = pygame.Rect((self.x - self.w / 2 + self.roundness, self.y - self.h / 2 + self.roundness, self.w - self.roundness * 2, self.h - self.roundness * 2))
        surf = render_textrect(self.text, Font, textRect, self.text_colour, self.colour, 0)
        if surf:
            window.blit(surf, textRect.topleft)
    def drawBackground(self):
        pygame.draw.rect(window, self.colour, (self.x - self.w / 2, (self.y - self.h / 2) + self.roundness, self.w, self.h - self.roundness * 2))
        pygame.draw.rect(window, self.colour, ((self.x - self.w / 2) + self.roundness, self.y - self.h / 2, self.w - self.roundness * 2, self.h))

        pygame.draw.circle(window, self.colour, (self.x - self.w / 2 + self.roundness, self.y - self.h / 2 + self.roundness), self.roundness)
        pygame.draw.circle(window, self.colour, (self.x + self.w / 2 - self.roundness, self.y - self.h / 2 + self.roundness), self.roundness)
        pygame.draw.circle(window, self.colour, (self.x + self.w / 2 - self.roundness, self.y + self.h / 2 - self.roundness), self.roundness)
        pygame.draw.circle(window, self.colour, (self.x - self.w / 2 + self.roundness, self.y + self.h / 2 - self.roundness), self.roundness)

BlackCard = visualCard((WIDTH / 2, HEIGHT / 4), SelectBlackCard())

class WhiteCard(visualCard):
    def __init__(self, position, text):
        super().__init__(position, text)
        self.colour, self.text_colour = (255, 255, 255), (0, 0, 0)
        self.hovered_y, self.target_y = self.y - 30, self.y
    def handle_hover(self):
        if rect_collision((self.x - self.w / 2, self.y - self.h / 2, self.w, self.h), pygame.mouse.get_pos()):
            self.target_y = self.hovered_y
        else:
            self.target_y = self.default[1]
        self.y += (self.target_y - self.y) * 0.1
    def handle_press(self):
        if rect_collision((self.x - self.w / 2, self.y - self.h / 2, self.w, self.h), pygame.mouse.get_pos()):
            self.swap()
    def swap(self):
        self.text = swapUserCard(self.text)
        BlackCardString = SelectBlackCard(previous = BlackCard.text)
        BlackCard.text = BlackCardString
        
VisualWhiteCards = []
for i in range(5):
    VisualWhiteCards.append(WhiteCard(((WIDTH / 5) * (i + 0.5), (HEIGHT / 4) * 3), UsersCardsStrings[i]))

def handle_swaps():
    for c in VisualWhiteCards:
        c.handle_press()

while True:
    window.fill((50, 50, 50))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            handle_swaps()
    BlackCard.draw()
    for c in VisualWhiteCards:
        c.draw()
        c.handle_hover()
    pygame.display.update()


