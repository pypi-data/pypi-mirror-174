import winreg

import downscale_image


def register_downscale_commands(path_to_program, args):
    """Register 'Downscale image' as right click option for each of _file_types to call program."""
    for file_type in [
        rf"Software\Classes\SystemFileAssociations\{ext}\shell"
        for ext in downscale_image.SUPPORTED_FILE_EXTENSIONS
    ]:
        _set_run_key(file_type + r"\DownscaleImage", "Downscale image")
        _set_run_key(
            file_type + r"\DownscaleImage\command", rf'"{path_to_program}"' + " " + " ".join(args)
        )


def _set_run_key(key, value, *_, section=winreg.HKEY_CURRENT_USER):
    """Set/Remove Run Key in windows registry."""
    # This is for the system run variable
    print("key is", key, "<->", value)
    winreg.SetValue(section, key, winreg.REG_SZ, value)

    return
