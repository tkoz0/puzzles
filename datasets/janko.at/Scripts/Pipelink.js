function Pipelink(){var b=this;b.constructor();b.uis.puzzle=["Pipelink","Leitungsnetz"];var l=b.board.c,m=0,n=0;b.charToValue=b.charToValue.concat([",",nil,"x",nil,"-",nil,"/",nil,".",nil]);b.enable.dragging=!0;b.enable.values=!1;b.enable.currentValue=!1;b.keypad.left=nil;b.uic.clues="#333333";b.init=function(){Object.getPrototypeOf(b).init.call(b)};b.reset2=function(){try{m=b.size.x;n=b.size.y;if(b.level.problem){var c=0;var f=b.level.problem.replace(/\s+/g," ").trim().split(" ");for(var d=0;d<n;d++)for(var a=
0;a<m;a++){var g=l[a][d];var e=f[c++];if("."!=e&&"-"!=e)if("@"==e)g.areas=b.cell.outside,g.value=16,g.valid=!1;else if("#"==e)g.value=16;else if("x"==e||"+"==e)g.value=15;else if(isNaN(parseInt(e))){var h=0;e.contains("n")&&(h|=1);e.contains("s")&&(h|=4);e.contains("e")&&(h|=2);e.contains("w")&&(h|=8);0!=h&&(g.value=h)}else g.value=parseInt(e);g.value!=nil&&(g.fixed=!0)}}if(b.level.solution)for(c=0,f=b.level.solution.replace(/\s+/g," ").trim().split(" "),d=0;d<n;d++)for(a=0;a<m;a++)g=l[a][d],e=f[c++],
"-"==e||"."==e?g.solution=nil:(h=0,e.contains("n")&&(h|=1),e.contains("s")&&(h|=4),e.contains("e")&&(h|=2),e.contains("w")&&(h|=8),0!=h&&(g.solution=h))}catch(p){throw b.exception(p),p;}};b.check2=function(){try{for(var c=function(a,d,g){try{var e=l[a][d];if(e.value!=nil){e.checked=!0;e.count=g;var h=16;15==e.value&&(2==f?h=8:8==f?h=2:1==f?h=4:4==f&&(h=1));if(8==h||16==h&&0!=(e.value&8))if(0==a)e.error=1;else if(15!=e.value||2==f){f=2;var k=l[a-1][d];k.value==nil||0==(k.value&2)?e.error=1:k.checked&&
15!=k.value||c(a-1,d,g)}if(2==h||16==h&&0!=(e.value&2))if(a==m-1)e.error=1;else if(15!=e.value||8==f)f=8,k=l[a+1][d],k.value==nil||0==(k.value&8)?e.error=1:k.checked&&15!=k.value||c(a+1,d,g);if(1==h||16==h&&0!=(e.value&1))if(0==d)e.error=1;else if(15!=e.value||4==f)f=4,k=l[a][d-1],k.value==nil||0==(k.value&4)?e.error=1:k.checked&&15!=k.value||c(a,d-1,g);if(4==h||16==h&&0!=(e.value&4))if(d==n-1)e.error=1;else if(15!=e.value||1==f)f=1,k=l[a][d+1],k.value==nil||0==(k.value&1)?e.error=1:k.checked&&15!=
k.value||c(a,d+1,g)}}catch(q){throw b.exception(q),q;}},f=16,d=0,a=0;a<m;a++)for(var g=0;g<n;g++){var e=l[a][g];e.checked||e.value==nil||c(a,g,d++)}1!=d&&(b.solved=!1);for(a=0;a<m;a++)for(g=0;g<n;g++)e=l[a][g],15!=e.value&&5!=e.value&&10!=e.value&&3!=e.value&&6!=e.value&&9!=e.value&&12!=e.value&&(e.error=1),e.checked||(e.error=3),15!=e.value||0!=a&&a!=m-1&&0!=g&&g!=n-1&&0!=(l[a-1][g].value&2)&&0!=(l[a+1][g].value&8)&&0!=(l[a][g-1].value&4)&&0!=(l[a][g+1].value&1)||(e.error=1)}catch(h){throw b.exception(h),
h;}};b.solve2=function(){try{for(var c=0;c<m;c++)for(var f=0;f<n;f++){var d=l[c][f];if(d.fixed){if(0!=(d.value&1)){var a=l[d.x][d.y-1];a.value=a.value==nil?4:a.value|4}0!=(d.value&4)&&(a=l[d.x][d.y+1],a.value=a.value==nil?1:a.value|1);0!=(d.value&8)&&(a=l[d.x-1][d.y],a.value=a.value==nil?2:a.value|2);0!=(d.value&2)&&(a=l[d.x+1][d.y],a.value=a.value==nil?8:a.value|8)}}}catch(g){throw b.exception(g),g;}};b.makeMove2=function(c,f,d){try{f||(f=nil),Object.getPrototypeOf(this).makeMove2.call(this,c,f,
d)}catch(a){throw b.exception(a),a;}};b.dragTo2=function(c,f){try{var d=f.value==nil?0:f.value,a=c.value==nil?0:c.value;f.y==c.y?f.x>c.x?(d|=8,a|=2):(d|=2,a|=8):f.x==c.x&&(f.y>c.y?(d|=1,a|=4):(d|=4,a|=1));d&&!f.fixed&&b.makeMove(f,d);a&&!c.fixed&&b.makeMove(c,a);b.moveTo(c)}catch(g){throw b.exception(g),g;}};b.dragTo2Alt=function(c,f){try{f.value!=nil&&b.makeMove(f,nil,b.current.color),c.value!=nil&&b.makeMove(c,nil,b.current.color),b.moveTo(c)}catch(d){throw b.exception(d),d;}};b.valueToString=function(b,
f){switch(b){case 16:return f?"x":"-";case 15:return"nsew";case 0:return"o";case 4:return"s";case 1:return"n";case 2:return"e";case 8:return"w";case 3:return"ne";case 9:return"nw";case 6:return"se";case 12:return"sw";case 5:return"ns";case 10:return"ew";default:return"-"}};b.paintCell=function(c){try{var f=b.canvas.getContext("2d");f.fillStyle=b.uic.light[0];f.fillRect(c.px,c.py,b.unit.x,b.unit.y);if(c.value!=nil){var d=Math.floor((b.unit.x-Math.floor(b.unit.x/4))/2),a=b.unit.x-2*d,g=a+d;f.fillStyle=
b.display.errors?b.uic.dark[c.count%10]:b.display.errors&&1==c.error?b.uic.error:c.fixed?b.uic.clues:0==c.color?b.uic.line:b.uic.dark[c.color];16!=c.value||b.solved||b.paintCross(c);0==c.value&&f.fillRect(c.px+d,c.py+d,a,a);0!=(c.value&1)&&f.fillRect(c.px+d,c.py,a,g);0!=(c.value&4)&&f.fillRect(c.px+d,c.py+d,a,g);0!=(c.value&2)&&f.fillRect(c.px+d,c.py+d,g,a);0!=(c.value&8)&&f.fillRect(c.px,c.py+d,g,a)}b.paintSymbolMarkers(c);c.error&&b.display.errors&&(c.label!=nil?b.paintErrorCircle(c):c.value==nil&&
b.paintErrorDot(c))}catch(e){throw b.exception(e),e;}}}Pipelink.prototype=new Puzzle;