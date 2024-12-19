from .models import NFCTag
from .validators import parse_ascii_mirror

def scan_nfc_tag(ascii_mirror, user=None):
    """
    Ensure that an NFCTagContent exists for every NFCTag instance.
    """
    uid, counter = parse_ascii_mirror(ascii_mirror)

    try:
        return NFCTag.objects.get(uid=uid)
    except NFCTag.DoesNotExist:
        print(f"NFCTag with UID {uid} does not exist.")
        return None
