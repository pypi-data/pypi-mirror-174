import pdb

import sys
from types import FrameType

import pathlib
import getopt
import os

KNOWN_UNITS = {"KB", "MB", "BYTES"}


class TomsPdb(pdb.Pdb):

    Path = pathlib.Path

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prompt = "[tomspdb] "

    @classmethod
    def frame_path(cls, frame) -> str:
        # WARNING. Pdb is weird. It delete all objects form the main namespace
        return cls.Path(frame.f_code.co_filename)

    @classmethod
    def in_my_code(cls, f: FrameType) -> bool:
        path = cls.frame_path(f)
        if any(p.name == "lib" for p in path.parents):
            return False
        return True

    def do_get_pdb(self, arg: str):
        "Get the pdb instance"
        del arg
        print("Set pself to pdb instance")
        self.curframe.f_globals["pself"] = self

    def do_top(self, arg: str):
        "Jump to the top of the stack. Equivalent to top -1"
        del arg
        self._select_frame(0)

    do_T = do_top

    def do_bottom(self, arg: str):
        "Jump to the top of the bottom of the stack. Equivalent to down -1"
        del arg
        self._select_frame(len(self.stack) - 1)

    do_B = do_bottom

    def do_get_frame(self, arg: str) -> FrameType:
        "Get the python frame object"
        del arg
        print("Putting current frame in frame variable")
        self.curframe.f_globals["frame"] = self.curframe

    def do_pretty_where(self, arg: str):
        "Print where we are in a pretty way"
        del arg

        for frame_lineno in self.stack:
            self.pretty_print_stack_entry(frame_lineno)

    do_W = do_pretty_where

    def pretty_print_stack_entry(self, frame_lineno):
        frame: FrameType
        frame, lineno = frame_lineno
        if frame is self.curframe:
            prefix = "> "
        else:
            prefix = "  "

        filename = self.Path(frame.f_code.co_filename).name
        func_name = frame.f_code.co_name

        whose = "MINE" if self.in_my_code(frame) else "LIB"
        self.message(f"{prefix} {whose:10} {func_name:20} {filename:20} {lineno:20}")

    def do_my_code(self, arg: str):
        "Jump out of library code into your code"
        del arg
        mycode_level = max(
            i for i, (x, _) in enumerate(self.stack) if self.in_my_code(x)
        )
        self._select_frame(mycode_level)

    do_my = do_my_code

    def do_show_exception(self, arg: str):
        "Show the current exception"
        code = compile(
            "import sys; __exception__ = sys.exc_info()[1]\n", "<stdin>", "single"
        )
        exec(
            code, self.curframe_locals, self.curframe.f_globals
        )  # pylint: disable=exec-used
        print(repr(self.curframe.f_globals["__exception__"]))

    do_e = do_show_exception

    def do_show_func(self, arg: str):
        "Get the current function"
        del arg
        import inspect

        arginfo = inspect.getargvalues(self.curframe)
        name = self.curframe.f_code.co_name
        self.message(f"{name}({','.join(arginfo.args)})")

    do_f = do_show_func

    def do_show_file(self, arg: str):
        "Get file we are current at"
        del arg
        self.message(self.curframe.f_code.co_filename)

    do_file = do_show_file


def main():
    # grumble at pdb for hard coding pdb type
    Restart = pdb.Restart
    import traceback
    import sys

    opts, args = getopt.getopt(sys.argv[1:], "mhc:", ["help", "command="])

    if not args:
        print(pdb._usage)
        sys.exit(2)

    commands = []
    run_as_module = False
    for opt, optarg in opts:
        if opt in ["-h", "--help"]:
            print(pdb._usage)
            sys.exit()
        elif opt in ["-c", "--command"]:
            commands.append(optarg)
        elif opt in ["-m"]:
            run_as_module = True

    mainpyfile = args[0]  # Get script filename
    print(mainpyfile)
    if not run_as_module and not os.path.exists(mainpyfile):
        print("Error:", mainpyfile, "does not exist")
        sys.exit(1)

    sys.argv[:] = args  # Hide "pdb.py" and pdb options from argument list

    print(args)

    if not run_as_module:
        mainpyfile = os.path.realpath(mainpyfile)
        # Replace pdb's dir with script's dir in front of module search path.
        sys.path[0] = os.path.dirname(mainpyfile)

    # Note on saving/restoring sys.argv: it's a good idea when sys.argv was
    # modified by the script being debugged. It's a bad idea when it was
    # changed by the user from the command line. There is a "restart" command
    # which allows explicit specification of command line arguments.
    p = TomsPdb()
    p.rcLines.extend(commands)
    while True:
        try:
            if run_as_module:
                p._runmodule(mainpyfile)
            else:
                p._runscript(mainpyfile)
            if p._user_requested_quit:
                break
            print("The program finished and will be restarted")
        except Restart:
            print("Restarting", mainpyfile, "with arguments:")
            print("\t" + " ".join(args))
        except SystemExit:
            # In most cases SystemExit does not warrant a post-mortem session.
            print("The program exited via sys.exit(). Exit status:", end=" ")
            print(sys.exc_info()[1])
        except SyntaxError:
            traceback.print_exc()
            sys.exit(1)
        except Exception:  # pylint: disable=broad-except
            traceback.print_exc()
            print("Uncaught exception. Entering post mortem debugging")
            print("Running 'cont' or 'step' will restart the program")
            t = sys.exc_info()[2]
            p.interaction(None, t)
            print(
                "Post mortem debugger finished. The "
                + mainpyfile
                + " will be restarted"
            )


def set_trace():
    import sys  # pylint: disable=import-outside-toplevel

    p = TomsPdb()
    p.set_trace(sys._getframe().f_back)  # pylint: disable=protected-access


if __name__ == "__main__":
    main()
