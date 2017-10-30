import xbmc
import os, sys
import xbmcaddon
import xbmcgui
from resources.lib.Screenshoter import Screenshoter

addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
addon_dir = xbmc.translatePath(addon.getAddonInfo('path'))
line1 = "Welcome!"
line2 = "Hyperion will be killed in order to enable access to the grabber."

xbmcgui.Dialog().ok(addonname, line1, line2)

options = ["PAL", "NTSC"]
selected_index = xbmcgui.Dialog().select("Select grabber standard:", options)

try:
    os.remove(os.path.join(addon_dir,"screenshot.png"))
except:
    pass

try:
    scsh = Screenshoter()
    scrnshotPath = scsh.takeScreenshot(addon_dir, options[selected_index])
except Exception, e:
    xbmcgui.Dialog().ok(addonname, e.message)
    sys.exit()

try:
    window = xbmcgui.WindowDialog()

    scrnshot = xbmcgui.ControlImage(0, 0, 1280, 720, scrnshotPath)
    window.addControl(scrnshot)
    window.show()
    xbmc.sleep(5000)
    window.close()

except Exception, e:
    xbmcgui.Dialog().ok(addonname, repr(e), "Please report an error at plugin github issue list")
