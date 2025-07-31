import subprocess
import json
import re

def run_powershell(cmd):
    """Run a PowerShell command and return parsed JSON."""
    completed = subprocess.run(
        ["powershell", "-NoProfile", "-Command", cmd],
        capture_output=True, text=True
    )
    if completed.returncode != 0:
        raise RuntimeError(f"PowerShell error: {completed.stderr.strip()}")
    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError:
        # Sometimes PS output is multiple JSON objects or non-json output, try fallback
        return None

def simplify_name(name):
    """Remove version numbers and 32/64Bit suffixes for cleaner display names."""
    if not name:
        return name
    name = re.sub(r'\s*\d+(\.\d+)+', '', name)  # remove versions like 1.2.3
    name = re.sub(r'\s*(64|32)Bit', '', name, flags=re.IGNORECASE)
    return name.strip()

def get_installed_programs():
    # PowerShell command to get installed programs with filtering:
    ps_cmd = r"""
    $exclusionPatterns = 'driver|filter|component|update'
    $publisherExclusions = 'amd|microsoft|intel|realtek|nvidia|qualcomm'

    $programs = Get-ItemProperty HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*,
                                  HKLM:\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\* |
        Where-Object {
            $_.DisplayName -and
            $_.DisplayName -notmatch $exclusionPatterns -and
            $_.Publisher -notmatch $publisherExclusions
        } |
        Select-Object DisplayName, DisplayVersion, Publisher, InstallLocation |
        ConvertTo-Json -Depth 4

    Write-Output $programs
    """
    result = run_powershell(ps_cmd)
    for p in result:
        print(f"Found program: {p.get('DisplayName', 'Unknown')}")
    if not result:
        return []

    # result is a list or dict (if one program), normalize to list
    if isinstance(result, dict):
        result = [result]

    # Post-process results in Python
    programs = []
    for p in result:
        name = p.get("DisplayName")
        publisher = p.get("Publisher", "")
        if not name:
            continue

        # Clean/simplify the name
        clean_name = simplify_name(name)

        # Filter again in Python just in case
        exclude_keywords = ['driver', 'filter', 'component', 'update']
        if any(k.lower() in clean_name.lower() for k in exclude_keywords):
            continue
        exclude_publishers = ['amd', 'microsoft', 'intel', 'realtek', 'nvidia', 'qualcomm']
        if publisher is not None and any(pub.lower() in publisher.lower() for pub in exclude_publishers):
            continue

        program = {
            "name": clean_name,
            "install_location": p.get("InstallLocation", ""),
        }
        programs.append(program)

    return programs

def save_programs_to_file(programs, filename="installed_programs.json"):
    data = {
        "programs": programs
    }
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def main():
    classic_programs = get_installed_programs()

    # Merge both lists, avoid duplicates by name (case-insensitive)
    seen = set()
    merged = []

    def add_unique(prog_list):
        for p in prog_list:
            name_lower = p["name"].lower()
            if name_lower not in seen:
                seen.add(name_lower)
                merged.append(p)

    add_unique(classic_programs)

    save_programs_to_file(merged)
    print(f"Saved {len(merged)} programs to installed_programs.json")


if __name__ == "__main__":
    main()
