import socket
import tkinter
import threading
import io
import pickle
import hashlib
import time
from PIL import Image
import os

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverName = 'localhost'
serverPort = 12000
clientSocket.bind(('0.0.0.0', 59583))

ACK = 1
expectedseqnumz = 1
ACK = 1
ack = []
recName = ''
name = ''
count = 0
st = 0
rfs = 0
total_p = 0
rounded_p = 0
base = 1
winz = []
lastackreceived = 0
print('Beginning handshake process...')
clientSocket.sendto('SYN'.encode('utf-8'), (serverName, serverPort))
print('Sent SYN to Server')
msgs, address = clientSocket.recvfrom(4096)
if msgs.decode('utf-8') == 'ACK':
    print('ACK received from Server.\nConnection established!')
else:
    print('Handshake process interrupted. Exiting.')
    quit()

def receive():
    global st
    global total_p
    global rounded_p
    global base
    global winz
    global lastackreceived
    global expectedseqnumz
    global lastpktreceivedz
    boo = True
    bo = True
    while True:
        try:
            rcvpkt = []
            global recName
            msgs, address = clientSocket.recvfrom(4096)  # 1098
            if isinstance(msgs, bytes):
                if msgs[:2].decode('utf-8', 'surrogatepass') == '`!':
                    clientSocket.settimeout(5)
                    try:
                        msgs = msgs[2:]
                        rcvpkt = pickle.loads(msgs.decode('utf-8').encode('latin1'))
                        c = rcvpkt[-1]
                        del rcvpkt[-1]
                        h = hashlib.md5()
                        h.update(pickle.dumps(rcvpkt))
                        if c == h.digest():
                            print("Received ack for", rcvpkt[0])
                            # slide window and reset timer
                            while rcvpkt[0] > base and winz:
                                lastackreceived = time.time()
                                del winz[0]
                                base = base + 1 # Might have to change
                        else:
                            print("error detected")
                        varzy.set(1)
                        clientSocket.settimeout(None)
                    except:
                        if time.time() - lastackreceived > 0.01:
                            for i in winz:
                                co = pickle.dumps(i)
                                co = co.decode('latin1')
                                clientSocket.sendto(('~~' + co).encode('utf-8'), (serverName, serverPort))
                elif msgs[:2].decode('utf-8', 'surrogatepass') == '~~':
                    clientSocket.settimeout(5)
                    try:
                        if bo:
                            msg_list.insert(tkinter.END, 'File download has started!')
                            imgs = open(my_ftop2.get(), 'wb')
                            endoffile = False
                            lastpktreceivedz = time.time()
                            starttime = time.time()
                            bo = False
                        msgs = msgs[2:]
                        rcvpkt = pickle.loads(msgs.decode('utf-8').encode('latin1'))
                        c = rcvpkt[-1]
                        del rcvpkt[-1]
                        h = hashlib.md5()
                        h.update(pickle.dumps(rcvpkt))
                        if c == h.digest():
                            if rcvpkt[0] == expectedseqnumz:
                                print("Received inorder", expectedseqnumz)
                                if rcvpkt[1]:
                                    imgs.write(rcvpkt[1])
                                    total_p = total_p + ((1096 / rfs) * 100)
                                    if round(total_p) != rounded_p and round(total_p) % 10 == 0:
                                        msg_list.insert(tkinter.END, 'File at ' + str(round(total_p)) + '%')
                                        rounded_p = round(total_p)
                                else:
                                    endoffile = True
                                    imgs.close()
                                    bo = True
                                    total_p = 0
                                    rounded_p = 0
                                    endtime = time.time()
                                    lastpktreceivedz = 0
                                    expectedseqnumz = 1
                                    print('FILE TRANSFER SUCCESSFUL')
                                    print("TIME TAKEN ", str(endtime - starttime))
                                    clientSocket.settimeout(None)
                                    msg_list.insert(tkinter.END,
                                                    'File was successfully uploaded! File is located at: ' + my_ftop2.get())
                                    my_ftop2.set('')
                                if bo == False:
                                    expectedseqnumz = expectedseqnumz + 1 # Might have to change
                                    sndpkt = []
                                    sndpkt.append(expectedseqnumz)
                                    h = hashlib.md5()
                                    h.update(pickle.dumps(sndpkt))
                                    sndpkt.append(h.digest())
                                    con = pickle.dumps(sndpkt)
                                    con = con.decode('latin1')
                                    # serverSocket.sendto('hello my friend'.encode('utf-8'), ('127.0.0.1', 59583))
                                    clientSocket.sendto(('`!' + con).encode('utf-8'), (serverName, serverPort))
                                    print("New Ack", expectedseqnumz)
                            else:
                                print("Received out of order", rcvpkt[0])
                                sndpkt = []
                                sndpkt.append(expectedseqnumz)
                                h = hashlib.md5()
                                h.update(pickle.dumps(sndpkt))
                                sndpkt.append(h.digest())
                                con = pickle.dumps(sndpkt)
                                con = con.decode('latin1')
                                clientSocket.sendto(('`!' + con).encode('utf-8'), (serverName, serverPort))
                                print("Ack", expectedseqnumz)
                        else:
                            print("error detected")
                    except:
                        if endoffile:
                            if time.time() - lastpktreceivedz > 3:
                                print('Yooo')
                elif msgs[:2].decode('utf-8', 'surrogatepass') == '~`':
                    if boo:
                        st = st + 1
                        img = open('new_picture_clientside_Comp3825App' + str(st) + '.jpg', 'wb')
                        boo = False
                    msgs = msgs[2:]
                    if msgs != b'End':
                        img.write(msgs)
                    if msgs == b'End':
                        img.close()
                        msg_list.insert(tkinter.END, recName + ' Shared a picture with you! The file is located at new_pictures_clientside_Comp3825App' + str(st) + '.jpg')
                        top2 = tkinter.Toplevel(window)
                        top2.geometry('%dx%d%+d%+d' % (500, 100, 850, 125))
                        top2.title('Picture')
                        msg1 = tkinter.Message(top2, text='Click on the link below to see the picture that was sent to you. The file path of the picture has been saved in the chat logs.', width=500)
                        msg1.pack()
                        panel = tkinter.Label(top2, text='new_picture_clientside_Comp3825App' + str(st) + '.jpg', fg='red', cursor='hand2')
                        panel.pack()
                        panel.bind('<Button-1>', showphotos)
                        button01 = tkinter.Button(top2, text='Dismiss', command=top2.destroy)
                        button01.pack()
                        boo = True
                elif msgs.decode('utf-8', 'surrogatepass')[:3] == '~!S':
                    rfs = int(msgs.decode('utf-8', 'surrogatepass')[3:])
                    top3 = tkinter.Toplevel(window)
                    top3.geometry('%dx%d%+d%+d' % (500, 100, 850, 125))
                    top3.title('File Path')
                    msg2 = tkinter.Message(top3, text=recName[:-2] + ' is about to send you a file. Please specify the file directory and name of the file.', width=500)
                    msg2.pack()
                    my_ftop2.set('Enter valid file path here')
                    entry_field3 = tkinter.Entry(top3, textvariable=my_ftop2, width=30)
                    entry_field3.pack()
                    button = tkinter.Button(top3, text='Send', command=lambda: [top3.destroy(), var.set(1)])
                    button.pack()
                    button.wait_variable(var)
                    clientSocket.sendto('~!'.encode('utf-8', 'surrogatepass'), (serverName, serverPort))
                elif msgs.decode('utf-8', 'surrogatepass')[-3:] == '```':
                    recName = msgs.decode('utf-8', 'surrogatepass')[:-3] + ': '
                    msg_list.insert(tkinter.END, recName[:-2] + ' has entered the chat!')
                elif msgs.decode('utf-8', 'surrogatepass') == '~!':
                    varz.set(1)
                    msg_list.insert(tkinter.END, varz)
                elif msgs[-2:].decode('utf-8', 'surrogatepass') == '`~':
                    msgs = msgs[:-2]
                    msg_list.insert(tkinter.END, recName + msgs.decode('utf-8', 'surrogatepass'))
                else:
                    msg_list.insert(tkinter.END, recName + msgs.decode('utf-8', 'surrogatepass'))
        except OSError:
            break


