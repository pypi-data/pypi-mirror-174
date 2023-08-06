def remove_doubles(array, sort=False):
    '''
    

    Parameters
    ----------
    array : ARRAY
        Array with double entries.
    sort : Boolean, optional
        If True, new array gets sorted from small to big. The default is False.

    Returns
    -------
    x : Array
        Array without doubles.

    '''
    x = list(dict.fromkeys(array))
    if sort: 
        x.sort()
    return x
        