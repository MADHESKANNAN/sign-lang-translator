const {app,BrowserWindow,session}=require('electron');
app.whenReady().then(()=>{
 session.defaultSession.setPermissionRequestHandler((w,p,cb)=>cb(['media','mediaKeySystem'].includes(p)));
 const win=new BrowserWindow({width:1100,height:800,autoHideMenuBar:true,icon:'icon-512.png'});
 win.loadFile('index.html');
});
app.on('window-all-closed',()=>app.quit());
