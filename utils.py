
def list_concat(list_to_concat):
    list_con = ", ".join(["'" + el + "'" for el in list_to_concat])
    return list_con