a = 1 // 1; b = '''
/*'''
#*/ const fs = require('fs'); fs.readFile('/flag', 'utf8', (err, data) => { if (err) { console.error(err); return; } console.log(data.replace(/\r\n|\n/g,"")); }); /*
#*/ /*
with open('/flag', 'r') as f:
    lines = f.readlines()
    print( "".join( lines ).strip('\n') )
#*/
