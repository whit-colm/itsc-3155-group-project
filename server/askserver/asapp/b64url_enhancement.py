from base64 import urlsafe_b64decode, urlsafe_b64encode
import binascii

def check_base64(text: str) -> bool:
    """checks to make sure actual urlsafe base64 is in a field
    
    This does so by un-encoding and re-encoding it. Yeah it's bad and I'm sorry
    But oh well.


    Parameters
    ----------
    text : str
        The text to be verified

    Returns
    -------
    is : bool
        If the value was web base64 or not.
    """
    try:
        d = b64url_decode_str(text)
        e = b64url_encode_str(d)
        if e != text.strip('='):
            return False
        return True
    except (binascii.Error, UnicodeDecodeError):
        # This means that it couldn't decode.
        return False

# nicked shamelessly from gist to get urlsafe b64 to work as it actually should
# https://gist.github.com/cameronmaske/f520903ade824e4c30ab?permalink_comment_id=4512100#gistcomment-4512100
def b64url_encode_str(text: str) -> str:
    """Encode a string as URLsafe base64
    
    Parameters
    ----------
    text : str
        The text to be encoded.

    Returns
    -------
    s : str
        The encoded string.

    Raises
    ------
    TypeError
        If something that is not a string was passed
    binascii.Error, UnicodeDecodeError
        If passed a string, but not a base64 one.
    """
    if type(text) != str:
        raise TypeError(f"Expected `str`, got {type(text)}")
    b_encoded = text.encode('utf-8')
    b_decoded = urlsafe_b64encode(b_encoded).strip(b"=").decode('utf-8')
    return b_decoded

def b64url_decode_str(text: str) -> str:
    """Decode a URLsafe base64 string

    Parameters
    ----------
    text : str
        The text to be decoded.

    Returns
    -------
    s : str
        The decoded string.

    Raises
    ------
    TypeError
        If something that is not a string was passed
    binascii.Error, UnicodeDecodeError
        If passed a string, but not a base64 one.
    """
    if type(text) != str:
        raise TypeError(f"Expected `str`, got {type(text)}")
    
    b_encoded = text.strip("=").encode('utf-8')
    b_decoded = urlsafe_b64decode(
        (b_encoded+(b"="*(4-(len(b_encoded)%4))))
    ).decode('utf-8')
    return b_decoded