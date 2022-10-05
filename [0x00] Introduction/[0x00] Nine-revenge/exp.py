import base64

enc = "LwcvGwpuiPzT7+LY9PPo6eLpuiY7vTY6ejz2OH1pui5uDu6+LY5unpui+6uj14qmpuipqfo="
enc = enc.replace( "pui", "" )
enc = list( base64.b64decode( enc[1:] ) )

for i in range( len( enc ) ):
    enc[i] = chr( enc[i] ^ 135 )

print( "".join( enc ) )
