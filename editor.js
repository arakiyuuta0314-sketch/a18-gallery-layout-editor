'use strict';
/* Reusable A18 concept layout editor; room manifests own geometry and sprites. */
(async()=>{
const $=s=>document.getElementById(s);
const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
const copy=o=>JSON.parse(JSON.stringify(o));
const same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
let room=null,objectIds=[],items={},start={},selected='',history=[],future=[],zoom=.8,mode='edit',drag=null;
const status=s=>{$('status').textContent=s;};
const errors=s=>{$('warning').textContent=s;};
const key=()=>('a18-layout-editor:'+room.id+':v1');
const layerRoot=$('scene-layers');
function defObj(o){return {x:Math.round(o.rect.x),y:Math.round(o.rect.y),w:o.rect.w,h:o.rect.h};}
function persistent(){try{localStorage.setItem(key(),JSON.stringify(items));}catch(_){}}
function normalized(input){
 const body=input.objects||input;
 if(input.roomId && input.roomId!==room.id)throw Error('別の展示室の配置です');
 const res={};
 for(const id of objectIds){
  const o=body[id],base=start[id];
  if(!o || !Number.isFinite(Number(o.x)) || !Number.isFinite(Number(o.y)))throw Error(id+' のX/Yが不正です');
  if(('w' in o && Number(o.w)!==base.w) || ('h' in o && Number(o.h)!==base.h))
    throw Error(id+' の寸法は変更できません');
  res[id]={...base,x:Math.round(Number(o.x)),y:Math.round(Number(o.y))};
 }
 return res;
}
const exportData=()=>({schema:'a18-gallery-layout-preview/v2',roomId:room.id,roomName:room.name,
 canvas:room.size,objects:copy(items)});
function overlap(a,b){return a.x<b.x+b.w && b.x<a.x+a.w && a.y<b.y+b.h && b.y<a.y+a.h;}
function warnings(){
 const l=room.limits||{left:0,right:0,top:0,bottom:0,clearRearCorridorY:0};
 const problems=[];
 for(let i=0;i<objectIds.length;i++){
  const id=objectIds[i],o=items[id],label=room.objects[i].label;
  if(o.x<l.left||o.x+o.w>room.size.width-l.right||o.y<l.top||o.y+o.h>room.size.height-l.bottom)
    problems.push(label+'が有効領域からはみ出しています');
  if(l.clearRearCorridorY && o.y<l.clearRearCorridorY)problems.push(label+'が上側通路に近いです');
  for(let j=i+1;j<objectIds.length;j++)if(overlap(o,items[objectIds[j]]))
    problems.push(label+'と'+room.objects[j].label+'が重なっています');
 }
 errors(problems.length?'⚠ '+problems.join('／'):'');
 for(const id of objectIds){
  const node=document.querySelector('[data-object="'+id+'"]');
  node.classList.toggle('invalid',problems.some(p=>p.includes(room.objects.find(o=>o.id===id).label)));
 }
}
function render(){
 if(!room)return;
 for(const id of objectIds){
  const o=items[id],node=document.querySelector('[data-object="'+id+'"]');
  Object.assign(node.style,{left:o.x+'px',top:o.y+'px',width:o.w+'px',height:o.h+'px',pointerEvents:mode==='edit'?'auto':'none'});
  node.classList.toggle('selected',selected===id);node.setAttribute('aria-pressed',String(id===selected));
 }
 for(const btn of document.querySelectorAll('[data-pick]')){
  const a=btn.dataset.pick===selected;btn.classList.toggle('primary',a);btn.setAttribute('aria-pressed',String(a));
 }
 const o=items[selected];
 for(const axis of ['x','y']){const field=$('coord-'+axis);field.value=o?o[axis]:'';field.disabled=!o;}
 $('dims').textContent=o?(o.w+' × '+o.h+' px'):'建築構造の確認のみ（展示壁は未配置）';
 for(const btn of document.querySelectorAll('[data-move]'))btn.disabled=!o;
 for(const id of ['reset','show-import','apply-import'])$(id).disabled=!o;
 $('json-preview').textContent=JSON.stringify(exportData(),null,2);
 $('undo').disabled=history.length===0;$('redo').disabled=future.length===0;
 warnings();
}
function commit(before,notice){
 if(same(before,items))return;
 history.push(copy(before));if(history.length>100)history.shift();future=[];
 persistent();render();status(notice||'配置を保存しました');
}
function choose(id){if(objectIds.includes(id)){selected=id;render();status(room.objects.find(x=>x.id===id).label+'を選択しました');}}
function change(id,target){
 const o=items[id];if(!o)return;
 const before=copy(items);
 const x=Number(target.x),y=Number(target.y);
 if(!Number.isFinite(x)||!Number.isFinite(y))return;
 o.x=clamp(Math.round(x),0,room.size.width-o.w);
 o.y=clamp(Math.round(y),0,room.size.height-o.h);
 commit(before,'座標を更新しました');
}
function setMode(m){
 if(!objectIds.length)m='pan';
 mode=m;
 $('edit-mode').setAttribute('aria-pressed',String(m==='edit'));
 $('pan-mode').setAttribute('aria-pressed',String(m==='pan'));
 render();
 status(!objectIds.length?'建築のみの確認モードです（展示壁は配置後に編集できます）':m==='edit'?'編集モード：指で設備を動かせます':'鑑賞モード：横にスクロールできます');
}
function zoomTo(z){
 zoom=z;$('stage').style.transform='scale('+z+')';
 $('outer').style.width=(room.size.width*z)+'px';$('outer').style.height=(room.size.height*z)+'px';
}
function toEntrance(){const e=$('scroller');e.scrollLeft=Number.isFinite(room.previewFocusX)?clamp(room.previewFocusX*zoom-e.clientWidth/2,0,e.scrollWidth-e.clientWidth):e.scrollWidth-e.clientWidth;}
function createImage(path,z){
 const e=document.createElement('img');e.src=path;e.alt='';e.draggable=false;e.className='art';
 e.style.width=room.size.width+'px';e.style.height=room.size.height+'px';e.style.zIndex=z;
 return e;
}
function createObject(cfg){
 const node=document.createElement('button');node.type='button';node.className='obj';
 node.dataset.object=cfg.id;node.setAttribute('aria-label',cfg.label+'を移動');
 const image=document.createElement('img');image.src=cfg.image;image.draggable=false;image.alt='';
 const handle=document.createElement('span');handle.className='handle';handle.textContent=cfg.label;
 node.append(image,handle);node.style.zIndex='4';
 node.addEventListener('pointerdown',e=>{
  if(mode!=='edit'||!e.isPrimary)return;
  e.preventDefault();choose(cfg.id);
  drag={id:cfg.id,pid:e.pointerId,startX:e.clientX,startY:e.clientY,old:copy(items)};
  node.setPointerCapture(e.pointerId);
 });
 node.addEventListener('pointermove',e=>{
  if(!drag||drag.pid!==e.pointerId||drag.id!==cfg.id)return;
  const b=drag.old[cfg.id],o=items[cfg.id];
  o.x=clamp(Math.round(b.x+(e.clientX-drag.startX)/zoom),0,room.size.width-o.w);
  o.y=clamp(Math.round(b.y+(e.clientY-drag.startY)/zoom),0,room.size.height-o.h);render();
 });
 function finish(e){
  if(!drag||drag.pid!==e.pointerId||drag.id!==cfg.id)return;
  const old=drag.old;drag=null;commit(old,cfg.label+'を移動しました');
 }
 node.addEventListener('pointerup',finish);node.addEventListener('pointercancel',finish);
 node.addEventListener('lostpointercapture',()=>{if(drag&&drag.id===cfg.id){const old=drag.old;drag=null;commit(old,cfg.label+'の移動を保存しました');}});
 node.addEventListener('click',()=>choose(cfg.id));
 return node;
}
async function loadRoom(id){
 const entry=catalog.rooms.find(r=>r.id===id);if(!entry)throw Error('展示室が見つかりません');
 const res=await fetch(entry.config,{cache:'no-store'});if(!res.ok)throw Error('展示室データの取得に失敗しました '+res.status);
 const next=await res.json();
 if(next.schema!=='a18-gallery-editor/room-v1'||next.id!==id||!Array.isArray(next.objects))throw Error('展示室の定義が不正です');
 room=next;objectIds=room.objects.map(o=>o.id);start=Object.fromEntries(room.objects.map(o=>[o.id,defObj(o)]));
 items=copy(start);
 try{const saved=localStorage.getItem(key());if(saved)items=normalized(JSON.parse(saved));}catch(e){console.warn('Invalid cached state',e);}
 selected=objectIds[0];history=[];future=[];
 $('room-title').textContent=room.name;$('room-subtitle').textContent=room.subtitle;
 $('room-edges').textContent=room.entrance+' ／ '+room.exit;
 $('stage').style.width=room.size.width+'px';$('stage').style.height=room.size.height+'px';
 layerRoot.innerHTML='';
 layerRoot.append(createImage(room.background,0));
 const grid=document.createElement('div');grid.id='checker';layerRoot.append(grid);
 const pick=$('pick-buttons');pick.innerHTML='';
 for(const obj of room.objects){
  layerRoot.append(createObject(obj));
  const btn=document.createElement('button');btn.className='btn';btn.dataset.pick=obj.id;btn.textContent=obj.label;
  btn.addEventListener('click',()=>choose(obj.id));pick.append(btn);
 }
 layerRoot.append(createImage(room.foreground,10));
 $('zoom').value=((!objectIds.length||room.id==='gallery3')&&window.innerWidth<500)?'.35':'.8';
 zoomTo(Number($('zoom').value));render();setMode(objectIds.length?'edit':'pan');
 history=[];future=[];render();requestAnimationFrame(toEntrance);
}
const catalog=await (async()=>{
 try{
  const r=await fetch('rooms/catalog.json',{cache:'no-store'});
  if(!r.ok)throw Error('展示室一覧 '+r.status);
  const c=await r.json();if(!c.rooms?.length)throw Error('展示室がありません');
  return c;
 }catch(e){errors('プレビューを読み込めませんでした。'+e.message);throw e;}
})();
for(const r of catalog.rooms){
 const o=document.createElement('option');o.value=r.id;o.textContent=r.name;$('room-select').append(o);
}
$('room-select').addEventListener('change',e=>loadRoom(e.target.value).catch(err=>errors(err.message)));
for(const btn of document.querySelectorAll('[data-move]')){
 btn.addEventListener('click',()=>{
  const [dx,dy]=btn.dataset.move.split(',').map(Number),o=items[selected];if(!o)return;change(selected,{x:o.x+dx,y:o.y+dy});
 });
}
for(const axis of ['x','y'])$('coord-'+axis).addEventListener('change',e=>{
 if(!items[selected])return;change(selected,{...items[selected],[axis]:Number(e.target.value)});
});
document.addEventListener('keydown',e=>{
 if(e.target.closest('input,select,textarea,button,summary'))return;
 const p={ArrowUp:[0,-1],ArrowDown:[0,1],ArrowLeft:[-1,0],ArrowRight:[1,0]}[e.key];
 if(p&&mode==='edit'&&items[selected]){e.preventDefault();const o=items[selected],v=e.shiftKey?10:1;
  change(selected,{x:o.x+p[0]*v,y:o.y+p[1]*v});}
});
$('edit-mode').onclick=()=>setMode('edit');$('pan-mode').onclick=()=>setMode('pan');
$('zoom').onchange=e=>zoomTo(Number(e.target.value));$('center-view').onclick=toEntrance;
$('grid-toggle').onclick=e=>{
 const active=$('checker').classList.toggle('active');e.currentTarget.setAttribute('aria-pressed',String(active));
};
$('undo').onclick=()=>{if(!history.length)return;future.push(copy(items));items=history.pop();persistent();render();status('元に戻しました');};
$('redo').onclick=()=>{if(!future.length)return;history.push(copy(items));items=future.pop();persistent();render();status('やり直しました');};
$('reset').onclick=()=>{
 if(!confirm('初期配置に戻しますか？'))return;
 const prev=copy(items);items=copy(start);commit(prev,'初期配置に戻しました');
};
async function copyText(t){
 try{await navigator.clipboard.writeText(t);return true;}catch(_){
 const e=document.createElement('textarea');e.value=t;document.body.append(e);e.select();const ok=document.execCommand('copy');e.remove();return ok;
 }
}
$('copy').onclick=async()=>{
 try{status(await copyText(JSON.stringify(exportData(),null,2))?'座標をコピーしました':'コピーできません。下のJSONを選択してください。');}
 catch(_){status('コピーできません。下のJSONを選択してください。');}
};
$('download').onclick=()=>{
 const blob=new Blob([JSON.stringify(exportData(),null,2)],{type:'application/json;charset=utf-8'}),
 url=URL.createObjectURL(blob),a=document.createElement('a');
 a.href=url;a.download='a18-'+room.id+'-layout.json';document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),3000);
 status('JSONファイルを保存しました');
};
$('show-import').onclick=()=>{$('json-text').style.display='block';$('apply-import').style.display='inline-block';};
$('apply-import').onclick=()=>{
 try{
  const before=copy(items),next=normalized(JSON.parse($('json-text').value));
  items=next;commit(before,'座標を読み込みました');
 }catch(e){status('読み込み失敗：'+e.message);}
};
const requested=new URLSearchParams(location.search).get('room');
await loadRoom(catalog.rooms.some(r=>r.id===requested)?requested:catalog.rooms[0].id);
$('room-select').value=room.id;
window.__A18_LAYOUT_EDITOR__={getState:exportData,select:choose,change,reset:()=>{items=copy(start);history=[];future=[];persistent();render();}};
})().catch(e=>{console.error('Editor initialization failed',e);document.getElementById('warning').textContent='読み込みに失敗しました：'+e.message;});
