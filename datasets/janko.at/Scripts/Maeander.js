function Maeander(){var a=this;a.constructor();a.uis.puzzle=["Maeander","M\u00e4ander"];a.charToValue=a.charToValue.concat(["/",1,"\\",2,"o",3,".",3,"x",0,",",0,"0",nil,"-",nil]);a.cell.values=[3,1,2,0,nil];a.enable.dragging=!0;a.keypad.left=nil;a.keypad.right=a.keypad.values;a.cell.nilalias=0;a.labels.north=a.labels.west=2;a.uic.line="#666666";a.init=function(){Object.getPrototypeOf(a).init.call(a)};a.reset2=function(){try{a.keypadValues=[["/",1],["\\",2],[a.paintCross,0],["o",3],["\u2022",nil]];
if(a.level.problem){var c=0;var b=a.level.problem.replace(/\s+/g," ").trim().split(" ");for(var d=2;d<a.size.y;d++)for(var e=2;e<a.size.x;e++){var f=a.board.c[e][d];var g=b[c++];"-"!=g&&"."!=g&&("/"==g?f.value=1:"\\"==g?f.value=2:"x"==g&&(f.value=0));f.value!=nil&&(f.fixed=!0)}}if(a.level.clabels)for(c=0,b=a.level.clabels.replace(/\s+/g," ").trim().split(" "),d=0;2>d;d++)for(e=2;e<a.size.x;e++)f=a.board.c[e][d],g=b[c++],"-"!=g&&"."!=g&&(f.label=parseInt(g));if(a.level.rlabels)for(c=0,b=a.level.rlabels.replace(/\s+/g,
" ").trim().split(" "),e=0;2>e;e++)for(d=2;d<a.size.y;d++)f=a.board.c[e][d],"-"!=g&&"."!=g&&(f.label=parseInt(g));if(a.level.solution)for(c=0,b=a.level.solution.replace(/\s+/g," ").trim().split(" "),d=2;d<a.size.y;d++)for(e=2;e<a.size.x;e++)f=a.board.c[e][d],g=b[c++],"-"!=g&&"."!=g&&("/"==g?f.solution=1:"\\"==g&&(f.solution=2));if(a.level.solution&&!a.level.rlabels&&!a.level.clabels){for(e=0;2>e;e++)for(d=2;d<a.size.y;d++)a.board.c[e][d].label=0;for(d=0;2>d;d++)for(e=2;e<a.size.x;e++)a.board.c[e][d].label=
0;for(e=2;e<a.size.x;e++)for(d=2;d<a.size.y;d++)2==a.board.c[e][d].solution?(a.board.c[e][0].label++,a.board.c[0][d].label++):1==a.board.c[e][d].solution&&(a.board.c[e][1].label++,a.board.c[1][d].label++)}a.reset2labels()}catch(h){throw a.exception(h),h;}};a.check2=function(){var c;try{for(var b=a.board.c,d=2;d<a.size.x;d++){var e=c=0;for(var f=2;f<a.size.y;f++)2==b[d][f].value?c++:1==b[d][f].value&&e++;b[d][0].label!=nil&&b[d][0].label!=c&&(b[d][0].error=2);b[d][1].label!=nil&&b[d][1].label!=e&&
(b[d][1].error=2)}for(f=2;f<a.size.y;f++){e=c=0;for(d=2;d<a.size.x;d++)2==b[d][f].value?c++:1==b[d][f].value&&e++;b[0][f].label!=nil&&b[0][f].label!=c&&(b[0][f].error=2);b[1][f].label!=nil&&b[1][f].label!=e&&(b[1][f].error=2)}e=0;c=[];for(var g=0;g<2*a.size.x+2*a.size.y;g++)c[g]=0;g=0;for(d=2;d<a.size.x-1;d++)1==b[d][2].value&&1==b[d+1][2].value&&(c[g++]=b[d+1][2],1==g&&(e=4)),2==b[d][2].value&&2==b[d+1][2].value&&(c[g++]=b[d][2],1==g&&(e=1)),1==b[d][a.size.y-1].value&&1==b[d+1][a.size.y-1].value&&
(c[g++]=b[d][a.size.y-1],1==g&&(e=1)),2==b[d][a.size.y-1].value&&2==b[d+1][a.size.y-1].value&&(c[g++]=b[d+1][a.size.y-1],1==g&&(e=4));for(f=2;f<a.size.y-1;f++)1==b[2][f].value&&1==b[2][f+1].value&&(c[g++]=b[2][f+1],1==g&&(e=8)),2==b[2][f].value&&2==b[2][f+1].value&&(c[g++]=b[2][f],1==g&&(e=2)),1==b[a.size.x-1][f].value&&1==b[a.size.x-1][f+1].value&&(c[g++]=b[a.size.x-1][f],1==g&&(e=2)),2==b[a.size.x-1][f].value&&2==b[a.size.x-1][f+1].value&&(c[g++]=b[a.size.x-1][f+1],1==g&&(e=8));2!=g&&(a.solved=
!1);for(var h=c[0];a.solved;){h.count++;3==h.count&&(a.solved=!1);g=h;switch(e){case 1:h.x<a.size.x-1&&(h=b[h.x+1][h.y]);break;case 4:2<h.x&&(h=b[h.x-1][h.y]);break;case 2:h.y<a.size.y-1&&(h=b[h.x][h.y+1]);break;case 8:2<h.y&&(h=b[h.x][h.y-1])}if(g==h){h!=c[1]&&(a.solved=!1);break}switch(e){case 1:1==h.value?e=8:2==h.value?e=2:a.solved=!1;break;case 4:1==h.value?e=2:2==h.value?e=8:a.solved=!1;break;case 2:1==h.value?e=4:2==h.value?e=1:a.solved=!1;break;case 8:1==h.value?e=1:2==h.value?e=4:a.solved=
!1}}for(d=2;d<a.size.x;d++)for(f=2;f<a.size.y;f++)b[d][f].value!=nil&&0!=b[d][f].value&&0==b[d][f].count&&(b[d][f].error=1)}catch(k){throw a.exception(k),k;}};a.valueToString=function(a,b){switch(a){case 0:return b?"x":"-";case 3:return"?";case 1:return"/";case 2:return"\\";case nil:return"-";default:return"%"}};a.paintCell=function(c){try{c.areas==a.cell.label?a.paintLabelCell(c):a.paintValueCell(c)}catch(b){throw a.exception(b),b;}};a.paintLabelCell=function(c){try{var b=a.canvas.getContext("2d");
b.fillStyle=a.uic.label;b.fillRect(c.px,c.py,a.unit.x,a.unit.y);0==c.x&&0==c.y&&(b.lineWidth=2,b.strokeStyle=b.fillStyle=a.uic.line,a.paintBSlash(c,{scale:70}),a.paintSquare(c,{width:1,stroke:a.uic.grid,scale:100}));1==c.x&&1==c.y&&(b.lineWidth=2,b.strokeStyle=b.fillStyle=a.uic.line,a.paintFSlash(c,{scale:70}),a.paintSquare(c,{width:1,stroke:a.uic.grid,scale:100}));c.label!=nil&&a.paintText(c.label.toString(),c);c.error&&a.display.errors&&a.paintErrorCircle(c)}catch(d){throw a.exception(d),d;}};a.paintValueCell=
function(c){try{var b=a.canvas.getContext("2d");b.fillStyle=a.uic.light[c.color];b.fillRect(c.px,c.py,a.unit.x,a.unit.y);b.strokeStyle=b.fillStyle=c.fixed?a.uic.clue:a.uic.line;switch(c.value){case 1:a.paintFSlash(c);break;case 2:a.paintBSlash(c);break;case 0:a.paintCross(c);break;case 3:a.paintCircle(c,{scale:30})}a.paintSymbolMarkers(c);c.error&&a.display.errors&&(c.value==nil?a.paintErrorDot(c):a.paintErrorCircle(c))}catch(d){throw a.exception(d),d;}};a.paintFSlash=function(c,b){try{if(b=a.defaultParams(c,
b)){c.px&&(c=a.canvas.getContext("2d"));c.strokeStyle=b.stroke?b.stroke:a.uic.line;c.fillStyle=b.fill?b.fill:a.uic.line;c.lineWidth=b.width?b.width:1;var d=Math.min(Math.floor(a.unit.x/12),2);c.beginPath();c.moveTo(b.x+b.w-d,b.y);c.lineTo(b.x+b.w,b.y);c.lineTo(b.x+b.w,b.y+d);c.lineTo(b.x+d,b.y+b.h);c.lineTo(b.x,b.y+b.h);c.lineTo(b.x,b.y+b.h-d);c.lineTo(b.x+b.w-d,b.y);c.stroke();c.fill()}}catch(e){throw a.exception(e),e;}};a.paintBSlash=function(c,b){try{if(b=a.defaultParams(c,b)){c.px&&(c=a.canvas.getContext("2d"));
c.strokeStyle=b.stroke?b.stroke:a.uic.slashedge;c.fillStyle=b.fill?b.fill:a.uic.slashfill;c.lineWidth=b.width?b.width:1;var d=Math.min(Math.floor(a.unit.x/12),2);c.beginPath();c.moveTo(b.x,b.y);c.lineTo(b.x+d,b.y);c.lineTo(b.x+b.w,b.y+b.h-d);c.lineTo(b.x+b.w,b.y+b.h);c.lineTo(b.x+b.w-d,b.y+b.h);c.lineTo(b.x,b.y+d);c.lineTo(b.x,b.y);c.stroke();c.fill()}}catch(e){throw a.exception(e),e;}};a.paintCurrentValue=function(){try{var c=a.uie.value,b=c.getContext("2d");b.fillStyle=a.uic.white;b.fillRect(0,
0,c.width,c.height);b.strokeStyle=b.fillStyle=a.uic.line;var d={x:0,y:0,w:c.width,h:c.height,scale:90};switch(a.current.value){case 1:a.paintFSlash(b,d);break;case 2:a.paintBSlash(b,d);break;case 3:d.scale=30;a.paintCircle(b,d);break;case 0:a.paintCross(b,d)}}catch(e){throw a.exception(e),e;}}}Maeander.prototype=new Puzzle;