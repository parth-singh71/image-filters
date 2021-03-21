import easygui
import tkinter
from filter import Filter

window = tkinter.Tk()
window.geometry('600x600')
window.title('Image Filters')
window.configure(background='white')
label = tkinter.Label(window, text="Add filters to your Images", background='#FFFFFF', font=('calibri', 10, 'bold'))
label.pack(pady=10)


def upload_file():
    filepath = easygui.fileopenbox()
    f = Filter(view_mode=False, save_mode=True)
    f.execute(filepath=filepath)


upload = tkinter.Button(window, text="Choose an image", command=upload_file)
upload.pack(pady=10)

window.mainloop()
