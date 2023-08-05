def fis_tools_clean_df_columns(df):
    """
    Pasamos un DataFrame y nos lo devuelve con las columnas con un correcto formato para trabajo
    """
    for col in df.columns:
        new_col = col.lower()
        new_col = new_col.replace(" ", "_")
        new_col = new_col.replace("ó", "o").replace("ò","o")
        new_col = new_col.replace("í", "i").replace("á", "a").replace("é", "e")
        new_col = new_col.replace("ü", "u").replace("à","a").replace("è","e")
        new_col = new_col.replace("(", "")
        new_col = new_col.replace(")", "")
        new_col = new_col.replace("-", "")
        new_col = new_col.replace('º', "").replace("__", "_")
        new_col = new_col.replace("ñ", "n").replace("ú", "u").replace("í", "i")
        df.rename({col: new_col}, axis=1, inplace=True)
    return df
	
def fis_tools_quitar_tildes(palabra):
    """
    Limpieza de tildes para análisis
    """
    #Definimos la versión con tildes y símbolos y la sin
    con = 'áéíóúüñÁÉÍÓÚÜÑ'
    sin = 'aeiouunAEIOUUN'
    #Creamos un traductor
    traductor = str.maketrans(con,sin)
    #Aplicamos el traductor y devolvemos la palabra limpia
    return(palabra.translate(traductor))