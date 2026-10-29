/* A18 930x582 approved-background walking QA. No persistent data edits. */
(() => {'use strict';
const W=930,H=582,$=id=>document.getElementById(id),ctx=$('scene').getContext('2d',{alpha:false}),world=$('world'),viewport=$('viewport');
const names=['エントランス','展示室1','展示室2','展示室3','展示室4','展示室5'];
const edges={0:{west:1,east:2,north:5},1:{east:0,north:3},2:{west:0,north:4},3:{south:1,east:5},4:{south:2,west:5},5:{south:0,west:3,east:4}};
const reverse={west:'east',east:'west',north:'south',south:'north'},glyph={north:'↑',south:'↓',west:'←',east:'→'};
const gates={
 0:{west:{at:[21,481],band:[433,557]},east:{at:[909,481],band:[433,557]},north:{at:[465,369],band:[414,516]}},
 1:{east:{at:[909,306],band:[262,354]},north:{at:[347,223],band:[300,403]}},
 2:{west:{at:[21,380],band:[306,454]},north:{at:[735,223],band:[680,791]}},
 3:{south:{at:[465,559],band:[411,530]},east:{at:[909,311],band:[268,360]}},
 4:{south:{at:[465,559],band:[409,531]},west:{at:[21,365],band:[300,435]}},
 5:{south:{at:[465,559],band:[402,532]},west:{at:[24,475],band:[366,543]},east:{at:[906,475],band:[366,543]}}
};
const arrivals={
 0:{west:[102,482],east:[826,482],north:[465,437]},
 1:{east:[804,296],north:[347,299]},
 2:{west:[123,278],north:[735,285]},
 3:{south:[465,490],east:[808,305]},
 4:{south:[465,496],west:[128,359]},
 5:{south:[465,500],west:[158,478],east:[772,478]}
};
const spawn={0:[465,520],1:[465,507],2:[465,517],3:[465,484],4:[465,482],5:[465,509]};
const state={room:0,x:465,y:520,dir:'front',gender:'curator',visits:[],blocked:0,ready:false,showPortals:true};
const bitmap=new Map(),configs=new Map(),down=new Set(),log=[];let last=0,portalCooldown=0;
function announce(message){
 log.unshift(message);if(log.length>14)log.pop();$('qa-log').textContent=log.join('\n');
 $('room-name').textContent=names[state.room];
 $('visit-status').textContent='実際に通過 '+state.visits.length+'回 ／ 遮られた動き '+state.blocked+'回';
 for(const el of $('map').querySelectorAll('button'))el.classList.toggle('active',Number(el.dataset.room)===state.room);
}
function loadImg(url){return new Promise((resolve,reject)=>{
 const im=new Image();im.onload=()=>im.naturalWidth&&im.naturalHeight?resolve(im):reject(Error('画像寸法不正 '+url));
 im.onerror=()=>reject(Error('読み込み失敗 '+url));im.src=url;
});}
function img(path){const im=bitmap.get(path);if(!im)throw Error('不足画像 '+path);return im;}
async function load(){
 const paths=new Set(['assets/entrance_background.png']);
 for(const role of ['curator','female'])for(const dir of ['front','back','left','right'])paths.add('assets/'+role+'-'+dir+'.png');
 for(let r=1;r<=5;r++){
  const resp=await fetch('../rooms/gallery'+r+'/room.json?rev=20261030',{cache:'no-store'});
  if(!resp.ok)throw Error('部屋設定取得に失敗 '+r);
  const data=await resp.json();
  if(data.id!=='gallery'+r||data.size.width!==W||data.size.height!==H)throw Error('部屋寸法が不一致 '+r);
  if(data.background!=='rooms/gallery'+r+'/background_approved.png')throw Error('承認素材と不一致 '+r);
  configs.set(r,data);paths.add('../'+data.background);
  if(data.foreground)paths.add('../'+data.foreground);
  for(const o of data.objects)paths.add('../'+o.image);
 }
 await Promise.all([...paths].map(async path=>bitmap.set(path,await loadImg(path))));
 const pairs=new Set();
 for(let room=0;room<6;room++)for(const [dir,to] of Object.entries(edges[room])){
  if(edges[to][reverse[dir]]!==room||!gates[room][dir]||!arrivals[room][dir])throw Error('館内通路の対応が不正');
  pairs.add([room,to].sort((a,b)=>a-b).join('-'));
 }
 if(pairs.size!==7)throw Error('通路が7本ではありません');
 state.ready=true;$('busy').style.display='none';announce('読み込み完了：7通路・14方向が通れます');draw();camera();
}
function floor(room,x,y){
 if(room===0)return y>=352||(x>=410&&x<=521&&y>=276);
 if(room===1)return y>=221||(x>=302&&x<=404&&y>=164);
 if(room===2)return y>=222||(x>=680&&x<=793&&y>=130);
 if(room===3)return y>=251||(x>=278&&x<=667&&y>=183);
 if(room===4)return y>=220;
 if(room===5)return y>=319||((x<=160||x>=770)&&y>=340);
 throw Error('不明な部屋');
}
function collides(room,x,y){
 const rs=configs.get(room)?.objects||[],radius=11,foot=y+4;
 for(const o of rs){
  const q=o.rect,xx=q.x+9,yy=q.y+q.h-28,ww=Math.max(1,q.w-18),hh=35;
  const px=Math.max(xx,Math.min(x,xx+ww)),py=Math.max(yy,Math.min(foot,yy+hh));
  if(Math.hypot(x-px,foot-py)<radius)return true;
 }return false;
}
function edgeAt(room,x,y,dx,dy){
 for(const [dir,g] of Object.entries(gates[room])){
  const [lo,hi]=g.band;
  if(dir==='west'&&dx<0&&x<=g.at[0]&&y>=lo&&y<=hi)return dir;
  if(dir==='east'&&dx>0&&x>=g.at[0]&&y>=lo&&y<=hi)return dir;
  if(dir==='north'&&dy<0&&y<=g.at[1]&&x>=lo&&x<=hi)return dir;
  if(dir==='south'&&dy>0&&y>=g.at[1]&&x>=lo&&x<=hi)return dir;
 }return null;
}
function step(dx,dy,seconds){
 if(!state.ready||(!dx&&!dy))return false;
 const dist=Math.min(Math.max(seconds,0),.055)*Number($('speed').value),len=Math.hypot(dx,dy);
 const x=state.x+dx/len*dist,y=state.y+dy/len*dist;
 state.dir=Math.abs(dx)>Math.abs(dy)?(dx<0?'left':'right'):(dy<0?'back':'front');
 if(portalCooldown<=0){
  const dir=edgeAt(state.room,x,y,dx,dy);
  if(dir){
   const from=state.room,to=edges[from][dir],pos=arrivals[to][reverse[dir]];
   if(to===undefined||!pos)throw Error('移動先定義エラー');
   state.room=to;state.x=pos[0];state.y=pos[1];
   if(!floor(to,state.x,state.y)||collides(to,state.x,state.y))throw Error('移動先が物体と重なります '+to);
   state.visits.push({from,to,dir});portalCooldown=.27;
   announce(names[from]+' '+glyph[dir]+' '+names[to]+'：移動成功');draw();camera();return true;
  }
 }
 if(x<18||x>912||y>570||y<110||!floor(state.room,x,y)||collides(state.room,x,y)){
  state.blocked++;return false;
 }
 state.x=x;state.y=y;return true;
}
function forceRoom(room){
 if(!Number.isInteger(room)||room<0||room>5)throw Error('不正な部屋番号');
 state.room=room;state.x=spawn[room][0];state.y=spawn[room][1];state.dir='front';portalCooldown=.28;
 if(!floor(room,state.x,state.y)||collides(room,state.x,state.y))throw Error('出現位置と壁が重なります '+room);
 announce(names[room]+'へデバッグ移動（通路通過数には含みません）');draw();camera();
}
function background(){
 if(state.room===0){
  const im=img('assets/entrance_background.png'),sourceH=im.naturalWidth*H/W;
  if(sourceH>im.naturalHeight)throw Error('入口画像比率不一致');
  ctx.drawImage(im,0,0,im.naturalWidth,sourceH,0,0,W,H);
 }else ctx.drawImage(img('../'+configs.get(state.room).background),0,0,W,H);
}
function sprites(){
 const config=configs.get(state.room);
 const painter=[{
  depth:state.y,draw(){
   const im=img('assets/'+state.gender+'-'+state.dir+'.png');
   ctx.fillStyle='rgba(17,14,11,.28)';ctx.beginPath();ctx.ellipse(state.x,state.y+4,16,6,0,0,2*Math.PI);ctx.fill();
   ctx.drawImage(im,Math.round(state.x-22),Math.round(state.y-56),44,57);
  }
 }];
 for(const o of config?.objects||[]){
  painter.push({depth:o.rect.y+o.rect.h-9,draw(){
   const r=o.rect;ctx.drawImage(img('../'+o.image),r.x,r.y,r.w,r.h);
  }});
 }
 painter.sort((a,b)=>a.depth-b.depth);
 for(const p of painter)p.draw();
 if(config?.foreground)ctx.drawImage(img('../'+config.foreground),0,0,W,H);
}
function tags(){
 if(!state.showPortals)return;
 ctx.font='bold 16px system-ui';ctx.textAlign='center';ctx.textBaseline='middle';
 for(const [dir,g] of Object.entries(gates[state.room])){
  const label=glyph[dir]+' '+names[edges[state.room][dir]],w=Math.max(86,ctx.measureText(label).width+24);
  const cx=Math.max(w/2+5,Math.min(W-w/2-5,g.at[0]));
  const cy=dir==='south'?535:((dir==='east'||dir==='west')?Math.min(518,g.at[1]):g.at[1]);
  ctx.fillStyle='rgba(20,39,32,.86)';ctx.strokeStyle='#d9b578';ctx.lineWidth=2;
  ctx.beginPath();ctx.roundRect(cx-w/2,cy-20,w,34,7);ctx.fill();ctx.stroke();
  ctx.fillStyle='#fff5df';ctx.fillText(label,cx,cy-2);
 }
}
function draw(){if(!state.ready)return;ctx.clearRect(0,0,W,H);background();sprites();tags();}
function camera(){
 if(!state.ready)return;
 const w=viewport.clientWidth,full=$('zoom-mode').value==='full';
 const scale=full?Math.min(w/W,1):Math.min(1,Math.max(.72,w/W));
 const h=full?H*scale:Math.min(H*scale,Math.max(310,Math.min(440,window.innerHeight*.46)));
 viewport.style.height=Math.round(h)+'px';
 const tx=W*scale<=w?(w-W*scale)/2:Math.max(w-W*scale,Math.min(0,w/2-state.x*scale));
 const ty=H*scale<=h?(h-H*scale)/2:Math.max(h-H*scale,Math.min(0,h/2-state.y*scale));
 world.style.transform='translate('+tx.toFixed(1)+'px,'+ty.toFixed(1)+'px) scale('+scale.toFixed(5)+')';
}
function tick(now){
 const dt=last?Math.min((now-last)/1000,.035):0;last=now;
 if(portalCooldown>0)portalCooldown=Math.max(0,portalCooldown-dt);
 let dx=0,dy=0;
 if(down.has('west'))dx--;if(down.has('east'))dx++;
 if(down.has('north'))dy--;if(down.has('south'))dy++;
 if(dx||dy){step(dx,dy,dt);draw();camera();}
 requestAnimationFrame(tick);
}
function controls(){
 const lookup={ArrowLeft:'west',ArrowRight:'east',ArrowUp:'north',ArrowDown:'south',a:'west',d:'east',w:'north',s:'south'};
 document.addEventListener('keydown',e=>{if(e.target.closest('input,select,button'))return;const dir=lookup[e.key];if(dir){e.preventDefault();down.add(dir);}});
 document.addEventListener('keyup',e=>{const dir=lookup[e.key];if(dir){e.preventDefault();down.delete(dir);}});
 window.addEventListener('blur',()=>down.clear());
 for(const btn of document.querySelectorAll('[data-dir]')){
  const dir=btn.dataset.dir;
  const release=()=>{down.delete(dir);btn.classList.remove('held');};
  btn.addEventListener('pointerdown',e=>{e.preventDefault();down.add(dir);btn.classList.add('held');btn.setPointerCapture(e.pointerId);});
  btn.addEventListener('pointerup',release);btn.addEventListener('pointercancel',release);
  btn.addEventListener('lostpointercapture',release);
 }
 $('reset-pos').onclick=()=>forceRoom(state.room);
 $('character').onchange=e=>{state.gender=e.target.value;draw();};
 $('show-portals').onchange=e=>{state.showPortals=e.target.checked;draw();};
 $('zoom-mode').onchange=camera;
 $('speed').onchange=()=>announce('移動速度を変更しました');
 window.addEventListener('resize',camera);
 for(const room of [3,5,4,1,0,2]){
  const b=document.createElement('button');b.type='button';b.textContent=names[room];b.dataset.room=room;
  b.onclick=()=>forceRoom(room);$('map').append(b);
 }
}
window.__A18_MOVE_QA__={
 getState:()=>({room:state.room,x:state.x,y:state.y,visits:state.visits.slice(),blocked:state.blocked,ready:state.ready}),
 edges:()=>JSON.parse(JSON.stringify(edges)),
 gates:()=>JSON.parse(JSON.stringify(gates)),
 arrivals:()=>JSON.parse(JSON.stringify(arrivals)),
 forceRoom,
 forcePosition:(x,y)=>{
  if(!Number.isFinite(x)||!Number.isFinite(y)||!floor(state.room,x,y)||collides(state.room,x,y))throw Error('不正なテスト立ち位置');
  state.x=x;state.y=y;portalCooldown=0;draw();camera();
 },
 step:(dir,seconds=.016)=>{
  if(!['west','east','north','south'].includes(dir))throw Error('不正な方向');
  portalCooldown=0;
  const vec={west:[-1,0],east:[1,0],north:[0,-1],south:[0,1]}[dir];
  const ok=step(vec[0],vec[1],seconds);draw();camera();return ok;
 },
 walkable:(r,x,y)=>floor(r,x,y)&&!collides(r,x,y),
 objectCount:r=>configs.get(r)?.objects.length??0
};
controls();
load().catch(e=>{$('busy').textContent='読み込みエラー：'+e.message;console.error(e);});
requestAnimationFrame(tick);
})();