import os
import sys


if os.name != "nt":
    import logging
    from logging.handlers import SysLogHandler


""" PrintHook intercepts stdout/stderr output, appends a comma-separated prefix, sends the
    modified message with a prefix to syslog through either the syslog facilities LOG_LOCAL1
    or LOG_LOCAL2 and sends the unmodified message back to its original destination (stdout/stderr)
    To begin the intercept, start_hook() method must explicitly be called after initialization.
    The same instance may be reused to start and stop the hook multiple times.
    Based off example from : https://code.activestate.com/recipes/579132-print-hook/
    Usage:
        from print_hook import PrintHook
        ph = PrintHook(PrintHook.stdout_fd)
        print('Hello World)     # Hello World
        ph.start_hook('My Prefix')
        print('Hello World')    # My Prefix, Hello World
        ph.stop_hook()          # Hello World
"""


class PrintHook(object):
    # Class variables to represent which of stdout/stderr to enable hooks for
    stdout_fd = 1
    stderr_fd = 2
    socket_address = "/var/log/rsyslog-custom-socket"
    """ Initializes the stdout/err hook. Initializing it alone will not begin intercepting
        stdout/stderr. start_hook must be called to begin the intercept and redirection.

        Members:
            _facility:
                syslog.LOG_LOCAL1 and syslog.LOG_LOCAL2 correspond to the syslog facilities
                that can be used for identifying and filtering specific messages in syslog.
                LOG_LOCAL0 to LOG_LOCAL7 are facilities available for local use cases.
                Others, such as LOG_KERN, LOG_USER are reserved for specific use cases:
                i.e. LOG_KERN for kernel related logs. This class uses LOG_LOCAL1 for stdout
                and LOG_LOCAL2 for stderr redirection.
            _prefix:
                default prefix is set to no request id as it may not always be called within
                a request's lifecycle.
            _target_fd:
                stores information on whether stdout or stderr is intercepted. See class variables
                stdout_fd and stderr_fd
            _original_fd:
                keep a handle to the original stdout and stderr so the unparsed message can be
                passed to the original file descriptors.
    """

    def __init__(self, file_descriptor=1):
        self._original_fd = None
        self._target_fd = file_descriptor
        if os.name != "nt":
            self._facility = (
                SysLogHandler.LOG_LOCAL1 if file_descriptor == PrintHook.stdout_fd else SysLogHandler.LOG_LOCAL2
            )
            self._syslog_logger = logging.getLogger(str(self._facility))
            if os.path.exists(self.socket_address):
                handler = logging.handlers.SysLogHandler(self.socket_address, self._facility)
                print("logging socket was found. logging is available.")
            else:
                handler = logging.FileHandler("/dev/null")
                print("logging socket not found. logging not available.")
            # rsyslog skips the first whitespace delimited token.
            # To negate this, we prepend THIS_WILL_BE_SKIPPED to our message format.
            # THIS_WILL_BE_SKIPPED does not end up in App Insights or stdout logs.
            formatter = logging.Formatter("THIS_WILL_BE_SKIPPED %(message)s")
            handler.setFormatter(formatter)
            self._syslog_logger.addHandler(handler)
            self._syslog_logger.setLevel(logging.INFO)
            # This prevents the logger from propagating to higher loggers which may be writing on the root logger
            # This will remove the syslog from printing to console
            self._syslog_logger.propagate = False

        self._prefix = "00000000-0000-0000-0000-000000000000"
        self._started = False

    def start_hook(self, prefix="00000000-0000-0000-0000-000000000000"):
        if not self._started:
            self.set_prefix(prefix)
            if self._target_fd == PrintHook.stdout_fd:
                self._original_fd = sys.stdout
                sys.stdout = self
            else:
                self._original_fd = sys.stderr
                sys.stderr = self
            self._started = True

    def stop_hook(self):
        if self._started:
            self._original_fd.flush()
            if self._target_fd == PrintHook.stdout_fd:
                sys.stdout = self._original_fd
            else:
                sys.stderr = self._original_fd
            self._started = False

    def set_prefix(self, prefix):
        self._prefix = prefix

    def write(self, text):
        if len(text.rstrip()):
            console_text = text.rstrip()
            # The request id should be inserted in front of every request
            modified_text = self._prefix + "," + console_text + "\n"
            self._pipe_to_original_dest(modified_text)
            if os.name != "nt":
                self._pipe_to_syslog(modified_text)

    def _pipe_to_original_dest(self, console_text):
        self._original_fd.write(console_text)

    def _pipe_to_syslog(self, syslog_text):
        self._syslog_logger.info(syslog_text)

    # pass any unhandled methods to original fd
    def __getattr__(self, name):
        return self._original_fd.__getattribute__(name)

    # To be able to handle unbuffered mode i.e print('text', flush= True)
    def flush(self):
        self._original_fd.flush()
