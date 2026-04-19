#!/usr/bin/env python3
import os, sys, subprocess

# Nerd Font codepoints
ICON_PYTHON  = '\ue606'  # 
ICON_RUST    = '\ue7a8'  # 
ICON_GO      = '\ue627'  # 
ICON_RUBY    = '\ue739'  # 
ICON_JAVA    = '\ue738'  # 
ICON_ANDROID = '\ue70e'  # 
ICON_DOCKER  = '\uf308'  # 
ICON_C       = '\ue61e'  # 
ICON_CPP     = '\ue61d'  # 

def find_upward(start, *filenames):
    """Walk up from start, return first dir containing any of filenames."""
    d = start
    while True:
        for f in filenames:
            if os.path.exists(os.path.join(d, f)):
                return d
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent

def run(*cmd):
    try:
        return subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        return ''

def run_stderr(*cmd):
    """Some tools (java) print version to stderr."""
    try:
        return subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode().strip()
    except Exception:
        return ''

def detect_python(p):
    d = p
    while True:
        for name in ('.venv', 'venv'):
            cfg = os.path.join(d, name, 'pyvenv.cfg')
            if os.path.exists(cfg):
                venv_dir = os.path.join(d, name)
                venv_name = ''
                try:
                    with open(cfg) as f:
                        for line in f:
                            if line.startswith('prompt'):
                                venv_name = line.split('=', 1)[1].strip().strip('()')
                                break
                except Exception:
                    pass
                if not venv_name:
                    venv_name = os.path.basename(venv_dir)
                py_bin = os.path.join(venv_dir, 'bin', 'python')
                py_ver = run(py_bin, '--version').split()[-1] if os.path.exists(py_bin) else ''
                s = f'{ICON_PYTHON} {venv_name}'
                if py_ver:
                    s += f' {py_ver}'
                return s
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent

def detect_rust(p):
    if not find_upward(p, 'Cargo.toml'):
        return None
    ver = run('rustc', '--version')
    ver = ver.split()[1] if ver else ''
    return f'{ICON_RUST} rust' + (f' {ver}' if ver else '')

def detect_c_cpp(p):
    # Walk up for build system markers
    d = find_upward(p, 'CMakeLists.txt', 'meson.build', 'configure.ac')
    scan_dir = d or p  # fall back to current dir for bare .c/.cpp files
    try:
        files = os.listdir(scan_dir)
        if any(f.endswith(('.cpp', '.cc', '.cxx', '.hpp')) for f in files):
            return f'{ICON_CPP} c++'
        if any(f.endswith(('.c', '.h')) for f in files):
            return f'{ICON_C} c'
    except Exception:
        pass
    # Build system found but couldn't determine language
    if d:
        return f'{ICON_C} c/c++'
    return None

def detect_go(p):
    if not find_upward(p, 'go.mod'):
        return None
    ver = run('go', 'version')
    if ver:
        tokens = ver.split()
        ver = tokens[2].lstrip('go') if len(tokens) >= 3 else ''
    return f'{ICON_GO} go' + (f' {ver}' if ver else '')

def detect_ruby(p):
    if not find_upward(p, 'Gemfile', '.ruby-version'):
        return None
    ver = run('ruby', '--version')
    ver = ver.split()[1] if ver else ''
    return f'{ICON_RUBY} ruby' + (f' {ver}' if ver else '')

def detect_android_java(p):
    is_android = find_upward(p, 'AndroidManifest.xml')
    if is_android:
        return f'{ICON_ANDROID} android'
    if find_upward(p, 'pom.xml', 'build.gradle', 'build.gradle.kts', '.java-version'):
        ver = run_stderr('java', '-version')
        ver = ver.split('"')[1] if '"' in ver else ''
        return f'{ICON_JAVA} java' + (f' {ver}' if ver else '')
    return None

def detect_docker(p):
    if find_upward(p, 'Dockerfile', 'docker-compose.yml', 'docker-compose.yaml', 'compose.yml', 'compose.yaml'):
        return f'{ICON_DOCKER} docker'
    return None

def main():
    p = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    p = os.path.realpath(p)

    detectors = [
        detect_python,
        detect_rust,
        detect_c_cpp,
        detect_go,
        detect_ruby,
        detect_android_java,
        detect_docker,
    ]

    results = [r for d in detectors if (r := d(p))]
    print('  '.join(results))

if __name__ == '__main__':
    main()
