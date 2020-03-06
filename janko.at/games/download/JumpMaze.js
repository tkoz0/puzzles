var $jscomp=$jscomp||{};$jscomp.scope={};$jscomp.ASSUME_ES5=!1;$jscomp.ASSUME_NO_NATIVE_MAP=!1;$jscomp.ASSUME_NO_NATIVE_SET=!1;$jscomp.defineProperty=$jscomp.ASSUME_ES5||"function"==typeof Object.defineProperties?Object.defineProperty:function(a,e,f){a!=Array.prototype&&a!=Object.prototype&&(a[e]=f.value)};$jscomp.getGlobal=function(a){return"undefined"!=typeof window&&window===a?a:"undefined"!=typeof global&&null!=global?global:a};$jscomp.global=$jscomp.getGlobal(this);$jscomp.SYMBOL_PREFIX="jscomp_symbol_";
$jscomp.initSymbol=function(){$jscomp.initSymbol=function(){};$jscomp.global.Symbol||($jscomp.global.Symbol=$jscomp.Symbol)};$jscomp.Symbol=function(){var a=0;return function(e){return $jscomp.SYMBOL_PREFIX+(e||"")+a++}}();
$jscomp.initSymbolIterator=function(){$jscomp.initSymbol();var a=$jscomp.global.Symbol.iterator;a||(a=$jscomp.global.Symbol.iterator=$jscomp.global.Symbol("iterator"));"function"!=typeof Array.prototype[a]&&$jscomp.defineProperty(Array.prototype,a,{configurable:!0,writable:!0,value:function(){return $jscomp.arrayIterator(this)}});$jscomp.initSymbolIterator=function(){}};$jscomp.arrayIterator=function(a){var e=0;return $jscomp.iteratorPrototype(function(){return e<a.length?{done:!1,value:a[e++]}:{done:!0}})};
$jscomp.iteratorPrototype=function(a){$jscomp.initSymbolIterator();a={next:a};a[$jscomp.global.Symbol.iterator]=function(){return this};return a};$jscomp.iteratorFromArray=function(a,e){$jscomp.initSymbolIterator();a instanceof String&&(a+="");var f=0,k={next:function(){if(f<a.length){var l=f++;return{value:e(l,a[l]),done:!1}}k.next=function(){return{done:!0,value:void 0}};return k.next()}};k[Symbol.iterator]=function(){return k};return k};
$jscomp.polyfill=function(a,e,f,k){if(e){f=$jscomp.global;a=a.split(".");for(k=0;k<a.length-1;k++){var l=a[k];l in f||(f[l]={});f=f[l]}a=a[a.length-1];k=f[a];e=e(k);e!=k&&null!=e&&$jscomp.defineProperty(f,a,{configurable:!0,writable:!0,value:e})}};$jscomp.polyfill("Array.prototype.keys",function(a){return a?a:function(){return $jscomp.iteratorFromArray(this,function(a){return a})}},"es6","es3");
$jscomp.checkStringArgs=function(a,e,f){if(null==a)throw new TypeError("The 'this' value for String.prototype."+f+" must not be null or undefined");if(e instanceof RegExp)throw new TypeError("First argument to String.prototype."+f+" must not be a regular expression");return a+""};
$jscomp.polyfill("String.prototype.startsWith",function(a){return a?a:function(a,f){var e=$jscomp.checkStringArgs(this,a,"startsWith");a+="";var l=e.length,q=a.length;f=Math.max(0,Math.min(f|0,e.length));for(var m=0;m<q&&f<l;)if(e[f++]!=a[m++])return!1;return m>=q}},"es6","es3");
function JumpMaze(){var a=this;a.constructor();a.uis.puzzle=["Jump Maze","Sprunglabyrinth"];var e=a.board.c,f=a.board.h,k=a.board.v,l=0,q=0;a.enable.dragging=!0;a.enable.swiping=!0;a.enable.tilt=!0;a.enable.hint=!1;a.enable.check=!1;a.enable.colors=!1;a.enable.smarkers=!1;a.enable.values=!1;a.enable.plines=!0;a.enable.pcursor=!1;a.keypad.left=nil;a.keypad.right=nil;a.moves.collapse=!1;a.score.label=a.uis.get("moves");a.score.optimize=a.score.minimize;a.solutionToString=a.solutionToStringGame;a.isNewSolution=
a.isNewSolutionGame;a.showSolution=a.showSolutionGame;a.keys=a.keys.concat(["steps"]);a.uic.ballFill="#cc0000";a.uic.ballEdge="#660000";a.uic.ballText="#ffffff";a.uic.goalEdge="#000000";a.uic.goalFill=a.uic.none;a.uis.steps=["Jumps","Spr\u00fcnge","Sauts","Salti"];a.infoText="\u2022";var m=[],p=0,u="",b=null,v=null;a.init=function(){Object.getPrototypeOf(a).init.call(a)};a.reset2=function(){var c;try{l=a.size.x;q=a.size.y;p=0;a.level.areas&&a.reset2areas(0,0,l,q,a.level.areas);if(a.level.steps)for(m=
[],u=a.level.steps,c=0;c<u.length;c++)m[c]=parseInt(u.substring(c,c+1));if(a.level.problem){c=0;for(var t=a.level.problem.replace(/\s+/g," ").trim().split(" "),d=0;d<q;d++)for(var g=0;g<l;g++){var h=e[g][d],n=t[c++];n.startsWith("x")&&(h.value=1,b=h,n=n.substring(1));n.startsWith("g")&&(h.label=4,v=h,n=n.substring(1));n=parseInt(n);var r=Math.floor(n/100);0!=r&&(h.label=4,v=h);r=Math.floor(n%100/10);0!=r&&(h.value=1,b=h);r=n%10;0!=(r&8)&&(f[g][d].value=a.line.wall);0!=(r&2)&&(f[g][d+1].value=a.line.wall);
0!=(r&4)&&(k[g][d].value=a.line.wall);0!=(r&1)&&(k[g+1][d].value=a.line.wall)}}a.level.solution?a.level.moves=a.level.solution:a.level.moves&&(a.level.solution=a.level.moves)}catch(w){throw a.exception(w),w;}};a.check2=function(){try{if(b==v)a.result.code=a.result.won;else{var c=m[p];b.x+c<l&&a.checkMove(e[b.x+c][b.y])&&(a.solved=!1);b.y+c<q&&a.checkMove(e[b.x][b.y+c])&&(a.solved=!1);0<=b.x-c&&a.checkMove(e[b.x-c][b.y])&&(a.solved=!1);0<=b.y-c&&a.checkMove(e[b.x][b.y-c])&&(a.solved=!1);a.solved&&
(a.result.code=a.result.lost)}}catch(t){throw a.exception(t),t;}};a.checkMove=function(c){try{var e=m[p];if(c.y==b.y&&c.x>b.x){for(var d=1;d<=e;d++)if(k[b.x+d][b.y].value==a.line.wall)return!1;return!0}if(c.y==b.y&&c.x<b.x){for(d=0;d<e;d++)if(k[b.x-d][b.y].value==a.line.wall)return!1;return!0}if(c.x==b.x&&c.y>b.y){for(d=1;d<=e;d++)if(f[b.x][b.y+d].value==a.line.wall)return!1;return!0}if(c.x==b.x&&c.y<b.y){for(d=0;d<e;d++)if(f[b.x][b.y-d].value==a.line.wall)return!1;return!0}return!1}catch(g){throw a.exception(g),
g;}};a.dragToDxDy=function(c,b,d){a.moveToDxDy(c,b,d)};a.moveToDxDy=function(c,f){try{var d=m[p];0<c&&b.x+d<l&&a.makeMove(e[b.x+d][b.y],null,null);0<f&&b.y+d<q&&a.makeMove(e[b.x][b.y+d],null,null);0>c&&0<=b.x-d&&a.makeMove(e[b.x-d][b.y],null,null);0>f&&0<=b.y-d&&a.makeMove(e[b.x][b.y-d],null,null)}catch(g){throw a.exception(g),g;}};a.makeMove2=function(c,f,d){try{if(!a.solved){var g=m[p];if(c.y==b.y&&c.x>b.x&&b.x+g<l)c=e[b.x+g][b.y],c.movedata="e";else if(c.y==b.y&&c.x<b.x&&0<=b.x-g)c=e[b.x-g][b.y],
c.movedata="w";else if(c.x==b.x&&c.y>b.y&&b.y+g<q)c=e[b.x][b.y+g],c.movedata="s";else if(c.x==b.x&&c.y<b.y&&0<=b.y-g)c=e[b.x][b.y-g],c.movedata="n";else return;a.checkMove(c)&&(Object.getPrototypeOf(this).makeMove2.call(this,c,1,d),b.value=nil,b=c,p++,p==m.length&&(p=0),a.score.current++)}}catch(h){throw a.exception(h),h;}};a.movesToString=function(){try{for(var c="",b="",d=0;d<a.moves.current+1;d++){var e=a.moves.list[d].split(",");b+=e[6];if(50<b.length||d==a.moves.current)c+=b+"\n",b=""}return c}catch(h){throw a.exception(h),
h;}};a.movesFromString=function(c){try{a.checking.disable++;a.reset();a.moves.current=-1;a.moves.last=-1;c=c.replace(/[\s,;]+/g,"").trim().toLowerCase();for(var f=0;f<c.length;f++){var d=b.x,g=b.y,h=m[p];switch(c[f]){case "e":d+=h;break;case "w":d-=h;break;case "s":g+=h;break;case "n":g-=h}a.makeMove(e[d][g],null,0)}}catch(n){ojdebug("Movelist: "+f+"\n",c),a.exception(n)}finally{a.checking.disable--}};a.paintInfo=function(c){try{c=a.uis.get("steps")+": "+m[p].toString()+" ("+m+") \u2022 ",c+=a.uis.get("moves")+
": "+a.score.current+" ("+a.score.best+") ["+a.score.high+"] ",Object.getPrototypeOf(this).paintInfo.call(this,c)}catch(t){throw a.exception(t),t;}};a.paintCell=function(c){try{var b=a.canvas.getContext("2d");b.fillStyle=a.uic.light[0];b.fillRect(c.px,c.py,a.unit.x,a.unit.y);4==c.label&&(a.paintCircle(c,{fill:a.uic.goalFill,stroke:a.uic.goalEdge,width:1,scale:70}),a.paintCircle(c,{fill:a.uic.goalFill,stroke:a.uic.goalEdge,width:1,scale:50}),a.paintCircle(c,{fill:a.uic.goalFill,stroke:a.uic.goalEdge,
width:1,scale:30}),a.paintCircle(c,{fill:a.uic.goalFill,stroke:a.uic.goalEdge,width:1,scale:10}));1==c.value&&(a.paintCircle(c,{fill:a.uic.ballFill,stroke:a.uic.ballEdge,scale:60}),a.paintText(m[p].toString(),c,{color:a.uic.ballText,scale:50}))}catch(d){throw a.exception(d),d;}}}JumpMaze.prototype=new Puzzle;
