#!/usr/bin/python
from ais import myAI
import tkinter
import tkinter.messagebox
# window
window = tkinter.Tk()
window.title('五子棋')
# label
text = tkinter.StringVar()
text.set('start!')
label = tkinter.Label(window, textvariable=text)
# canvas
canvas = tkinter.Canvas(window)
canvas.config(width=750, height=750)
width = 50
for i in range(15):
    for j in range(15):
        myAI.list_all.append((i, j))
lastStep = ()


def draw(blockColor,  pos, lineColor):
    canvas.create_rectangle(
        pos[0]*width, pos[1]*width, (pos[0] + 1)*width, (pos[1] + 1)*width, fill=blockColor, outline=lineColor)
    canvas.update()


def handleClick(event):
    global lastStep
    tmp = (int(event.x / 50), int(event.y / 50))
    if tmp not in myAI.listAI and tmp not in myAI.listHuman:
        text.set('thinking')
        myAI.listHuman.append(tmp)
        draw('black', tmp, 'red')
        if lastStep:
            draw('white', lastStep, 'blue')
        lastStep = tmp
        x, y = myAI.ai(myAI.listAI, myAI.listHuman, myAI.list_all)
        myAI.listAI.append((x, y))
        draw('white', (x, y), 'red')
        if lastStep:
            draw('black', lastStep, 'blue')
        lastStep = (x, y)
        text.set('it\'s your turn.')
        if myAI.game_win(myAI.listAI):
            tkinter.messagebox.showinfo('游戏结束', 'AI胜利')
            exit(0)
        elif myAI.game_win(myAI.listHuman):
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
    imFirst = tkinter.messagebox.askokcancel('提示', '是否由您先手？')
    if not imFirst:
        x, y = myAI.ai(myAI.listAI, myAI.listHuman, myAI.list_all)
        myAI.listAI.append((x, y))
        draw('white', (x, y), 'red')
    canvas.bind('<Button-1>', handleClick)
    window.mainloop()


if __name__ == '__main__':
    main()
