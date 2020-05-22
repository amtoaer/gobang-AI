#!/usr/bin/python
from ais import demo
import tkinter
import tkinter.messagebox
window = tkinter.Tk()
window.title('五子棋')
text = tkinter.StringVar()
text.set('start!')
label = tkinter.Label(window, textvariable=text)
canvas = tkinter.Canvas(window)
canvas.config(width=750, height=750)
width = 50
for i in range(15):
    for j in range(15):
        demo.list_all.append((i, j))


def draw(color, pos):
    canvas.create_rectangle(
        pos[0]*width, pos[1]*width, (pos[0] + 1)*width, (pos[1] + 1)*width, fill=color, outline='blue')
    canvas.update()


def handleClick(event):
    tmp = (int(event.x / 50), int(event.y / 50))
    if tmp not in demo.listAIAndHuman:
        text.set('thinking')
        demo.listHuman.append(tmp)
        draw('black', tmp)
        x, y = demo.ai(demo.listAI, demo.listHuman, demo.list_all)
        demo.listAI.append((x, y))
        draw('white', (x, y))
        text.set('it\'s your turn.')
        if demo.game_win(demo.listAI):
            tkinter.messagebox.showinfo('游戏结束', 'AI胜利')
            exit(0)
        elif demo.game_win(demo.listHuman):
            tkinter.messagebox.showinfo('游戏结束', '人类胜利')
            exit(0)


def main():
    for x in range(15):
        for y in range(15):
            canvas.create_rectangle(
                x*width, y*width, (x + 1)*width, (y + 1)*width, fill="orange", outline='black')
    canvas.pack()
    label.pack()
    canvas.focus_set()
    canvas.bind('<Button-1>', handleClick)
    window.mainloop()


if __name__ == '__main__':
    main()
