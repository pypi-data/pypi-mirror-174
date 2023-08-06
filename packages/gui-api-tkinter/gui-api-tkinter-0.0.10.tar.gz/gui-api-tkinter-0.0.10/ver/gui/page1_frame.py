import tkinter as tk

from ver.gui import mvc
from ver.gui.frame_base import FrameBase


# --------------------
## holds the Page1 Frame
class Page1Frame(FrameBase):

    # --------------------
    ## constructor
    def __init__(self):
        ## holds the name of this page
        self._page = 'page1'
        ## holds the string variable used for the label1 widget
        self._label1_text = None
        ## hodls the string variable used for the label2 widget
        self._label2_text = None

    # --------------------
    ## Creates and returns a frame containing status information about the operation of the program.
    #
    # @param root  reference to the parent this frame resides on
    # @return reference to the Frame object
    def init(self, root) -> tk.Widget:
        page1_frame = tk.Frame(master=root,
                               borderwidth=self.FRAME_BORDERWIDTH,
                               relief=tk.RIDGE)
        mvc.guiapi.set_name(page1_frame, 'page1_frame')

        title_label = tk.Label(master=page1_frame,
                               text='Page : ',
                               font='Helvetica 14 bold')
        mvc.guiapi.set_name(title_label, 'title')
        title_label.grid(column=0, columnspan=1, row=0, rowspan=1, sticky=tk.W)

        str_var = tk.StringVar()
        str_var.set(self._page)
        label = tk.Label(master=page1_frame, textvariable=str_var)
        mvc.guiapi.set_name(label, 'page')
        label.grid(column=1, columnspan=1, row=0, rowspan=1, sticky=tk.NSEW)

        button_frame = tk.Frame(master=page1_frame)
        mvc.guiapi.set_name(button_frame, 'button_frame')
        button_padding_x = 3
        button_padding_y = 2
        button_frame.grid(column=0, columnspan=2,
                          row=1, rowspan=1, sticky=tk.NSEW,
                          )

        # TODO how to go to page2?

        # ---
        row = 0
        col = 0
        button = tk.Button(button_frame,
                           text='press me!',
                           command=self._on_button1_pressed,
                           )
        mvc.guiapi.set_name(button, 'button1')
        button.grid(column=col, columnspan=1,
                    row=row, rowspan=1, sticky=tk.NSEW,
                    padx=button_padding_x, pady=button_padding_y)

        col += 1
        self._label1_text = tk.StringVar()
        label = tk.Label(master=button_frame,
                         font='Helvetica 12',
                         textvariable=self._label1_text,
                         relief=tk.SUNKEN
                         )
        mvc.guiapi.set_name(label, 'label1')
        label.grid(column=col, columnspan=1,
                   row=row, rowspan=1, sticky=tk.EW)

        # ---
        row += 1
        col = 0
        button = tk.Button(button_frame,
                           text='press me!',
                           command=self._on_button2_pressed)
        mvc.guiapi.set_name(button, 'button2')

        button.grid(column=col, columnspan=1,
                    row=row, rowspan=1, sticky=tk.NSEW,
                    padx=button_padding_x, pady=button_padding_y)

        col += 1
        self._label2_text = tk.StringVar()
        label = tk.Label(master=button_frame,
                         font='Helvetica 12',
                         textvariable=self._label2_text,
                         relief=tk.SUNKEN
                         )
        mvc.guiapi.set_name(label, 'label2')
        label.grid(column=col, columnspan=1,
                   row=row, rowspan=1, sticky=tk.EW)

        self._set_labels()

        return page1_frame

    # --------------------
    ## reset the content of this frame
    #
    # @return None
    def clear(self):
        mvc.model.clear()
        self._set_labels()

    # --------------------
    ## callback used when button1 is pressed
    #
    # @return None
    def _on_button1_pressed(self):
        # toggle state
        mvc.model.toggle_state1()
        self._set_labels()

    # --------------------
    ## callback used when button2 is pressed
    #
    # @return None
    def _on_button2_pressed(self):
        mvc.model.toggle_state2()
        self._set_labels()

    # --------------------
    ## set the lable1 and lable2 based on the current model states
    #
    # @return None
    def _set_labels(self):
        self._label1_text.set(f'state: {mvc.model.state1}')
        self._label2_text.set(f'state: {mvc.model.state2}')
