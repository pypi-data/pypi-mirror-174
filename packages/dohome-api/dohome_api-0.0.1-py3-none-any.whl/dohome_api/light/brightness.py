"""Brightness helper"""

def apply_brightness(value: int, brightness_uint8: int) -> int:
    """Applies brightness to the value"""
    # TODO: Add gamma correction
    brightness_percent = brightness_uint8 / 255
    return int(value * brightness_percent)
