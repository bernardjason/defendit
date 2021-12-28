import sys

from game import runtime


def main():
    runtime.tk.title("defendit")
    #runtime.tk.attributes("-fullscreen", True)
    #game.SCREEN_X = runtime.tk.winfo_screenwidth()
    runtime.mainloop()


if __name__ == "__main__":
    sys.exit(main())
