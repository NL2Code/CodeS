import configparser


def read_configuration(file_path):
    """
    reads configuration from given file path
    For two displays:
    return (p_brightness, p_red, p_green, p_blue, temperature
            s_brightness, s_red, s_green, s_blue)
    for one display:
    return (p_brightness, p_red, p_green, p_blue, temperature)
    """
    config = configparser.RawConfigParser()
    config.read(file_path)
    p_brightness = config.getint("primary", "brightness")
    p_red = config.getint("primary", "red")
    p_green = config.getint("primary", "green")
    p_blue = config.getint("primary", "blue")
    temperature = (
        config.get("primary", "temperature")
        if config.has_option("primary", "temperature")
        else "Default"
    )
    if config.getboolean("primary", "has_secondary"):
        p_source = config.get("primary", "source")
        s_brightness = config.getint("secondary", "brightness")
        s_red = config.getint("secondary", "red")
        s_green = config.getint("secondary", "green")
        s_blue = config.getint("secondary", "blue")
        s_source = config.get("secondary", "source")
        return (
            p_brightness,
            p_red,
            p_green,
            p_blue,
            p_source,
            temperature,
            s_brightness,
            s_red,
            s_green,
            s_blue,
            s_source,
        )
    else:
        return p_brightness, p_red, p_green, p_blue, temperature
