#!/usr/bin/env python
import argparse
import curses
import requests
from curses import panel

def begin_curses():
    curses.noecho()
    curses.cbreak()
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, i, -1)

class API:

    def __init__(self):
        self.BASE = 'https://api.github.com/'

    def search(self, query, **kwargs):
        url = f'{self.BASE}search/{kwargs["opt"]}?q={query}'
        for k,v in kwargs:
            if k in ['page', 'sort', 'order', 'per_page']:
                url += f'&{k}={v}'

class Interface:

    def __init__(self, stdscr):
        self.api = API()
        self.stdscr = stdscr
        self.char_stack = ''
        L,C = self.stdscr.getmaxyx()
        self.left_win = curses.newwin(L, C, 0, 0)

    def show_help(self):
        L,C = self.stdscr.getmaxyx()
        self.help_win = self.left_win.subwin(15, 40, L//2-10, C//2-20)
        self.help_win.addstr(2, 2, 's: search')
        self.help_win.border()
        self.help_win.refresh()
        self.help_win.getch()
        self.search_opt = ''

    def search(self):
        L,C = self.stdscr.getmaxyx()
        self.search_opt_win = self.left_win.subwin(10, C//3, L//2-10, C//2-20)
        opts = {
                'C': 'commits',
                'c': 'code',
                'i': 'issues',
                'r': 'repositories',
                'u': 'users',
                }
        for i, (k,opt) in enumerate(opts.items()):
            self.search_opt_win.addstr(2+i, 2, f'{k}: {opt}' )
        self.search_opt_win.border()
        self.search_opt_win.refresh()
        opt = chr(self.search_opt_win.getch())
        self.search_opt_win.clear()
        self.left_win.addstr(2, 2, opts[opt] + ': ')
        self.left_win.move(2, 4 + len(opts[opt]))

    def do_getch(self):
        L,C = self.stdscr.getmaxyx()
        gotch = self.left_win.getch()
        char = chr(gotch)
        if char == '\x7f':
            self.char_stack = self.char_stack[:-1]
        elif char == 'a':
            pass
        elif char == 's':
            self.search()
            curses.curs_set(1)
        elif char == '?':
            self.show_help()
        elif len(char) > 1 or gotch == curses.KEY_RESIZE:
            pass
        else:
            self.char_stack += char

    def main_loop(self):
        curses.curs_set(0)
        L,C = self.stdscr.getmaxyx()
        while True:
            # left_win.resize(0,C-1)
            L,C = self.stdscr.getmaxyx()
            self.left_win.border()
            self.left_win.refresh()
            # if hasattr(self, 'search_opt'):
            #     self.left_win.addstr(2,2, 'kekao')
            # self.left_win.move(2,2)
            # self.left_win.addstr(L-2, 1, self.char_stack)
            self.do_getch()
            # self.left_win.clear()

def interactive(stdscr, args):
    begin_curses()
    i = Interface(stdscr)
    i.main_loop()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ncurses interface for GitHub')
    curses.wrapper(interactive, parser.parse_args())

