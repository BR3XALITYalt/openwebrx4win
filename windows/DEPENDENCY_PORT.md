# Windows dependency port

OpenWebRX+ uses native C++ components for DSP and SDR hardware access. These components must build and run as Windows processes; changing the Python package paths alone does not provide a working receiver.

## CSDR and PyCSDR

OpenWebRX+ requires the compiled `pycsdr.modules` extension and checks that both its binding version and the linked CSDR version are at least 0.18.0.

The upstream build currently has these Windows blockers:

- CSDR's CMake configuration discovers FFTW3f and libsamplerate through pkg-config.
- The CMake configuration applies GNU-specific compiler flags and defines `_GNU_SOURCE`.
- CSDR's `ExecModule` uses `fork`, `execvp`, POSIX pipes, `fcntl`, `poll`, `waitpid`, and Unix signals.
- PyCSDR builds a compiled Python extension and links it against `csdr++` and FFTW3f. It is not a pure-Python dependency.
- The CSDR `nmux` utility uses POSIX file descriptors, `fcntl`, `select`, pthread synchronization, and Unix signal handling.

Relevant upstream sources:

- [CSDR build configuration](https://github.com/luarvique/csdr/blob/master/CMakeLists.txt)
- [CSDR ExecModule](https://github.com/luarvique/csdr/blob/master/src/lib/exec.cpp)
- [CSDR nmux](https://github.com/luarvique/csdr/blob/master/src/apps/nmux/nmux.cpp)
- [PyCSDR extension build](https://github.com/luarvique/pycsdr/blob/master/setup.py)

The Windows port needs Win32 process and pipe handling for ExecModule, a Windows implementation of nmux behavior, a Windows-capable build configuration, and compatible FFTW3f and libsamplerate development libraries. Do not omit ExecModule or nmux to get a partial build accepted as complete.

## OWRX Connector

OpenWebRX+ uses the OWRX Connector executables to provide SDR sample streams and runtime device control. Its CMake project requires CSDR and optionally builds the RTL-SDR and SoapySDR connectors when their development libraries are found.

The current source uses POSIX socket headers and functions, including `sys/socket.h`, `netinet/in.h`, `arpa/inet.h`, `unistd.h`, `close`, and `MSG_NOSIGNAL`. The connector command-line parsing also uses `getopt_long`, and the applications install Unix signal handlers.

A Windows implementation must use Winsock startup, socket types and shutdown calls, Windows-compatible command-line parsing, and Windows process shutdown handling. Keep the connector command names and command-line options expected by OpenWebRX+ unchanged.

Relevant upstream sources:

- [OWRX Connector build configuration](https://github.com/luarvique/owrx_connector/blob/master/CMakeLists.txt)
- [Connector executable targets](https://github.com/luarvique/owrx_connector/blob/master/src/app/CMakeLists.txt)
- [Connector IQ socket](https://github.com/luarvique/owrx_connector/blob/master/src/lib/iq_connection.cpp)
- [Connector control socket](https://github.com/luarvique/owrx_connector/blob/master/src/lib/control_connection.cpp)

## Port order

1. Make CSDR and PyCSDR build with the selected native Windows compiler and preserve their existing APIs.
2. Port CSDR process execution and nmux without removing their behavior.
3. Port the OWRX Connector base library and socket handling.
4. Build and validate the RTL-SDR connector, then the SoapySDR connector.
5. Verify receiver start, sample streaming, control updates, and shutdown through the unchanged OpenWebRX+ backend.

A component is not Windows-supported merely because CMake generates build files. It must compile, load, communicate with the rest of OpenWebRX+, and pass runtime tests on Windows.