def send(event=None):
    global name, count
    if msg_list.size() == 1 or count == 0:
        name = my_msg.get()
        msg_list.insert(tkinter.END, 'Welcome ' + name + '!')
        my_msg.set('')
        clientSocket.sendto((name + '```').encode('utf-8', 'surrogatepass'), (serverName, serverPort))
        count = 1
        if name == "{quit}":
            clientSocket.close()
            window.quit()
    else:
        msgs = my_msg.get()
        if msgs == "{quit}":
            msg_list.insert(tkinter.END, name + ': Exiting chat room...')
            # clientSocket.sendto((name + ' exited the chat room').encode('utf-8', 'surrogatepass'), ('localhost', 12000))
            clientSocket.close()
            window.quit()
            chat1 = open('projectChatLogsClient.txt', 'w')
            for i in enumerate(msg_list.get(0, tkinter.END)):
                try:
                    chat1.write((str(i) + '\n'))  #.encode('utf-8').decode('utf-8')
                except:
                    nn = 0
            chat1.close()
            window.destroy()
        else:
            if msgs[-2:] == '`~':
                msg_list.insert(tkinter.END, name + ': ' + msgs[:-2])
            else:
                msg_list.insert(tkinter.END, name + ': ' + msgs)
            my_msg.set("")
            clientSocket.sendto(msgs.encode('utf-8', 'surrogatepass'), (serverName, serverPort))


