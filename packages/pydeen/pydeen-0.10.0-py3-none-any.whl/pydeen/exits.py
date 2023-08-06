"""PyDEEN exits to enhance Functionality
"""

class ExitBase:
    pass

class MenuExitCallback(ExitBase):
    def exit_menu_process_selection(self, exit, owner, selected:str, text:str=None) -> bool:
        self.trace(f"no menu processing by menuexit {self}")
        return False

    def exit_menu_get_entries_top(self, exit, owner) -> dict:
        self.trace(f"no menu at top level by menuexit {self}")
        return None

    def exit_menu_get_entries_bottom(self, exit, owner) -> dict:
        self.trace(f"no menu at bottom level by menuexit {self}")
        return None


class MenuExit(ExitBase):

    def __init__(self, callback:MenuExitCallback, entries_top:dict=None, entries_bottom:dict=None) -> None:
        super().__init__()
        self.callback = callback
        self.entries_top:dict=entries_top
        self.entries_bottom:dict=entries_bottom



