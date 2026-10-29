"""Check reachable walking paths from each room center to all its visible exits."""
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
from pathlib import Path
from playwright.sync_api import sync_playwright
import threading
root=Path(r"C:\Users\User\source\repos\a18-gallery5-material-review")
srv=ThreadingHTTPServer(("127.0.0.1",0),partial(SimpleHTTPRequestHandler,directory=str(root)))
threading.Thread(target=srv.serve_forever,daemon=True).start()
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel="chrome",headless=True)
  p=b.new_page()
  p.goto(f"http://127.0.0.1:{srv.server_port}/movement-preview/")
  p.wait_for_function("window.__A18_MOVE_QA__ && window.__A18_MOVE_QA__.getState().ready")
  res=p.evaluate("""() => {
   const qa=window.__A18_MOVE_QA__,edges=qa.edges(),gates=qa.gates();
   const unit=12;
   const IX=75,IY=39;
   const at=(ix,iy)=>[20+ix*unit,110+iy*unit];
   const results=[];
   for(let r=0;r<6;r++){
     qa.forceRoom(r);
     const start=qa.getState(),startIx=Math.round((start.x-20)/unit),startIy=Math.round((start.y-110)/unit);
     const visited=new Set(),q=[];
     const add=(ix,iy)=>{
       if(ix<0||ix>=IX||iy<0||iy>=IY)return;
       const key=ix+','+iy;
       if(visited.has(key))return;
       const [x,y]=at(ix,iy);
       if(x<18||x>912||y>570||y<110||!qa.walkable(r,x,y))return;
       visited.add(key);q.push([ix,iy]);
     };
     add(startIx,startIy);
     for(let i=0;i<q.length;i++){const [x,y]=q[i];add(x-1,y);add(x+1,y);add(x,y-1);add(x,y+1);}
     for(const [dir,g] of Object.entries(gates[r])){
      const [cx,cy]=g.at;
      const goal=dir==='west'?[40,cy]:dir==='east'?[892,cy]:dir==='north'?[cx,cy+11]:[cx,cy-11];
      const found=q.some(([ix,iy])=>{const [x,y]=at(ix,iy);return Math.hypot(x-goal[0],y-goal[1])<20;});
      results.push({r,dir,to:edges[r][dir],reached:found,visited:visited.size,goal});
     }
   }return results;
  }""")
  for item in res:print(item)
  assert len(res)==14 and all(x["reached"] for x in res),"INACCESSIBLE ROUTES"
  print("PASS all 14 physical routes reachable from room spawn")
  b.close()
finally:srv.shutdown()
