const {app  , BrowserWindow} = require("electron")

function Main() { 

    
    const launchWindow = new BrowserWindow({
        title : " Mubark  Casheer System", 
        'minWidth' : 700,
        'minHeight' : 700,
        "center": true,
        // "alwaysOnTop" : true,
        "autoHideMenuBar" : true , 
        "roundedCorners":true , 
        "darkTheme"  : true , 
        "focusable" : true, 
        "fullscreen" : true , 
        "thickFrame" : true ,
        // "icon" : "icon.ico" , 
        
        
        
        

    });
    launchWindow.maximize()
    launchWindow.show()

    const appUrl = "http://127.0.0.1:789";
    launchWindow.loadURL(appUrl)
    const sessions = launchWindow.webContents.session
    sessions.clearStorageData()

  
}
app.commandLine.appendSwitch("disable-http-cashe")

app.whenReady().then(Main)