
import os
import shutil
import subprocess
from fixture import TempIO
from nosetty import NoseTTY
from nose.tools import eq_
try:
    # 0.10.0 :
    from nose.plugins import PluginTester, NoseStream
except ImportError:
    from nosetrim.test import PluginTester, NoseStream
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

class NoseTTYTester(PluginTester):
    activate_opt = "--with-tty"
    addargs = ['--tty-editor=echo', "--tty-session-file", '~/.nosetty-test']
    env = os.environ.copy()
    env['NOSE_TTY_EDITOR'] = ""
    env['NOSE_TTY_EDIT_CMD'] = ""
    env['EDITOR'] = ""
    env['NOSE_TTY_SESSION_FILE'] = ""
    
    def inputLines(self, *lines):
        for line in lines:
            self.nose.proc.stdin.write("%s\n" % line)
            self.nose.proc.stdin.flush()
        self.nose.proc.stdin.close()
        
    def setUp(self):
        super(NoseTTYTester, self).setUp()
    
    def _makeNose(self):
        """returns a NoseStream object."""
        # print self._args
        return NoseStream( subprocess.Popen(self._args, 
                                    stdout=subprocess.PIPE, 
                                    stderr=subprocess.STDOUT,
                                    stdin=subprocess.PIPE,
                                    cwd=self.suitepath, env=self.env, bufsize=1,
                                    universal_newlines=True))

class WithTestMethod(object):
    """mixin to run tests with a failing method"""
    def assert_failure_edited(self):
        self.inputLines("1")
        assert "+3" in self.nose
        assert "test_to_fail.py" in self.nose
        
    def makeSuite(self):
        self.tmp = TempIO()
        self.tmp.putfile("test_to_fail.py",
            """\
def test_bad():
    print "it's no good!!!"
    assert False""")
        return self.tmp

class WithUnitTest(object):
    """mixin to run tests with a failing unittest.TestCase"""
    def assert_failure_edited(self):
        self.inputLines("1")
        assert "+4" in self.nose
        assert "test_to_fail_unittest.py" in self.nose
        
    def makeSuite(self):
        self.tmp = TempIO()
        self.tmp.putfile("test_to_fail_unittest.py",
            """\
import unittest
class TestToFail(unittest.TestCase):
    def test_bad_from_unittest(self):
        assert False
            """)
        return self.tmp

class WithTestClass(object):
    """mixin to run tests with a failing test class"""
    def assert_failure_edited(self):
        self.inputLines("1")
        assert "+3" in self.nose
        assert "test_to_fail_testclass.py" in self.nose
        
    def makeSuite(self):
        self.tmp = TempIO()
        self.tmp.putfile("test_to_fail_testclass.py",
            """\
class TestToFail(object):
    def test_bad_from_testclass(self):
        assert False
            """)
        return self.tmp

class EditingErrorsByNumber(NoseTTYTester):
    def test_typing_a_number_edits_file_in_traceback(self):
        self.assert_failure_edited()

class TestEditingErrorsByNumberWithMethod(
        WithTestMethod, EditingErrorsByNumber):
    pass
class TestEditingErrorsByNumberWithUnittest(
        WithUnitTest, EditingErrorsByNumber):
    pass
class TestEditingErrorsByNumberWithTestClass(
        WithTestClass, EditingErrorsByNumber):
    pass

class EditErrorsByNumber(EditingErrorsByNumber):
    def makeSuite(self):
        self.tmp = TempIO()
        self.tmp.putfile("test_to_fail_nested.py",
            """\
def two():
    raise ValueError
def three():
    two()
def four():
    three()
def test_nested_fail():
    four()""")
        return self.tmp

class TestEditErrorAtNumber1(EditErrorsByNumber):        
    def assert_failure_edited(self):
        self.inputLines("1")
        assert "+2" in self.nose
        assert "test_to_fail_nested.py" in self.nose

class TestEditErrorAtNumber2(EditErrorsByNumber):        
    def assert_failure_edited(self):
        self.inputLines("2")
        assert "+4" in self.nose
        assert "test_to_fail_nested.py" in self.nose
        
class TestEditErrorAtNumber3(EditErrorsByNumber):        
    def assert_failure_edited(self):
        self.inputLines("3")
        assert "+6" in self.nose
        assert "test_to_fail_nested.py" in self.nose
        
class TestEditErrorAtNumber4(EditErrorsByNumber):        
    def assert_failure_edited(self):
        self.inputLines("4")
        assert "+8" in self.nose
        assert "test_to_fail_nested.py" in self.nose
        
class TestEditErrorAtNonexistantNumber(EditErrorsByNumber):        
    def assert_failure_edited(self):
        self.inputLines("99")
        assert "error(s):" in self.nose
        self.nose.reset_buffer()
        assert " - trace number" in self.nose
    

class TestEditorOption(WithTestMethod, NoseTTYTester):
    def test_option_can_set_editor(self):
        """--tty-editor option can set editor"""
        self.assert_failure_edited()
    
class TestEditorVar(WithTestMethod, NoseTTYTester):
    addargs = []
    env = NoseTTYTester.env
    env['NOSE_TTY_EDITOR'] = 'echo'
    
    def test_env_var_can_set_editor(self):
        """NOSE_TTY_EDITOR var can set editor"""
        self.assert_failure_edited()
    
