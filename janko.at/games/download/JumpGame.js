function JumpGame(){var a=this;a.constructor();a.uis.puzzle=["Jump Game"];var g=a.board.c,k=0,h=0;a.enable.dragging=!0;a.enable.tilt=!0;a.enable.hint=!1;a.enable.check=!1;a.enable.colors=!1;a.enable.smarkers=!1;a.enable.values=!1;a.enable.pgrid=!0;a.enable.pgrid=!0;a.enable.pgridlines=!1;a.keypad.left=nil;a.keypad.right=nil;a.moves.collapse=!1;a.score.label=a.uis.get("moves");a.score.optimize=a.score.maximize;a.solutionToString=a.solutionToStringGame;a.showSolution=a.showSolutionGame;a.isNewSolution=
a.isNewSolutionGame;a.uim.cellCursor=3;a.uic.target="#333333";a.uic.targetNumber="#ffffff";a.infoText="\u2022";var n=null,p=null,b=null;a.init=function(){Object.getPrototypeOf(a).init.call(a)};a.run2=function(){try{a.config.mode==a.config.modeGame&&(a.level.size=(8).toString(),a.level.depth=(3).toString()),Object.getPrototypeOf(this).run2.call(this)}catch(c){throw a.exception(c),c;}};a.reset2=function(){try{b=null;k=a.size.x;h=a.size.y;if(a.level.problem)for(var c=0,e=a.level.problem.replace(/\s+/g,
" ").trim().split(" "),d=0;d<h;d++)for(var f=0;f<k;f++){var l=g[f][d],m=e[c++];l.label=parseInt(m)}a.level.solution?a.level.moves=a.level.solution:a.level.moves&&(a.level.solution=a.level.moves)}catch(q){throw a.exception(q),q;}};a.make2=function(){try{k=a.size.x;h=a.size.y;for(var c="",b=0;b<h;b++)for(var d=0;d<k;d++)c+=(a.random.getInt(a.size.z)+1).toString()+" ";a.level.problem=c;a.level.author="Otto Janko";a.level.source="Script/Gen";a.level.info=a.level.seed}catch(f){throw a.exception(f),f;}};
a.check2=function(){try{a.solved=null==b?!1:0<=b.x-b.label&&g[b.x-b.label][b.y].value==nil||b.x+b.label<k&&g[b.x+b.label][b.y].value==nil||0<=b.y-b.label&&g[b.x][b.y-b.label].value==nil||b.y+b.label<h&&g[b.x][b.y+b.label].value==nil?!1:!0}catch(c){throw a.exception(c),c;}};a.movesToString=function(){try{for(var c="",b="",d=0;d<a.moves.current+1;d++){var f=a.moves.list[d].split(",");b+=(parseInt(f[1])*h+parseInt(f[2])).toString()+",";if(50<b.length||d==a.moves.current)c+=b+"\n",b=""}return c}catch(l){throw a.exception(l),
l;}};a.movesFromString=function(c){try{a.checking.disable++;a.reset();a.moves.current=-1;a.moves.last=-1;c=c.replace(/[\s,;]+/g," ").trim();for(var b=c.split(" "),d=0;d<b.length;d++){var f=parseInt(b[d]);a.makeMove(g[Math.floor(f/h)][f%h],0,0)}}catch(l){ojdebug("Movelist: "+d+"\n",c),a.exception(l)}finally{a.checking.disable--}};a.dragToDxDy=function(c,b,d){a.moveToDxDy(c,b,d)};a.moveToDxDy=function(c,e){try{null==b?Object.getPrototypeOf(this).moveToDxDy.call(this,c,e):-1==c&&0<=b.x-b.label?a.makeMove(g[b.x-
b.label][b.y],nil,0):1==c&&b.x+b.label<k?a.makeMove(g[b.x+b.label][b.y],nil,0):-1==e&&0<=b.y-b.label?a.makeMove(g[b.x][b.y-b.label],nil,0):1==e&&b.y+b.label<h&&a.makeMove(g[b.x][b.y+b.label],nil,0)}catch(d){throw a.exception(d),d;}};a.makeMove2=function(c,e,d){try{a.solved||1==c.value||(a.display.cursor=!1,null==b?(b=c,a.score.current++,Object.getPrototypeOf(this).makeMove2.call(this,c,1,0)):c.valuel!=nil&&(c.x==b.x&&c.y==b.y+g[b.x][b.y].label||c.x==b.x&&c.y==b.y-g[b.x][b.y].label||c.y==b.y&&c.x==
b.x+g[b.x][b.y].label||c.y==b.y&&c.x==b.x-g[b.x][b.y].label)&&(b=c,a.score.current++,Object.getPrototypeOf(this).makeMove2.call(this,c,1,0)))}catch(f){throw a.exception(f),f;}};a.onRun=function(){try{if(a.config.mode==a.config.modeGame&&(a.enable.make=!0),Object.getPrototypeOf(this).onRun.call(this),a.config.mode==a.config.modeGame){for(var c=document.createElement("select"),b=6;12>=b;b+=1){var d=document.createElement("option");d.value=b.toString();d.textContent=b.toString()+"\u00d7"+b.toString();
c.appendChild(d)}c.value=8;c.style.position="relative";c.style.top="-6px";a.uie.toolbar.insertBefore(c,a.uie.make);n=c;c=document.createElement("select");for(b=2;5>=b;b+=1)d=document.createElement("option"),d.value=b.toString(),d.textContent="Farben: "+b.toString(),c.appendChild(d);c.value=3;c.style.position="relative";c.style.top="-6px";a.uie.toolbar.insertBefore(c,a.uie.make);p=c}}catch(f){throw a.exception(f),f;}};a.onMake=function(b){try{a.enable.make&&(a.level.depth=p.value,a.level.rows=a.level.cols=
n.value,a.setup())}catch(e){throw a.exception(e),e;}};a.paintInfo=function(b){try{b="",b+=a.uis.get("moves")+": "+a.score.current+" ("+a.score.best+") ["+a.score.high+"] ",Object.getPrototypeOf(this).paintInfo.call(this,b)}catch(e){throw a.exception(e),e;}};a.paintCell=function(c){try{var e=a.canvas.getContext("2d"),d=!1;c.value==nil&&null!=b&&(c.x==b.x&&c.y==b.y+b.label||c.x==b.x&&c.y==b.y-b.label||c.y==b.y&&c.x==b.x+b.label||c.y==b.y&&c.x==b.x-b.label)&&(d=!0);e.save();if(c.value!=nil)e.fillStyle=
a.uic.gray;else if(d)e.fillStyle=a.uic.target;else{var f=e.createRadialGradient(c.px+a.unit.x/2,c.py+a.unit.y/2,0,c.px+a.unit.x/2,c.py+a.unit.y/2,a.unit.x);f.addColorStop(0,"#eeeeee");f.addColorStop(.4,a.uic.light[c.label]);f.addColorStop(1,a.uic.dark[c.label]);e.fillStyle=f}e.fillRect(c.px,c.py,a.unit.x,a.unit.y);e.restore();b!=nil&&c==b&&a.paintCircle(c,{stroke:a.uic.black,fill:a.uic.none,width:2});e.lineWidth=2;e.beginPath();e.strokeStyle=a.uic.buttonBorderLight;dx=0==c.x?2:1;dy=0==c.y?2:1;e.moveTo(c.px+
dx,c.py+a.unit.y-1);e.lineTo(c.px+dx,c.py+dy);e.lineTo(c.px+a.unit.x-dx,c.py+dy);e.stroke();e.beginPath();e.strokeStyle=a.uic.buttonBorderDark;dy=dx=1;e.moveTo(c.px+a.unit.x-dx,c.py+dy);e.lineTo(c.px+a.unit.x-dx,c.py+a.unit.y-dy);e.lineTo(c.px+ +dx,c.py+a.unit.y-dy);e.stroke();var g=d?a.uic.targetNumber:a.uic.text;c.value!=nil&&c!=b||a.paintText(c.label.toString(),c,{color:g})}catch(m){throw a.exception(m),m;}}}JumpGame.prototype=new Puzzle;
