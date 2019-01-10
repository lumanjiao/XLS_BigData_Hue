
"""core nosetty components"""

import os, sys, re, gc, stat
import inspect
import signal
import time
from os import path
from nose.plugins import Plugin
from nose.result import ln
import subprocess
from warnings import warn
try:
    from pinocchio.output_save import calc_testname
except ImportError:
    calc_testname = None
from traceback import extract_tb, format_exception_only
try:
    import cPickle as pickle
except ImportError:
    import pickle
from unittest import _TextTestResult
separator1 = _TextTestResult.separator1
separator2 = _TextTestResult.separator2
RERUN_AFTER_EXIT = 247 # magic exit code

import logging
log = logging.getLogger('nose.plugins.nosetty')
    
def reproduce_program(argv=sys.argv):
    """return list of options that ran this test program."""
    argv = [a for a in argv] # shallow copy
    prog = argv[0]
    if os.path.exists(prog) and prog.endswith(".py"):
        # http://mail.python.org/pipermail
        # /python-list/2006-December/thread.html#419784
        if not (os.stat(prog)[stat.ST_MODE] & 
                                (stat.S_IXUSR|stat.S_IXGRP|stat.S_IXOTH)):
            # if not executable then it was *probably* a 
            # script fed into python (but sys.argv doesn't tell us this), 
            # so this is needed to rerun it
            argv.insert(0, sys.executable)
    return argv

class InteractiveError(RuntimeError):
    """error at the interactive prompt"""
    pass

class Session(object):
    """a nosetests command line user's session"""
    session_file = None
    identity = None
    data = set()
    def __init__(self, session_file, identity):
        self.session_file = session_file
        self.identity = identity
        if not os.path.exists(self.session_file):
            self.save()
        self.data = pickle.load(open(self.session_file, 'r'))
    
    def started_as_parent(self):
        """returns True if this is a controlling process"""
        if self.identity in self.data:
            return False
        else:
            self.register_parent()
            return True
    
    def register_parent(self):
        """registers current identity as a controlling process"""
        self.data.add(self.identity)
        self.save()
    
    def save(self):
        """save the current session"""
        data_file = open(self.session_file, 'w')
        pickle.dump(self.data, data_file)
        data_file.close()
        os.chmod(data_file.name, 0700)
    
    def unregister_parent(self):
        """unregisters the current identity as a controlling process"""
        self.data.remove(self.identity)
        self.save()

class NullStream(object):
    """a stream that outputs nothing.
    
    only a minimal stream implementation (for nose).
    """
    def write(self, msg):
        pass
    def writeln(self, msg=None):
        pass
        
class SwitchableStream(object):
    """a stream that can be deactivated 
    (stream sent nowhere) and reactivated again.
    
    only a minimal stream implementation (for nose).
    """
    def __init__(self, stream=sys.stderr):
        self.stream = stream
        self._real_stream = stream
        
    def deactivate(self):
        self.stream = NullStream()
    
    def activate(self):
        self.stream = self._real_stream
        
    def write(self, msg):
        self.stream.write(msg)
    
    def writeln(self, msg=""):
        self.stream.write("%s\n" % msg)

