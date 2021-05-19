import ctypes
import os
import unittest
import sys

import faulthandler
faulthandler.enable()

class WinLibdeepspeechTester(unittest.TestCase):
    @unittest.skipIf(sys.platform != 'win32', 'Win32 only test skipped.')
    def test_loading_win_dlls(self):
        """Gives the user a clue on any dlls that aren't installed yet."""
        # These dlls were found via DUMPBIN /import libdeepspeech.so
        # You'll need to install the VC build tools and enter the build
        # console in order to find all the files.
        dlls = [
            "USERENV.dll",
            "VERSION.dll",
            "ADVAPI32.dll",
            "WS2_32.dll",
            "CRYPT32.dll",
            "Normaliz.dll",
            "dbghelp.dll",
            "MSVCP140.dll",
            "SHLWAPI.dll",
            "KERNEL32.dll",
            "VCRUNTIME140.dll",
            "VCRUNTIME140_1.dll",
            "api-ms-win-crt-runtime-l1-1-0.dll",
            "api-ms-win-crt-heap-l1-1-0.dll",
            "api-ms-win-crt-utility-l1-1-0.dll",
            "api-ms-win-crt-math-l1-1-0.dll",
            "api-ms-win-crt-stdio-l1-1-0.dll",
            "api-ms-win-crt-filesystem-l1-1-0.dll",
            "api-ms-win-crt-convert-l1-1-0.dll",
            "api-ms-win-crt-string-l1-1-0.dll",
            "api-ms-win-crt-environment-l1-1-0.dll",
            "api-ms-win-crt-time-l1-1-0.dll",
        ]
        failures = []
        for dll in dlls:
            try:
                # Either works or throws an exception
                ctypes.windll.LoadLibrary(dll)
            except OSError as err:
                failures.append([dll, err])
        if failures:
            error_msg = ''
            for dll, err in failures:
                error_msg += f'{dll} failed with {err}\n'
            self.failed(error_msg)

    @unittest.skipIf(sys.platform != 'win32', 'Win32 only test skipped.')
    def test_loading_libdeepspeech_so(self):
        import site;
        sitepackgs = site.getsitepackages() + [site.getusersitepackages()]
        sitepackgs = [e for e in sitepackgs if e.endswith('site-packages')]
        libdeepspeech_paths = []
        for sp in sitepackgs:
            fullpath = os.path.join(sp, 'deepspeech', 'lib', 'libdeepspeech.so')
            if os.path.exists(fullpath):
                libdeepspeech_paths.append(fullpath)
        self.assertTrue(libdeepspeech_paths, 'Could not find libdeepspeech.so')
        libdeepspeech_so = os.path.abspath(libdeepspeech_paths[0])
        try:
            ctypes.CDLL(libdeepspeech_so)
        except OSError as err:
            # If there is a crash dump, it will be located at:
            # %LOCALAPPDATA%\CrashDumps
            dump_location = os.path.join(os.environ.get('LOCALAPPDATA', 'UNKNOWN'), 'CrashDumps')
            self.fail(f'Could not load {libdeepspeech_so}\nError: {err}\n\nPlease check the memory dump location at "{dump_location}"')
          
if __name__ == '__main__':
    unittest.main()
