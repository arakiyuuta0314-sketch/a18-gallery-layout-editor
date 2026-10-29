from pathlib import Path
from PIL import Image,ImageDraw,ImageEnhance
import numpy as np,cv2
r=Path(r'C:\Users\User\source\repos\a18-gallery5-material-review')
p=r/'architecture-review/gallery5/gallery5_v04_authentic_entrance_material_REVIEW.png'
im=np.array(Image.open(p).convert('RGB'))
source=np.array(Image.open(r'C:\Users\User\source\repos\web-tools-preview-a18-entrance-2d-assets-20261028\a18\layout-test\assets\entrance\approved_initial_20261027\entrance_background_initial_approved.png').convert('RGB'))
# Real wood doorway casing from the approved entrance, transformed to the side portals.
for right in [False,True]:
 patch=source[105:510,568:806].copy()
 # Preserve original carved wood surround; darken interior to indicate a passable corridor, not a closed door.
 patch[:,:,:]=np.array([10,30,26],dtype=np.uint8); patch[:28,:,:]=source[35:63,70:308]; patch[:,0:23,:]=source[105:510,515:538]; patch[:,215:238,:]=source[105:510,515:538]; patch[365:405,:,:]=source[470:510,70:308]
 sh,sw=patch.shape[:2]
 target=np.float32([[33,282],[148,291],[158,541],[28,568]])
 if right:target[:,0]=929-target[:,0]
 src=np.float32([[0,0],[sw-1,0],[sw-1,sh-1],[0,sh-1]])
 matrix=cv2.getPerspectiveTransform(src,target)
 warped=cv2.warpPerspective(patch,matrix,(930,582),flags=cv2.INTER_LINEAR)
 mask=cv2.warpPerspective(np.full((sh,sw),255,dtype=np.uint8),matrix,(930,582))
 alpha=(mask.astype(np.float32)/255.0)[:,:,None]
 im=np.uint8(im*(1-alpha)+warped*alpha)
# Crown and wall/floor shadows in room perspective; no new furniture.
d=ImageDraw.Draw(Image.fromarray(im))
out=Image.fromarray(im)
out.save(r/'architecture-review/gallery5/gallery5_v07_flat_wood_portals_REVIEW.png')
print('SAVED v06',out.size)

