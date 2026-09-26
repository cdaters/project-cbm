"""Appliance display sizes: binary scaling with familiar KB/MB/GB labels."""

def human_size(value):
    if type(value) is not int or not 0 <= value < 2**64:
        return 'Unknown'
    if value < 1024:
        return f'{value} bytes'
    size = value
    for unit in ('KB', 'MB', 'GB', 'TB', 'PB', 'EB'):
        size /= 1024
        # Promote values which would round up to the next unit.
        if round(size, 1) < 1024 or unit == 'EB':
            return f'{size:.1f}'.rstrip('0').rstrip('.') + ' ' + unit