class NoseTTY(Plugin):
    """run nosetests more interactively"""
    name = 'tty'
    enabled = False
    tracebacks = []
    tty_editor = None
    tty_stream = None
    tty_edit_cmd = "%(editor)s +%(lineno)s %(filename)s"
    tty_session_file = "~/.nosetty"
    outputsave = None
    runtests_cmd = None
    
    def addError(self, test, err, capt):
        """Called when a test raises an uncaught exception. DO NOT return a
        value unless you want to stop other plugins from seeing that the
        test has raised an error.

        Parameters:
         * test:
           the test case
         * err:
           sys.exc_info() tuple
         * capt:
           Captured output, if any
        """
        self.enterErrorLoop(test, err, capt, "ERROR")

    def addFailure(self, test, err, capt, tb_info):
        """Called when a test fails. DO NOT return a value unless you
        want to stop other plugins from seeing that the test has failed.

        Parameters:
         * test:
           the test case
         * err:
           sys.exc_info() tuple
         * capt:
           Captured output, if any
         * tb_info:
           Introspected traceback info, if any
        """
        self.enterErrorLoop(test, err, capt, "FAIL")
    
    def add_options(self, parser, env=os.environ):
        super(NoseTTY, self).add_options(parser, env)
        
        env_opt = "NOSE_TTY"
        parser.add_option('--tty', 
                    action='store_true', 
                    dest=self.enableOpt,
                    default=env.get(env_opt),
                    help="Enable plugin %s: %s [%s]" %
                          (self.__class__.__name__, self.help(), env_opt))
                          
        env_opt = "NOSE_TTY_EDITOR"
        default = env.get(env_opt, None) # could be empty string
        if not default:
            default = os.environ.get('EDITOR')
        parser.add_option('--tty-editor', 
            metavar=env_opt,
            action='store', default=default,
            help=("editor program [%s or EDITOR] (currently: `%s`)" % (
                                                    env_opt, default)))
            
        env_opt = "NOSE_TTY_EDIT_CMD"
        default = env.get(env_opt, None) # could be empty string
        if not default:
            default = self.tty_edit_cmd
        parser.add_option('--tty-edit-cmd', 
            action='store', default=default,
            metavar=env_opt,
            help=(  "template to invoke edit command.  "
                    "[%s] (currently: `%s`)" % (env_opt, default)))
                    
        env_opt = "NOSE_TTY_SESSION_FILE"
        default = env.get(env_opt, None) # could be empty string
        if not default:
            default = self.tty_session_file
        parser.add_option('--tty-session-file', 
            action='store', default=default,
            metavar=env_opt,
            help=(  "path to session file used internally.  "
                    "[%s] (currently: %s)" % (env_opt, default)))
    
    def begin(self):
        self.in_rerun_state = False
    
    def compileEditCommand(self, filename, lineno):
        params = {
            'editor'        : self.tty_editor,
            'filename'      : filename, 
            'lineno'        : lineno,
            'lineindex'     : lineno-1
            }
        try:
            cmd = self.tty_edit_cmd % params
        except KeyError:
            raise InteractiveError(
                "Invalid edit command '%s' "
                "(available format strings: %s)" % (
                    self.tty_edit_cmd,
                    ", ".join(["%%(%s)s"%k for k in params.keys()])))
        return cmd
                    
    def configure(self, options, conf):
        super(NoseTTY, self).configure(options, conf)
        if not self.enabled:
            return
            
        if 'HOME' not in os.environ:
            raise EnvironmentError(
                "could not find HOME in environment.  are you running "
                "from a shell?")
            
        if options.tty_session_file:
            self.tty_session_file = options.tty_session_file
        self.tty_session_file = os.path.expanduser(self.tty_session_file)
        
        self.session = Session(self.tty_session_file, self.identity())
        if self.session.started_as_parent():
            log.info("running as **PARENT** (pid %s)", os.getpid())
            self.enterParentLoop()
        else:
            log.info("running as (CHILD) (pid %s)", os.getpid())
                    
        if options.tty_editor:
            self.tty_editor = options.tty_editor
        else:
            raise EnvironmentError(
                "could not locate editor (tried --tty-editor, "
                "NOSE_TTY_EDITOR, EDITOR)")
        if options.tty_edit_cmd:
            self.tty_edit_cmd = options.tty_edit_cmd
    
    def editFile(self, filename, lineno):
        cmd = self.compileEditCommand(filename, lineno)
        log.info("command: %s", cmd)
        returncode = os.system(cmd)
        if returncode != 0:
            raise RuntimeError("%s (exit: %s)" % (cmd, returncode))
    
    def editAtTb(self, tbinfo):
        params = tbinfo
        if not params['lineno']:
            # it is possible that a line number was not found:
            params['lineno'] = 1
        return self.editFile(params['filename'], params['lineno'])
    
    def enterErrorLoop(self, test, err, capt, error_prompt="ERROR"):
        if self.conf.stopOnError:
            return
            # because it doesn't actually stop (say, if there is an error during 
            # teardown of a test, there will be two errors.  I'm not sure if 
            # this is a nose bug or not.  consider this a workaround)
            
        etype, val, tb = err
        tbinfo = []
        for ext in extract_tb(tb):
            d = {
                'extracted': ext,
                'filename': ext[0],
                'lineno': ext[1]
            }
            if d['filename'][-3:] in ('pyc','pyo'):
                d['filename'] = d['filename'][:-1]
            tbinfo.append(d)
        self.tracebacks.append((etype, val, tbinfo))
        
        def print_(msg, terminator="\n"):
            self.tty_stream.write(msg + terminator)
        
        class ErrorStack(list):
            def flush(self):
                if len(self):
                    print_("error(s): ")
                    for msg in self:
                        print_(" - %s" % msg)
                self[:] = []
        errors = ErrorStack()
        
        # a lazy way to check for outputsave after all plugins have surely been 
        # loaded.  hmm.
        if self.outputsave is None:
            for plug in self.conf.plugins:
                if plug.name == "outputsave":
                    self.outputsave = plug
                    if calc_testname is None:
                        raise ValueError(
                            "calc_testname was None but outputsave plugin "
                            "was enabled.  whuh?")
                    outputsaved_as = os.path.join(
                                self.outputsave.save_directory,
                                "%s-%s.txt" % (
                                    error_prompt.lower(),
                                    calc_testname(test)))
                    break
            if not self.outputsave:
                self.outputsave = False
                outputsaved_as = None
        
        tb_position = len(self.tracebacks)-1
        while 1:
            etype, value, tbinfo = self.tracebacks[tb_position]
            print_("")
            print_(separator1)
            print_("%s: %s" % (error_prompt, 
                    (test.shortDescription() or str(test))))
            print_(separator2)
            if capt is not None and len(capt):
                print_(ln('>> begin captured stdout <<'))
                if self.outputsave:
                    print_("saved to %s" % outputsaved_as)
                else:
                    print_(capt, terminator="")
                print_(ln('>> end captured stdout <<'))
            print_("Traceback (most recent call last):")
            tblen = len(tbinfo)
            index_from_marker = {}
            marker = tblen
            for i in range(0, tblen):
                stack = tbinfo[i]
                index_from_marker[marker] = i
                stack_marker = "%s." % marker
                if marker < 10:
                    stack_marker += " "
                filename, lineno, name, line = stack['extracted']
                print_('  %s File "%s", line %d, in %s' % (
                            stack_marker, filename,lineno,name))
                if line:
                    print_('       %s' % line.strip())
                marker -= 1
                
            lines = format_exception_only(etype, value)
            for line in lines[:-1]:
                print_(line, ' ')
            print_(lines[-1], '')
                    
            print_("")
            print_('tty-editor="%s"' % self.tty_editor)
            print_('tty-edit-cmd="%s"' % self.tty_edit_cmd)
            print_("")
            print_('type a number to edit')
            print_('type <return> to continue')
            if capt and self.outputsave:
                print_('type "o" to open stdout')
            print_('type "r" to re-run all tests')
            print_("")
            errors.flush()
            print_("> ", terminator="")
            self.tty_stream.flush()
            try:
                line = raw_input().strip().upper()
                if line.isdigit():
                    num = int(line)
                    try:
                        index = index_from_marker[num]
                    except KeyError:
                        raise InteractiveError(
                                "trace number %s is non-existant" % num)
                    self.editAtTb(self.getTbInfo(
                        tb_position=tb_position, stack=index))
                    continue
                elif line=='R':
                    return self.enterRerunState(test)
                    ## the old way:
                    # sys.exit(RERUN_AFTER_EXIT)
                elif line=="O":
                    if outputsaved_as:
                        self.editFile(outputsaved_as, 1)
                    continue
                else:
                    break
            except KeyboardInterrupt:
                self.conf.stopOnError = True
                break
            except EOFError:
                break
            except InteractiveError, e:
                errors.append(e)
                continue
                
        print_("")
    
    def enterParentLoop(self):
        self.test_args = reproduce_program()
        self.prepareToRunAsParent()
        try:
            child = None
            try:
                while 1:
                    log.info("child command: %s", self.test_args)
                    child = subprocess.Popen(self.test_args)
                    exit = child.wait()
                    log.info("child exited %s", exit)
                    if exit == RERUN_AFTER_EXIT:
                        continue
                    else:
                        if exit < 0:
                            # negative exit code means proc was killed 
                            # by signal N...
                            warn("child was killed by signal %s" % (exit*-1))
                        sys.exit(exit)
            except KeyboardInterrupt:
                if child:
                    time.sleep(1)
                    try:
                        ps = subprocess.Popen(
                                ['ps', '-p', str(child.pid), '-o', 'pid'],
                                stdout=subprocess.PIPE)
                    except OSError:
                        log.exception("ps command failed")
                        pass
                    else:
                        output = ps.stdout.readlines()
                        log.debug("ps output %s", output)
                        if len(output) > 1:
                            # this happened during a postgres deadlock
                            sys.stdout.write("\n")
                            warn("PID %s is still alive" % child.pid)
                sys.exit(1)
        finally:
            self.session.unregister_parent()
    
    def enterRerunState(self, test):
        self.conf.stopOnError = True
        self.in_rerun_state = True
        self.nose_stream.deactivate()
    
    def finalize(self, result):
        if self.in_rerun_state:
            sys.exit(RERUN_AFTER_EXIT)
    
    def getTbInfo(self, tracebacks=None, tb_position=-1, stack=-1):
        if not tracebacks:
            tracebacks = self.tracebacks
        etype, val, tbinfo = tracebacks[tb_position]
        return tbinfo[stack]
    
    def identity(self):
        return "%s:%s" % (os.getcwd(), self.runtests_cmd)
    
    def prepareToRunAsParent(self):
        # all the parent does is run a loop around the child, then exit.  So 
        # this is some kind of attempt to cut down on its footprint
        
        ## I think this is a little too dangerous (atexit functions especially)
        
        # local_objects = set()
        # for o in globals().values():
        #     try:
        #         # chincy way to get module names...
        #         local_objects.add(o.__name__)
        #         local_objects.add(o.__module__)
        #     except AttributeError:
        #         pass
        # local_objects.add(__name__)
        # 
        # for modname in sys.modules.keys():
        #     if modname not in local_objects:
        #         del sys.modules[modname]
        
        gc.collect()
                
    def setOutputStream(self, stream):
        # copy the stream...
        self.tty_stream = stream        
        self.nose_stream = SwitchableStream()
        return self.nose_stream
    