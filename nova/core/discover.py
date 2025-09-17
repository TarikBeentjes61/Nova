import os
from pathlib import Path
import win32com.client

IGNORE_PATTERNS = [
    "uninstall", "setup", "update", "helper",
    "crashreport", "readme", "manual"
]

def should_ignore(name: str) -> bool:
    lname = name.lower()
    return any(p in lname for p in IGNORE_PATTERNS)


def resolve_lnk(path: Path) -> tuple[Path | None, Path | None]:
    """
    grab the exe and icon path from a shortcut (.lnk) file
    """
    try:
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortcut(str(path))

        target = shortcut.Targetpath
        icon_location, _ = shortcut.IconLocation.split(",")[0], None  # some icons have ",index"

        exe_path = None
        icon_path = None

        # Only accept valid .exe targets
        if target and target.lower().endswith(".exe") and Path(target).exists():
            exe_path = Path(target)

            # If icon location is set and exists, use it
            if icon_location and Path(icon_location).exists():
                icon_path = Path(icon_location)
            else:
                # fallback: use exe itself as icon source
                icon_path = exe_path

        return exe_path, icon_path

    except Exception:
        return None, None


def discover_programs(limit=200):
    """
    discover installed programs on Windows by scanning Start Menu shortcuts
    and filtering out unwanted patterns.
    """
    programs = []
    seen = set()

    # start menu paths to scan 
    start_menu_paths = [
        Path(os.environ.get("APPDATA", "")) / "Microsoft" / "Windows" / "Start Menu" / "Programs",
        Path(os.environ.get("ProgramData", "")) / "Microsoft" / "Windows" / "Start Menu" / "Programs"
    ]

    for root in start_menu_paths:
        if not root.exists():
            continue
        for lnk in root.rglob("*.lnk"):
            name = lnk.stem.strip()

            # skip duplicates, ignored patterns and non-exe targets
            if name.lower() in seen or should_ignore(name):
                continue

            exe, icon = resolve_lnk(lnk)
            if not exe:
                continue

            seen.add(name.lower())

            entry = {
                "name": name,
                "category": "Application",
                "command_type": "executable",
                "icon": str(icon) if icon else "", # path could be the same as exe (cause its stored in the exe file)
                "exe": str(exe)
            }
            programs.append(entry)

            if len(programs) >= limit:
                return programs

    return programs