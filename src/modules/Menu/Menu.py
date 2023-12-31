from src.modules.Menu.Option import Option
import sys

class Menu:
    def __init__(self, self_call: bool = False, 
                 linejump_before:int = 0,
                 option_pointer:str = "->",
                 menu_title:str = None,
                 ask_option_str:str = None) -> None:
        #self.__self_option = Option("menu",self.launch)
        self.__options = []
        self.__self_call = self_call
        self.__linejump_before = linejump_before
        self.__option_pointer = option_pointer
        self.__menu_title = menu_title
        self.__ask_option_str = ask_option_str
    
    def add_option(self, identifier, funct) -> None:
        self.__options.append(Option(identifier, funct)) 

    def launch(self):
        print(self)
        self.ask_option()
        if self.__self_call:
            self.launch()

    def ask_option(self) -> bool:
        __opt_str = self.__ask_option_str + self.__option_pointer + " " if self.__ask_option_str != None else self.__option_pointer + " "

        __opt:str = input(__opt_str)
        if __opt.isdigit():
            __opt = int(__opt)
            if __opt in range(1, len(self.__options) + 1):
                __c_opt:Option = self.__options[__opt - 1]
                __c_opt.call()

    def __str__(self) -> str:
        __str = "" + "\n" * self.__linejump_before
        if self.__menu_title != None:
            __str += self.__menu_title
        for __enum in enumerate(self.__options, 1):
            __str += str(__enum[0]) + self.__option_pointer + str(__enum[1]) + "\n"
        
        return __str

def close():
    sys.exit(0)

if __name__ == "__main__":   
    menuPrincipal = Menu()
    subMenu = Menu()

    menuPrincipal.add_option("Sub menu", subMenu.launch)
    menuPrincipal.add_option("salir", close)
    subMenu.add_option("Volver al menu", menuPrincipal.launch)

    while True:
        menuPrincipal.launch()
