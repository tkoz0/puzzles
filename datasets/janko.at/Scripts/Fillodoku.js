function Fillodoku(){var a=this;a.constructor();a.uis.puzzle=["Fillodoku"];var r=a.board.c,k=0,q=0,l=0,m=0;zmin=1;zmax=0;a.keys=a.keys.concat(["patternx","patterny"]);a.enable.vmarkers=!0;a.enable.dragging=!0;a.enable.pgrid=!1;a.enable.values=!1;a.enable.currentValue=!1;a.cell.nilalias=1;a.cvalues=[];a.charToValue=a.charToValue.concat(["x",1,"0",1,",",1,"/",nil,"-",nil]);a.init=function(){Object.getPrototypeOf(a).init.call(a)};a.reset2=function(){var b;try{k=a.labels.west;q=a.labels.north;l=a.size.x-
a.labels.east;m=a.size.y-a.labels.south;zmin=1;zmax=a.size.z;a.cvalues=[];6==a.size.x&&(a.cvalues=[0,1,2,3]);9==a.size.x?a.cvalues=[0,2,0,3,4]:12==a.size.x&&(a.cvalues=[0,2,2,3,0,5]);var h=0;a.cell.values=[];for(b=0;b<a.cvalues.length;b++)a.cvalues[b]&&(a.cell.values[h++]=b);a.cell.values[h++]=nil;h=2;a.valueToMarker=[1,a.marker.letterX];for(b=2;b<a.cvalues.length;b++)a.cvalues[b]&&(a.valueToMarker[h++]=b,a.valueToMarker[h++]=a.marker.numberBase+b);h=0;a.keypadValues=[];for(b=2;b<a.cvalues.length;b++)a.cvalues[b]&&
(a.keypadValues[h++]=[b.toString(),b]);a.keypadValues[h++]=["X",1];a.keypadValues[h++]=["\u2022",nil];h=a.charToValue.length;a.charToValue[h++]="X";a.charToValue[h++]=1;for(b=2;b<a.cvalues.length;b++)a.cvalues[b]&&(a.charToValue[h++]=b.toString(),a.charToValue[h++]=b);a.infoText=a.uis.get("numbers")+": ";h=!0;for(b=2;b<a.cvalues.length;b++)a.cvalues[b]&&(h||(a.infoText+=", "),a.infoText+=b,h=!1);var n=patterny=0;9==a.size.x?n=patterny=3:6==a.size.x?(n=3,patterny=2):12==a.size.x&&(n=4,patterny=3);
a.level.patternx&&(n=parseInt(a.level.patternx));a.level.patterny&&(patterny=parseInt(a.level.patterny));if(n&&patterny)for(var d=q;d<a.size.z;d++)for(var g=k;g<a.size.z;g++)r[g][d].areas=Math.floor(g/n)+Math.floor(d/patterny)*l;if(a.level.problem){b=0;var c=a.level.problem.replace(/\s+/g," ").trim().split(" ");for(d=q;d<m;d++)for(g=k;g<l;g++){var f=a.board.c[g][d];var e=c[b++];"."==e||"-"==e?f.value=nil:(f.value=parseInt(e),f.fixed=!0)}}if(a.level.solution)for(b=0,c=a.level.solution.replace(/\s+/g,
" ").trim().split(" "),d=q;d<m;d++)for(g=k;g<l;g++)f=a.board.c[g][d],e=c[b++],f.solution="."==e||"-"==e?nil:parseInt(e)}catch(p){throw a.exception(p),p;}};a.check2=function(){try{for(var b=function(c,d){try{c.count=d;for(var e=0;4>e;e++){var f=c.x+h[e],g=c.y+n[e];if(0<=f&&f<l&&0<=g&&g<m){var k=r[f][g];k.areas==c.areas&&k.value==c.value&&0==k.count&&b(k,d)}}}catch(z){throw a.exception(z),z;}},h=[1,0,-1,0],n=[0,1,0,-1],d=k;d<l;d++){var g=[];for(var c=0;c<a.cvalues.length;c++)g[c]=0;for(var f=q;f<m;f++){var e=
a.board.c[d][f];e.value!=nil&&g[e.value]++}for(c=2;c<a.cvalues.length;c++)if(g[c]!=a.cvalues[c])for(a.solved=!1,f=q;f<m;f++)e=a.board.c[d][f],e.value==c&&(e.error=2)}for(f=k;f<m;f++){g=[];for(c=0;c<a.cvalues.length;c++)g[c]=0;for(d=k;d<l;d++)e=a.board.c[d][f],e.value!=nil&&g[e.value]++;for(c=2;c<a.cvalues.length;c++)if(g[c]!=a.cvalues[c])for(a.solved=!1,d=k;d<l;d++)e=a.board.c[d][f],e.value==c&&(e.error=2)}var p=1;for(d=k;d<l;d++)for(f=q;f<m;f++)e=r[d][f],0==e.count&&1<e.value&&b(r[d][f],p++);for(d=
k;d<l;d++)for(f=q;f<m;f++)if(e=r[d][f],e.value!=nil&&1!=e.value&&!e.checked){g=[];for(c=0;c<a.cvalues.length;c++)g[c]=0;p=[];for(c=0;c<a.cvalues.length;c++)p[c]=0;for(var t=k;t<l;t++)for(var u=q;u<m;u++){var w=r[t][u],v=w.value;w.areas==e.areas&&(g[v]++,0==p[v]?p[v]=w.count:p[v]!=w.count&&(p[v]=99))}for(c=2;c<a.cvalues.length;c++)if(g[c]!=a.cvalues[c]||1!=c&&99==p[c])for(t=k;t<l;t++)for(u=q;u<m;u++){var x=r[t][u];x.areas==e.areas&&x.value==c&&(x.error=2)}}}catch(y){throw a.exception(y),y;}};a.paintCell=
function(b){try{var h=a.canvas.getContext("2d");h.fillStyle=a.uic.light[b.color];h.fillRect(b.px,b.py,a.unit.x,a.unit.y);a.paintSymbolMarkers(b);a.paintValueMarkers(b);1==b.value?a.paintCross(b,{scale:50,color:b.fixed?a.uic.clue:a.uic.text}):b.value!=nil&&(a.paintCircle(b,{fill:"#ffffff #ffcccc #66ff99 #ffff99 #bbffee #bbffee #ffffff #ffffff".split(" ")[b.value],stroke:a.uic.none,scale:80}),a.paintText(b.value.toString(),b,{color:b.fixed?a.uic.clue:a.uic.text}));b.error&&a.display.errors&&(b.value==
nil?a.paintErrorDot(b):a.paintErrorCircle(b))}catch(n){throw a.exception(n),n;}}}Fillodoku.prototype=new Puzzle;