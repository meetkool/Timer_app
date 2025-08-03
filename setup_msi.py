import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but some modules need help.
build_options = {
    'packages': [
        'timer_app',
        'pygame',
        'PIL',
        'mutagen',
        'tkinter'
    ],
    'excludes': ['matplotlib', 'numpy', 'pandas', 'scipy'],
    'include_files': [
        ('icon.ico', 'icon.ico'),
        ('sessions', 'sessions'),
        ('storage', 'storage'),
    ]
}

# MSI specific options
bdist_msi_options = {
    'upgrade_code': '{121e6ae8-7d8c-4dc3-ab66-b7a560adc6e9}',
    'add_to_path': False,
    'initial_target_dir': '[ProgramFilesFolder]\Timer Application',
    'install_icon': 'icon.ico'
}

base = 'Win32GUI' if sys.platform == 'win32' else None

executables = [
    Executable(
        'main.py',
        base=base,
        target_name='Timer_Application.exe',
        icon='icon.ico',
        shortcut_name='Timer Application',
        shortcut_dir='DesktopFolder'
    )
]

setup(
    name='Timer Application',
    version='1.0.0',
    description='Professional Timer Application for Problem Solving',
    author='Timer App Developer',
    options={
        'build_exe': build_options,
        'bdist_msi': bdist_msi_options
    },
    executables=executables
)