def showphotos(event=None):
    global st
    ms = 'new_picture_clientside_Comp3825App' + str(st) + '.jpg'
    im = Image.open(ms)
    im.show()


def photos():
    top = tkinter.Toplevel(window)
    top.geometry('%dx%d%+d%+d' % (500, 100, 850, 125))
    top.title('Enter a file name')
    msg = tkinter.Message(top, text='Enter a valid file path for your picture location and press Send.', width=500)
    msg.pack()
    my_ms.set('Enter valid file name here')
    entry_field2 = tkinter.Entry(top, textvariable=my_ms, width=30)
    entry_field2.pack()
    button = tkinter.Button(top, text='Send', command=lambda: [top.destroy(), photo()])
    button.pack()


def photo():
    ms = my_ms.get()
    msg_list.insert(tkinter.END, 'Sending Picture...')
    try:
        data = open(ms, 'rb')
        while True:
            strng = data.read(1024)
            if not strng:
                clientSocket.sendto('~`End'.encode('utf-8'), (serverName, serverPort))
                break
            img = '~`'
            clientSocket.sendto(img.encode('utf-8') + strng, (serverName, serverPort))
        data.close()
        msg_list.insert(tkinter.END, 'Picture was sent! You sent the picture located at ' + ms)
        msg_list.insert(tkinter.END, name + ': ' + 'Shared a picture!')
        top2 = tkinter.Toplevel(window)
        top2.geometry('%dx%d%+d%+d' % (500, 100, 850, 125))
        top2.title('Picture')
        msg1 = tkinter.Message(top2, text='Click on the link below to see the picture you sent. The file path of the picture has been saved in the chat logs.', width=500)
        msg1.pack()
        panel = tkinter.Label(top2, text=ms, fg='red', cursor='hand2')
        panel.pack()
        panel.bind('<Button-1>', showphoto)
        button01 = tkinter.Button(top2, text='Dismiss', command=lambda: [my_ms.set(''), top2.destroy()])
        button01.pack()
    except FileNotFoundError:
        msg_list.insert(tkinter.END, 'An error occurred. Please try again.')
        topp = tkinter.Toplevel(window)
        topp.geometry('%dx%d%+d%+d' % (500, 100, 850, 125))
        topp.title('Error Message')
        msg = tkinter.Message(topp, text='The file path you entered is not correct. Please try again.', width=500)
        msg.pack()
        button = tkinter.Button(topp, text='Dismiss', command=topp.destroy)
        button.pack()


def showphoto(event=None):
    ms = my_ms.get()
    im = Image.open(ms)
    im.show()


def files(event=None):
    ftop = tkinter.Toplevel(window)
    ftop.geometry('%dx%d%+d%+d' % (500, 100, 850, 125))
    ftop.title('Enter a file name')
    msg = tkinter.Message(ftop, text='Enter a valid file path for your file location and press Send.', width=500)
    msg.pack()
    my_ms.set('Enter valid file name here')
    entry_field2 = tkinter.Entry(ftop, textvariable=my_fms, width=30)
    entry_field2.pack()
    button = tkinter.Button(ftop, text='Send', command=lambda: [ftop.destroy(), file()])
    button.pack()


