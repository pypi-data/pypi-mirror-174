# Generating Caesar Cipher Function
def cipher(text, shift, encrypt=True):
    """
    Encrypt text using Caesar Cipher method. 
    It converts each letter by certain shifts.

    Parameters
    ----------
    text : Text or string type parameter.
        Text that you would like to encrypt. It should be alphabet only.
        Number and symbol cannot be encrypted.
    shift : Integer type parameter. It can be positive or negative value.
        A number letter shift you expect to change the original text.
    encrypt: A boolean type parameter. The default is True.
        If it is True, then the text will be encrypted. 
        If the value is False, the function will decrypt the text.
    
    Returns
    -------
    String type output. Encrpyted text by how many shifts that determined.

    Examples
    --------

    Encryption:
    >>> from cipher_yazid_ega import cipher_ey2335
    >>> cipher_ey2335.cipher(text='wallnut', shift=1, encrypt=True)
        Output : 'xbmmvu'

    Decryption:
    >>> from cipher_yazid_ega import cipher_ey2335
    >>> cipher_ey2335.cipher(text='xbmmvu', shift=1, encrypt=True)
        Output : 'wallnut'
    """

    alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    new_text = ''
    for c in text:
        index = alphabet.find(c)
        if index == -1:
            new_text += c
        else:
            new_index = index + shift if encrypt == True else index - shift
            new_index %= len(alphabet)
            new_text += alphabet[new_index:new_index+1]
    return new_text