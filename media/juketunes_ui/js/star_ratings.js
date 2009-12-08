/* AJAX Star Rating : v1.0.3 : 2008/05/06 */
/* http://www.nofunc.com/AJAX_Star_Rating/ */

function agent(v) { 
	return(Math.max(navigator.userAgent.toLowerCase().indexOf(v),0)); 
}
function abPos(o) { 
	var o=(typeof(o)=='object'?o:$(o)), z={X:0,Y:0}; 
	while(o!=null) { 
		z.X+=o.offsetLeft; 
		z.Y+=o.offsetTop; 
		o=o.offsetParent; 
	}; 
	return(z); }
function XY(e,v) { 
	var o;
	if agent('msie') {
		o = {'X':event.clientX+document.body.scrollLeft, 
			 'Y':event.clientY+document.body.scrollTop};
	} else {
		o = {'X':e.pageX,'Y':e.pageY};
	} 
	return(v?o[v]:o); 
}

star={};

star.getPerc()

star.mouse=function(e,o) { 
	if(star.stop || isNaN(star.stop)) { 
		star.stop=0;

		document.onmousemove=function(e) { 
			var n=star.num;
		
			var p=abPos($('star'+n)), x=XY(e), oX=x.X-p.X, oY=x.Y-p.Y; 
			star.num=o.id.substr(4);
	
			if(oX<1 || oX>84 || oY<0 || oY>19) { 
				star.stop=1; 
				star.revert(); 
			} else {
	
				$('starCur'+n).setStyle({width:oX+'px'});
				$('starCur'+n).title=Math.round(oX/84*100)+'%';
			}
		};
	} 
};

star.update=function(e,o, url) { 
	var n=star.num, v=parseInt($('starCur'+n).title);

	n=o.id.substr(4); $('starCur'+n).title=v;

	req=new XMLHttpRequest(); 
	req.open('GET',url +'?rating='+(v/100),false); 
	req.send(null);    
};

star.revert=function() { 
	var n=star.num, v=parseInt($('starCur'+n).title);

	$('starCur'+n).setStyle({width: Math.round(v*84/100)+'px'});
	$('starCur'+n).title=(v>0?Math.round(v)+'%':'');
	
	document.onmousemove='';

};

star.num=0;