class TestDefaultEditor(WithTestMethod, NoseTTYTester):
    addargs = []
    env = NoseTTYTester.env
    env['NOSE_TTY_EDITOR'] = ""
    env['EDITOR'] = 'echo'
    
    def test_env_var_can_set_editor(self):
        """EDITOR var can set editor"""
        self.assert_failure_edited()
    
class TestEditCommandVar(WithTestMethod, NoseTTYTester):
    addargs = ['--tty-editor=echo']
    debuglog = 'nose.plugins.nosetty'
    env = os.environ.copy()
    env['NOSE_TTY_EDIT_CMD'
                    ] = "%(editor)s %(filename)s --any-custom-opt=%(lineno)s"
    
    def assert_failure_edited(self):
        self.inputLines("1")
        assert "test_to_fail.py --any-custom-opt=3" in self.nose
    
    def test_env_var_can_set_edit_command(self):
        """NOSE_TTY_EDIT_CMD can set edit command"""
        self.assert_failure_edited()

class TestInvalidEditCommand(WithTestMethod, NoseTTYTester):    
    addargs = ['--tty-edit-cmd=%(editor)s %(noop)s'] # invalid template
    def test_invalid_edit_command_prints_error(self):
        self.inputLines("1")
        assert "error(s):" in self.nose
        self.nose.reset_buffer()
        assert " - Invalid edit command" in self.nose
        
    
class TestEditCommandOption(WithTestMethod, NoseTTYTester):
    addargs = [
        '--tty-edit-cmd="%(editor)s %(filename)s --any-custom-opt=%(lineno)s"',     
        '--tty-editor=echo']
    
    def assert_failure_edited(self):
        self.inputLines("1")
        assert "test_to_fail.py --any-custom-opt=3" in self.nose
    
    def test_tty_edit_cmd_can_set_edit_command(self):
        """--tty-edit-cmd can set edit command"""
        self.assert_failure_edited()

class TestSuccessfulRun(WithTestMethod, NoseTTYTester):
    def makeSuite(self):
        self.tmp = TempIO()
        self.tmp.putfile("test_to_pass.py",
            """def test_good(): pass""")
        return self.tmp
        
    def test_absence_of_error_does_nothing(self):
        assert "test_to_pass.py" not in self.nose

class TestRerunCommand(WithTestMethod, NoseTTYTester):
    addargs = NoseTTYTester.addargs + ['--verbose']
    # debuglog = "nose.plugins.nosetty"
    env = NoseTTYTester.env
    env['NOSE_TTY_EDITOR'] = 'echo'
    num_reruns = 4
    
    def accept_token(self, line):
        """returns true if something in the line should restart the counter
        
        i.e. you could count how many times 
        "type "r" to re-run all tests" appears
        """
        return "test_foo.test_will_fail ..." in line
        
    def makeSuite(self):
        self.tmp = TempIO()
        self.tmp.test = "test"
        self.tmp.test.putfile("__init__.py",
            """
import os
def teardown():
    f = open(os.path.join(os.path.dirname(__file__),'foo.out'), 'w')
    f.write("blah")
    f.close()
    pass
            """)
        self.tmp.test.putfile("test_foo.py",
            """
def test_will_fail():
    raise AssertionError
            """)
        return self.tmp
    
    def onrun(self, run_number):
        """called for each run number"""
        if run_number == 2:
            assert os.path.exists(self.tmp.test.join('foo.out')), (
                "expected package level teardown() to "
                "generate 'foo.out' in %s" % (
                    os.listdir(self.tmp.test)))
    
    def send_eof(self):
        self.nose.proc.stdin.close()
    
    def send_rerun_cmd(self):
        self.nose.proc.stdin.write("r\n")
        self.nose.proc.stdin.flush()
        
    def test_r_command_reruns_test_suite(self):
        ticker = 0
        run_number = 0
        ticker_limit = self.num_reruns*100
        self.send_rerun_cmd()
        for line in self.nose:
            ticker += 1
            last_run = run_number
            if self.accept_token(line):
                run_number += 1
                try:
                    self.send_rerun_cmd()
                except ValueError:
                    # IO op on closed stdin
                    pass
                if run_number == self.num_reruns:
                    self.send_eof()
            if run_number != last_run:
                try:
                    self.onrun(run_number)
                except:
                    self.send_eof()
                    raise
            if ticker > ticker_limit:
                raise RuntimeError("time out")
        returncode = self.nose.proc.wait()
        
        # expect the first run + number of re-runs...
        eq_(run_number, self.num_reruns+1)

class OutputsavePlugin(NoseTTYTester):
    addargs = [
        '--tty-edit-cmd', "%(editor)s 'OPENFILE:%(filename)s LINE:%(lineno)s'",
        '--tty-editor=echo', 
        '--with-outputsave', '--save-directory=output']
    
class TestOutputsavePlugin(WithTestMethod, OutputsavePlugin):
    def assert_failure_edited(self):
        self.inputLines("o")
        filename = os.path.join(self.tmp, "output", 
                                "fail-test_to_fail.test_bad.txt")
        assert "OPENFILE:%s LINE:1" % filename in self.nose
        assert 'type "o" to open stdout' in self.nose
    
    def test_typing_o_opens_saved_output(self):
        self.assert_failure_edited()

class TestOutputsavePluginWhenNoOutput(WithTestClass, OutputsavePlugin):
    def assert_failure_edited(self):
        self.inputLines("")
        assert 'type "o" to open stdout' not in self.nose
    
    def test_if_no_output_then_there_is_no_prompt(self):
        self.assert_failure_edited()
        