function Mastermind(){var a=this;a.constructor();a.uis.puzzle=["Master Mind"];a.enable.vmarkers=!0;a.enable.values=!1;a.enable.currentValue=!1;a.labels.east=2;a.uis.duplicates=["Dup"];a.charToValue=a.charToValue.concat(["0",nil,"/",nil,"-",nil,",",nil]);a.init=function(){Object.getPrototypeOf(a).init.call(a)};a.reset2=function(){var b;try{a.size.z==nil&&(a.size.z=a.size.x-2);a.cell.min=1;a.cell.max=a.size.z;a.infoText=a.uis.get("numbers")+": 1~"+a.size.z+", ";a.infoText+=a.uis.get("duplicates")+": ";
a.level.options.contains("unique")?a.infoText+=a.uis.get("no"):a.infoText+=a.uis.get("yes");a.cell.values=[];var d=0;for(b=1;b<=a.size.z;b++)a.cell.values[d++]=b;a.cell.values[d++]=nil;d=a.size.z;a.keypadValues=a.keypad.numbers.slice(0,d);a.keypadValues[d++]=["\u2022",nil];if(a.level.problem){b=0;var h=a.level.problem.replace(/\s+/g," ").trim().split(" ");for(var c=0;c<a.size.y;c++)for(var e=0;e<a.size.x;e++){var g=a.board.c[e][c];var f=h[b++];g.value="."==f||"-"==f?g.solution=nil:g.solution=parseInt(f);
g.value!=nil&&(g.fixed=!0)}}if(a.level.solution)for(b=0,h=a.level.solution.replace(/\s+/g," ").trim().split(" "),e=0;e<a.size.x-2;e++)g=a.board.c[e][a.size.y-1],f=h[b++],g.solution="."==f||"-"==f||"0"==f?nil:parseInt(f);for(c=0;c<a.size.y;c++)for(e=0;e<a.size.x;e++)g=a.board.c[e][c],g.areas=e>=a.size.x-2?a.cell.label:c!=a.size.y-1?2:1}catch(k){throw a.exception(k),k;}};a.check2=function(){try{for(var b=0,d=[],h=[],c=0;c<a.size.x-2;c++)a.board.c[c][a.size.y-1].value==nil&&(a.board.c[c][a.size.y-1].error=
1);for(var e=0;e<a.size.y-1;e++){for(c=0;c<a.size.x-2;c++)d[c]=a.board.c[c][e].value,h[c]=a.board.c[c][a.size.y-1].value;for(c=b=0;c<a.size.x-2;c++)h[c]==d[c]&&(b++,d[c]=nil-1,h[c]=nil);var g=a.board.c[a.size.x-2][e];g.value!=nil&&g.value!=b&&(g.error=2);for(var f=b=0;f<a.size.x-2;f++)for(var k=0;k<a.size.x-2;k++)h[f]==d[k]&&(b++,d[k]=nil-1,h[f]=nil);g=a.board.c[a.size.x-1][e];g.value!=nil&&g.value!=b&&(g.error=2)}if(a.level.options.contains("unique"))for(f=0;f<a.size.x-3;f++)for(k=f+1;k<a.size.x-
2;k++)a.board.c[f][a.size.y-1].value==a.board.c[k][a.size.y-1].value&&(a.board.c[f][a.size.y-1].error=a.board.c[k][a.size.y-1].error=3)}catch(l){throw a.exception(l),l;}};a.solutionToString=function(b){try{for(var d="solution\n",h=0;h<a.size.x-2;h++){var c=a.board.c[h][a.size.y-1];d+=a.valueToString(b?c.solution:c.value)+" "}d=d.rtrim()+"\n";return d+"end\n"}catch(e){throw a.exception(e),e;}};a.paintCell=function(b){try{b.areas==a.cell.label?a.paintLabelCell(b):a.paintValueCell(b)}catch(d){throw a.exception(d),
d;}};a.paintLabelCell=function(b){try{a.canvas.getContext("2d"),b.x==a.size.x-1?(a.paintCircle(b,{fill:a.uic.white,stroke:a.uic.black,scale:80}),b.value!=nil&&a.paintText(b.value.toString(),b,{color:a.uic.black})):(a.paintCircle(b,{fill:a.uic.black,stroke:a.uic.black,scale:80}),b.value!=nil&&a.paintText(b.value.toString(),b,{color:a.uic.white})),b.error&&a.display.errors&&a.paintErrorCircle(b)}catch(d){throw a.exception(d),d;}};a.paintValueCell=function(b){try{var d=a.canvas.getContext("2d");d.fillStyle=
a.uic.light[b.color];d.fillRect(b.px,b.py,a.unit.x,a.unit.y);a.paintSymbolMarkers(b);a.paintValueMarkers(b);b.value!=nil&&a.paintText(b.value.toString(),b);b.error&&a.display.errors&&(b.value==nil?a.paintErrorDot(b):a.paintErrorCircle(b))}catch(h){throw a.exception(h),h;}}}Mastermind.prototype=new Puzzle;