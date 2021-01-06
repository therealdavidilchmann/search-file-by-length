from cx_Freeze import setup, Executable

base = None    

executables = [Executable("suchen_z.py", base=base)]

packages = ["idna", "os"]
options = {
    'build_exe': {    
        'packages':packages,
    },
}

setup(
    name = "test",
    options = options,
    version = "0.1",
    description = 'Hello World!',
    executables = executables
)