def file(event=None):
    global base
    global winz
    global lastackreceived
    base = 1
    nextSeqnum = 1
    windowSize = 7
    winz = []
    fs = my_fms.get()
    msg_list.insert(tkinter.END, 'Sending File...')
    try:
        data = open(fs, 'rb')
        total_len = os.path.getsize(fs)
        clientSocket.sendto(('~!S' + str(total_len)).encode('utf-8'), (serverName, serverPort))
        msg_list.wait_variable(varz)
        strng = data.read(1096)  ### Was at 1024
        done = False
        lastackreceived = time.time()
        total_progress = 0
        rounded_progress = 0
        while not done or winz:
            if (nextSeqnum < base + windowSize) and not done:
                total_progress = total_progress + ((1096 / total_len) * 100)
                if round(total_progress) != rounded_progress and round(total_progress) % 10 == 0:
                    msg_list.insert(tkinter.END, 'File at ' + str(round(total_progress)) + '%')
                    rounded_progress = round(total_progress)
                sndpkt = []
                sndpkt.append(nextSeqnum)
                sndpkt.append(strng)
                h = hashlib.md5()
                h.update(pickle.dumps(sndpkt))
                sndpkt.append(h.digest())
                conv = pickle.dumps(sndpkt)
                conv = conv.decode('latin1')
                clientSocket.sendto(('~~' + conv).encode('utf-8'), (serverName, serverPort))
                msg_list.wait_variable(varzy)
                print("Sent data", nextSeqnum)
                nextSeqnum = nextSeqnum + 1
                if not strng:
                    msg_list.insert(tkinter.END, 'File was successfully sent!')
                    done = True
                winz.append(sndpkt)
                strng = data.read(1096)  ### Was at 1024
                if not strng:
                    msg_list.insert(tkinter.END, 'File was successfully sent!')
                # time.sleep(0.001) important for sending large files like pdfs
        data.close()
        my_fms.set('')
    except FileNotFoundError:
        msg_list.insert(tkinter.END, 'An error occurred. Please try again.')
        topp2 = tkinter.Toplevel(window)
        topp2.geometry('%dx%d%+d%+d' % (500, 100, 850, 125))
        topp2.title('Error Message')
        msg = tkinter.Message(topp2, text='The file path you entered is not correct. Please try again.', width=500)
        msg.pack()
        button = tkinter.Button(topp2, text='Dismiss', command=topp2.destroy)
        button.pack()


def emoji(emoj):
    msgs = my_msg.get()
    my_msg.set(msgs + emoj + '`~')


def on_closing(event=None):
    my_msg.set("{quit}")
    send()


window = tkinter.Tk()
window.title("Client Side Chat Room")
window.tk.call('encoding', 'system', 'utf-8')
messages_frame = tkinter.Frame(window)
emoji_frame = tkinter.Frame(window)
emoji2_frame = tkinter.Frame(window)
my_msg = tkinter.StringVar()
my_ms = tkinter.StringVar()
my_ftop2 = tkinter.StringVar()
var = tkinter.IntVar()
my_fms = tkinter.StringVar()
varz = tkinter.IntVar()
varzy = tkinter.IntVar()
my_msg.set("Type your messages here.")
scrollbar = tkinter.Scrollbar(messages_frame)
msg_list = tkinter.Listbox(messages_frame, height=30, width=75, yscrollcommand=scrollbar.set)
msg_list.configure(fg='red', font=72)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack(side=tkinter.TOP)
emoji_frame.pack(side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=True)
emoji2_frame.pack(side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=True)

