#!/usr/bin/env python3
#
# provides alt+tab functionality between windows, switching
# between n windows; example i3 conf to use:
#     exec_always --no-startup-id i3-cycle-focus.py --history 2
#     bindsym $mod1+Tab exec --no-startup-id i3-cycle-focus.py --switch
from collections import defaultdict
import os
import asyncio
from argparse import ArgumentParser
import logging

from i3ipc.aio import Connection

SOCKET_FILE = '/tmp/.i3-cycle-focus.sock'
MAX_WIN_HISTORY = 16
UPDATE_DELAY = .5


def on_shutdown(i3_conn, e):
    os._exit(0)


class WinQueue:
    def __init__(self, max_hist=MAX_WIN_HISTORY):
        self.max_hist = max_hist
        self.window_list = []
        self.window_index = None

    def update_focus(self, con):
        window_id = con.id
        if not self.window_list:
            self.window_list.append(window_id)
            self.window_index = 0
        # elif self.window_list[self.window_index] != window_id:
        else:
            self.remove_win(con)
            self.window_index += 1
            self.window_list.insert(self.window_index, window_id)

        if len(self.window_list) > self.max_hist:
            del self.window_list[self.max_hist:]

    def remove_win(self, con):
        window_id = con.id
        if window_id not in self.window_list:
            return

        prev_win_id = self.window_list[self.window_index]
        self.window_list.remove(window_id)
        self.window_index = self.window_list.index(prev_win_id)
    
    def get_prev(self):
        self.window_index = (self.window_index - 1) % len(self.window_list)
        return self.window_list[self.window_index]

    def get_next(self):
        self.window_index = (self.window_index - 1) % len(self.window_list)
        return self.window_list[self.window_index]

def get_focused_ws_name(ws_reply):
    focused = [ws for ws in ws_reply if ws.focused][0]
    return focused.name

class FocusWatcher:
    def __init__(self):
        self.i3 = None
        self.queue = WinQueue()
        self.update_task = None
        self.ws_queues = defaultdict(WinQueue)
        self.ws_name = None

    async def connect(self):
        self.i3 = await Connection().connect()
        tree = await self.i3.get_tree()
        asyncio.create_task(self.update_window_list(
            tree.find_focused()
        ))
        self.ws_name = tree.find_focused().workspace().name
        self.i3.on('window::focus', self.on_window_focus)
        self.i3.on('window::close', self.on_window_close)
        self.i3.on('shutdown', on_shutdown)

    async def update_window_list(self, con):
        if UPDATE_DELAY != 0.0:
            await asyncio.sleep(UPDATE_DELAY)

        logging.info('updating window list')
        logging.info('old window list: {}'.format(self.queue.window_list))
        logging.info('old index: {}'.format(self.queue.window_index))

        self.queue.update_focus(con)
        self.ws_queues[self.ws_name].update_focus(con)
        
        logging.info('new window list: {}'.format(self.queue.window_list))
        logging.info('new index: {}'.format(self.queue.window_index))

    async def on_window_focus(self, i3conn, event):
        logging.info('got window focus event')
        wss = await self.i3.get_workspaces()
        self.ws_name = get_focused_ws_name(wss)
        # self.ws_name = event.container.workspace().name

        # print("XXXXXX", self.ws_name.find_focused().workspace().name)
        # # print("XXXXXX", self.ws_name.id)
        # # print("XXXXXX", self.ws_name.parent.id)
        if (args.filter_workspace is not None 
            and self.ws_name != args.filter_workspace):
            logging.info('not handling window outside workspace specified')
            return
        if args.ignore_float and (event.container.floating == "user_on"
                                  or event.container.floating == "auto_on"):
            logging.info('not handling this floating window')
            return

        if self.update_task is not None:
            self.update_task.cancel()

        logging.info('scheduling task to update window list')
        self.update_task = asyncio.create_task(
            self.update_window_list(event.container)
        )

    async def on_window_close(self, i3conn, event):
        self.queue.remove_win(event.container)
        self.ws_queues[self.ws_name].remove_win(event.container)

    async def run(self):
        async def handle_switch(reader, writer):
            print("ind::::::  ", self.queue.window_index)
            print("list size::::::  ", len(self.queue.window_list))
            data = await reader.read(1024)
            logging.info('received data: {}'.format(data))
            if data == b'switch':  #switchprev
                window_id = self.queue.get_prev()
                await self.i3.command('[con_id={}] focus'.format(window_id))
            elif data == b'switchback': #switchnext
                window_id = self.queue.get_next()
                await self.i3.command('[con_id={}] focus'.format(window_id))
            elif data == b'wsswitch':  #switchprev
                window_id = self.ws_queues[self.ws_name].get_prev()
                await self.i3.command('[con_id={}] focus'.format(window_id))
            elif data == b'wsswitchback': #switchnext
                window_id = self.ws_queues[self.ws_name].get_next()
                await self.i3.command('[con_id={}] focus'.format(window_id))
        server = await asyncio.start_unix_server(handle_switch, SOCKET_FILE)
        await server.serve_forever()