entry_field = tkinter.Entry(window, textvariable=my_msg, width=30)
msg_list.insert(tkinter.END, 'NOTE: The chat logs will be saved in the project folder under projectChatLogsClient.txt')
msg_list.insert(tkinter.END, 'Welcome to the chat room! What is your name?')
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(window, text="Send", command=send)
picture_button = tkinter.Button(window, text='Send Small Picture', command=photos)
file_button = tkinter.Button(window, text='Send File/Large Picture', command=files)
emoji_button = tkinter.Button(window, text='\ud83d\ude02', command=lambda: emoji('\ud83d\ude02'))
emoji1_button = tkinter.Button(window, text='\ud83d\udc96', command=lambda: emoji('\ud83d\udc96'))
emoji2_button = tkinter.Button(window, text='\ud83d\ude12', command=lambda: emoji('\ud83d\ude12'))
emoji3_button = tkinter.Button(window, text='\ud83d\ude0d', command=lambda: emoji('\ud83d\ude0d'))
emoji4_button = tkinter.Button(window, text='\ud83d\udc4c', command=lambda: emoji('\ud83d\udc4c'))
emoji5_button = tkinter.Button(window, text='\ud83d\ude18', command=lambda: emoji('\ud83d\ude18'))
emoji6_button = tkinter.Button(window, text='\ud83d\ude14', command=lambda: emoji('\ud83d\ude14'))
emoji7_button = tkinter.Button(window, text='\ud83d\ude29', command=lambda: emoji('\ud83d\ude29'))
emoji8_button = tkinter.Button(window, text='\ud83d\ude2d', command=lambda: emoji('\ud83d\ude2d'))
emoji9_button = tkinter.Button(window, text='\ud83d\ude01', command=lambda: emoji('\ud83d\ude01'))
emoji10_button = tkinter.Button(window, text='\ud83d\ude0f', command=lambda: emoji('\ud83d\ude0f'))
emoji11_button = tkinter.Button(window, text='\ud83d\udc95', command=lambda: emoji('\ud83d\udc95'))
emoji12_button = tkinter.Button(window, text='\ud83d\udc4d', command=lambda: emoji('\ud83d\udc4d'))
emoji13_button = tkinter.Button(window, text='\ud83d\ude4c', command=lambda: emoji('\ud83d\ude4c'))
emoji14_button = tkinter.Button(window, text='\ud83d\ude09', command=lambda: emoji('\ud83d\ude09'))
emoji15_button = tkinter.Button(window, text='\ud83d\udc81', command=lambda: emoji('\ud83d\udc81'))
emoji16_button = tkinter.Button(window, text='\ud83d\ude48', command=lambda: emoji('\ud83d\ude48'))
emoji17_button = tkinter.Button(window, text='\ud83d\ude49', command=lambda: emoji('\ud83d\ude49'))
emoji18_button = tkinter.Button(window, text='\ud83d\ude0e', command=lambda: emoji('\ud83d\ude0e'))
emoji19_button = tkinter.Button(window, text='\u270c', command=lambda: emoji('\u270c'))
emoji20_button = tkinter.Button(window, text='\u270b', command=lambda: emoji('\u270b'))
emoji21_button = tkinter.Button(window, text='\ud83d\ude4f', command=lambda: emoji('\ud83d\ude4f'))
emoji22_button = tkinter.Button(window, text='\ud83d\ude1c', command=lambda: emoji('\ud83d\ude1c'))
emoji23_button = tkinter.Button(window, text='\ud83d\udc40', command=lambda: emoji('\ud83d\udc40'))
emoji24_button = tkinter.Button(window, text='\ud83d\ude0a', command=lambda: emoji('\ud83d\ude0a'))
emoji25_button = tkinter.Button(window, text='\ud83d\ude34', command=lambda: emoji('\ud83d\ude34'))
emoji26_button = tkinter.Button(window, text='\ud83d\udc4f', command=lambda: emoji('\ud83d\udc4f'))
emoji27_button = tkinter.Button(window, text='\ud83d\ude4a', command=lambda: emoji('\ud83d\ude4a'))
emoji28_button = tkinter.Button(window, text='\ud83d\udcaf', command=lambda: emoji('\ud83d\udcaf'))
emoji29_button = tkinter.Button(window, text='\ud83d\ude22', command=lambda: emoji('\ud83d\ude22'))
emoji30_button = tkinter.Button(window, text='\ud83d\ude21', command=lambda: emoji('\ud83d\ude21'))
emoji31_button = tkinter.Button(window, text='\ud83d\ude2b', command=lambda: emoji('\ud83d\ude2b'))
emoji32_button = tkinter.Button(window, text='\ud83d\ude31', command=lambda: emoji('\ud83d\ude31'))
emoji33_button = tkinter.Button(window, text='\ud83d\udc94', command=lambda: emoji('\ud83d\udc94'))
emoji34_button = tkinter.Button(window, text='\ud83d\udc8b', command=lambda: emoji('\ud83d\udc8b'))
emoji35_button = tkinter.Button(window, text='\ud83d\ude2a', command=lambda: emoji('\ud83d\ude2a'))
emoji36_button = tkinter.Button(window, text='\ud83d\udc4a', command=lambda: emoji('\ud83d\udc4a'))
emoji37_button = tkinter.Button(window, text='\ud83d\ude24', command=lambda: emoji('\ud83d\ude24'))
emoji38_button = tkinter.Button(window, text='\ud83d\udc7f', command=lambda: emoji('\ud83d\udc7f'))
emoji39_button = tkinter.Button(window, text='\u2714', command=lambda: emoji('\u2714'))
emoji40_button = tkinter.Button(window, text='\ud83d\udc4b', command=lambda: emoji('\ud83d\udc4b'))
emoji41_button = tkinter.Button(window, text='\ud83d\ude37', command=lambda: emoji('\ud83d\ude37'))
emoji42_button = tkinter.Button(window, text='\ud83c\udf39', command=lambda: emoji('\ud83c\udf39'))
emoji43_button = tkinter.Button(window, text='\u2728', command=lambda: emoji('\u2728'))
emoji44_button = tkinter.Button(window, text='\ud83d\ude45', command=lambda: emoji('\ud83d\ude45'))
emoji45_button = tkinter.Button(window, text='\ud83c\udf89', command=lambda: emoji('\ud83c\udf89'))
emoji46_button = tkinter.Button(window, text='\ud83d\udd2b', command=lambda: emoji('\ud83d\udd2b'))
emoji47_button = tkinter.Button(window, text='\ud83d\udcaa', command=lambda: emoji('\ud83d\udcaa'))
emoji48_button = tkinter.Button(window, text='\ud83d\ude06', command=lambda: emoji('\ud83d\ude06'))
emoji49_button = tkinter.Button(window, text='\ud83d\ude4b', command=lambda: emoji('\ud83d\ude4b'))
emoji50_button = tkinter.Button(window, text='\ud83d\udc4e', command=lambda: emoji('\ud83d\udc4e'))
emoji51_button = tkinter.Button(window, text='\ud83d\ude36', command=lambda: emoji('\ud83d\ude36'))
emoji52_button = tkinter.Button(window, text='\u270a', command=lambda: emoji('\u270a'))
emoji53_button = tkinter.Button(window, text='\ud83d\ude3b', command=lambda: emoji('\ud83d\ude3b'))
emoji54_button = tkinter.Button(window, text='\ud83d\udc80', command=lambda: emoji('\ud83d\udc80'))
emoji55_button = tkinter.Button(window, text='\ud83d\udd25', command=lambda: emoji('\ud83d\udd25'))
emoji56_button = tkinter.Button(window, text='\xa9', command=lambda: emoji('\xa9'))
emoji57_button = tkinter.Button(window, text='\ud83d\udc51', command=lambda: emoji('\ud83d\udc51'))
emoji58_button = tkinter.Button(window, text='\ud83d\udc98', command=lambda: emoji('\ud83d\udc98'))
emoji59_button = tkinter.Button(window, text='\ud83d\udc83', command=lambda: emoji('\ud83d\udc83'))

send_button.pack(in_=emoji2_frame, side=tkinter.TOP)
picture_button.pack(in_=emoji2_frame, side=tkinter.TOP)
file_button.pack(in_=emoji2_frame, side=tkinter.TOP)
emoji_button.pack(in_=emoji_frame, side=tkinter.LEFT)
emoji1_button.pack(in_=emoji_frame, side=tkinter.LEFT)
emoji2_button.pack(in_=emoji_frame, side=tkinter.LEFT)
emoji3_button.pack(in_=emoji_frame, side=tkinter.LEFT)
emoji4_button.pack(in_=emoji_frame, side=tkinter.LEFT)
emoji5_button.pack(in_=emoji_frame, side=tkinter.LEFT)
emoji6_button.pack(in_=emoji_frame, side=tkinter.LEFT)
emoji7_button.pack(in_=emoji_frame, side=tkinter.LEFT)
emoji8_button.pack(in_=emoji_frame, side=tkinter.LEFT)
emoji9_button.pack(in_=emoji_frame, side=tkinter.LEFT)
emoji10_button.pack(in_=emoji_frame, side=tkinter.LEFT)
emoji11_button.pack(in_=emoji_frame, side=tkinter.LEFT)
emoji12_button.pack(in_=emoji_frame, side=tkinter.LEFT)
emoji13_button.pack(in_=emoji_frame, side=tkinter.LEFT)
emoji14_button.pack(in_=emoji_frame, side=tkinter.LEFT)
emoji15_button.pack(in_=emoji_frame, side=tkinter.LEFT)
emoji16_button.pack(in_=emoji_frame, side=tkinter.LEFT)
emoji17_button.pack(in_=emoji_frame, side=tkinter.LEFT)
emoji18_button.pack(in_=emoji_frame, side=tkinter.LEFT)
emoji19_button.pack(in_=emoji_frame, side=tkinter.LEFT)
emoji20_button.pack(in_=emoji_frame, side=tkinter.LEFT)
emoji21_button.pack(in_=emoji_frame, side=tkinter.LEFT)
emoji22_button.pack(in_=emoji_frame, side=tkinter.LEFT)
emoji23_button.pack(in_=emoji_frame, side=tkinter.LEFT)
emoji24_button.pack(in_=emoji_frame, side=tkinter.LEFT)
emoji25_button.pack(in_=emoji_frame, side=tkinter.LEFT)
emoji26_button.pack(in_=emoji_frame, side=tkinter.LEFT)
emoji27_button.pack(in_=emoji_frame, side=tkinter.LEFT)
emoji28_button.pack(in_=emoji_frame, side=tkinter.LEFT)
emoji29_button.pack(in_=emoji_frame, side=tkinter.LEFT)
emoji30_button.pack(in_=emoji2_frame, side=tkinter.LEFT)
emoji31_button.pack(in_=emoji2_frame, side=tkinter.LEFT)
emoji32_button.pack(in_=emoji2_frame, side=tkinter.LEFT)
emoji33_button.pack(in_=emoji2_frame, side=tkinter.LEFT)
emoji34_button.pack(in_=emoji2_frame, side=tkinter.LEFT)
emoji35_button.pack(in_=emoji2_frame, side=tkinter.LEFT)
emoji36_button.pack(in_=emoji2_frame, side=tkinter.LEFT)
emoji37_button.pack(in_=emoji2_frame, side=tkinter.LEFT)
emoji38_button.pack(in_=emoji2_frame, side=tkinter.LEFT)
emoji39_button.pack(in_=emoji2_frame, side=tkinter.LEFT)
emoji40_button.pack(in_=emoji2_frame, side=tkinter.LEFT)
emoji41_button.pack(in_=emoji2_frame, side=tkinter.LEFT)
emoji42_button.pack(in_=emoji2_frame, side=tkinter.LEFT)
emoji44_button.pack(in_=emoji2_frame, side=tkinter.LEFT)
emoji45_button.pack(in_=emoji2_frame, side=tkinter.LEFT)
emoji46_button.pack(in_=emoji2_frame, side=tkinter.LEFT)
emoji47_button.pack(in_=emoji2_frame, side=tkinter.LEFT)
emoji48_button.pack(in_=emoji2_frame, side=tkinter.LEFT)
emoji49_button.pack(in_=emoji2_frame, side=tkinter.LEFT)
emoji50_button.pack(in_=emoji2_frame, side=tkinter.LEFT)
emoji51_button.pack(in_=emoji2_frame, side=tkinter.LEFT)
emoji52_button.pack(in_=emoji2_frame, side=tkinter.LEFT)
emoji53_button.pack(in_=emoji2_frame, side=tkinter.LEFT)
emoji54_button.pack(in_=emoji2_frame, side=tkinter.LEFT)
emoji55_button.pack(in_=emoji2_frame, side=tkinter.LEFT)
emoji56_button.pack(in_=emoji2_frame, side=tkinter.LEFT)
emoji57_button.pack(in_=emoji2_frame, side=tkinter.LEFT)
emoji58_button.pack(in_=emoji2_frame, side=tkinter.LEFT)
emoji59_button.pack(in_=emoji2_frame, side=tkinter.LEFT)
emoji43_button.pack(in_=emoji2_frame, side=tkinter.LEFT)
window.protocol("WM_DELETE_WINDOW", on_closing)

receive_thread = threading.Thread(target=receive)
receive_thread.start()
window.mainloop()