async def send_switch():
    reader, writer = await asyncio.open_unix_connection(SOCKET_FILE)

    logging.info('sending switch message')
    writer.write('switch'.encode())
    await writer.drain()

    logging.info('closing the connection')
    writer.close()
    await writer.wait_closed()


async def send_switchback():
    reader, writer = await asyncio.open_unix_connection(SOCKET_FILE)

    logging.info('sending switch message')
    writer.write('switchback'.encode())
    await writer.drain()

    logging.info('closing the connection')
    writer.close()
    await writer.wait_closed()

async def send_wsswitch():
    reader, writer = await asyncio.open_unix_connection(SOCKET_FILE)

    logging.info('sending wsswitch message')
    writer.write('wsswitch'.encode())
    await writer.drain()

    logging.info('closing the connection')
    writer.close()
    await writer.wait_closed()


async def send_wsswitchback():
    reader, writer = await asyncio.open_unix_connection(SOCKET_FILE)

    logging.info('sending wsswitchback message')
    writer.write('wsswitchback'.encode())
    await writer.drain()

    logging.info('closing the connection')
    writer.close()
    await writer.wait_closed()


async def run_server():
    focus_watcher = FocusWatcher()
    await focus_watcher.connect()
    await focus_watcher.run()


if __name__ == '__main__':
    parser = ArgumentParser(prog='i3-cycle-focus.py',
                            description="""
        Cycle backwards through the history of focused windows (aka Alt-Tab).
        This script should be launched from ~/.xsession or ~/.xinitrc.
        Use the `--history` option to set the maximum number of windows to be
        stored in the focus history (Default 16 windows).
        Use the `--delay` option to set the delay between focusing the
        selected window and updating the focus history (Default 2.0 seconds).
        Use a value of 0.0 seconds to toggle focus only between the current
        and the previously focused window. Use the `--ignore-floating` option
        to exclude all floating windows when cycling and updating the focus
        history. Use the `--visible-workspaces` option to include windows on
        visible workspaces only when cycling the focus history. Use the
        `--active-workspace` option to include windows on the active workspace
        only when cycling the focus history.

        To trigger focus switching, execute the script from a keybinding with
        the `--switch` option.""")
    parser.add_argument('--history',
                        dest='history',
                        help='Maximum number of windows in the focus history',
                        type=int)
    parser.add_argument('--delay',
                        dest='delay',
                        help='Delay before updating focus history',
                        type=float)
    parser.add_argument('--ignore-floating',
                        dest='ignore_float',
                        action='store_true',
                        help='Ignore floating windows '
                        'when cycling and updating the focus history')
    parser.add_argument('--visible-workspaces',
                        dest='visible_workspaces',
                        action='store_true',
                        help='Include windows on visible '
                        'workspaces only when cycling the focus history')
    parser.add_argument('--active-workspace',
                        dest='active_workspace',
                        action='store_true',
                        help='Include windows on the '
                        'active workspace only when cycling the focus history')
    parser.add_argument('--filter-workspace',
                        dest='filter_workspace',
                        action='store',
                        help='Include windows on the '
                        'specified workspace only when cycling the focus history')
    parser.add_argument('--switch',
                        dest='switch',
                        action='store_true',
                        help='Switch to the previous window',
                        default=False)
    parser.add_argument('--switchback',
                        dest='switchback',
                        action='store_true',
                        help='Switch to the previous window',
                        default=False)
    parser.add_argument('--wsswitch',
                        dest='wsswitch',
                        action='store_true',
                        help='Switch to the previous window',
                        default=False)
    parser.add_argument('--wsswitchback',
                        dest='wsswitchback',
                        action='store_true',
                        help='Switch to the previous window',
                        default=False)
    parser.add_argument('--debug', dest='debug', action='store_true', help='Turn on debug logging')
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    if args.history:
        MAX_WIN_HISTORY = args.history
    if args.delay:
        UPDATE_DELAY = args.delay
    else:
        if args.delay == 0.0:
            UPDATE_DELAY = args.delay
    if args.switch:
        asyncio.run(send_switch())
    elif args.switchback:
        asyncio.run(send_switchback())
    elif args.wsswitch:
        asyncio.run(send_wsswitch())
    elif args.wsswitchback:
        asyncio.run(send_wsswitchback())
    else:
        asyncio.run(run_server())

